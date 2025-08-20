#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强版视频处理器 - 一次性镜头分析，支持多产品识别
"""

import os
import json
import time
import random
import re
from typing import List, Dict, Any

from dotenv import load_dotenv
import ffmpeg
from tqdm import tqdm
import httpx
import ssl
from google import genai

from single_shot_prompts import (
    SINGLE_SHOT_SYSTEM_INSTRUCTION, 
    SINGLE_SHOT_USER_PROMPT, 
    SINGLE_SHOT_RESPONSE_SCHEMA
)
from asset_library import compute_embedding, upsert_asset

load_dotenv()

# 使用高性能模型进行一次性分析
ANALYSIS_MODEL = "models/gemini-2.5-pro"


def _generate_with_retry(client, *, model, contents, config, max_retries=3):
    """带重试的内容生成"""
    attempt = 0
    while True:
        try:
            return client.models.generate_content(
                model=model,
                contents=contents,
                config=config,
            )
        except (httpx.HTTPError, ssl.SSLError) as e:
            attempt += 1
            if attempt > max_retries:
                raise
            delay_seconds = 2 ** attempt + random.uniform(0, 0.5)
            print(f"网络波动（第 {attempt} 次）：{e}. {delay_seconds:.1f}s 后重试...")
            time.sleep(delay_seconds)


def _upload_with_retry(client, *, file, max_retries=5):
    """带重试的文件上传（增强版）"""
    attempt = 0
    while True:
        try:
            print(f"📤 开始上传文件: {os.path.basename(file)} (尝试 {attempt + 1}/{max_retries + 1})")
            result = client.files.upload(file=file)
            print(f"✅ 文件上传成功: {result.name}")
            return result
        except (httpx.HTTPError, ssl.SSLError, Exception) as e:
            attempt += 1
            if attempt > max_retries:
                print(f"❌ 文件上传最终失败，已重试 {max_retries} 次")
                raise
            delay_seconds = min(2 ** attempt + random.uniform(0, 1), 30)  # 最大延迟30秒
            print(f"⚠️ 网络波动（上传，第 {attempt} 次）：{type(e).__name__}: {e}")
            print(f"⏳ {delay_seconds:.1f}s 后重试...")
            time.sleep(delay_seconds)


def _files_get_with_retry(client, *, name, max_retries=3):
    """带重试的文件状态查询"""
    attempt = 0
    while True:
        try:
            return client.files.get(name=name)
        except (httpx.HTTPError, ssl.SSLError) as e:
            attempt += 1
            if attempt > max_retries:
                raise
            delay_seconds = 2 ** attempt + random.uniform(0, 0.5)
            print(f"网络波动（查询文件状态，第 {attempt} 次）：{e}. {delay_seconds:.1f}s 后重试...")
            time.sleep(delay_seconds)


def _files_delete_with_retry(client, *, name, max_retries=2):
    """带重试的文件删除"""
    attempt = 0
    while True:
        try:
            return client.files.delete(name=name)
        except (httpx.HTTPError, ssl.SSLError) as e:
            attempt += 1
            if attempt > max_retries:
                raise
            delay_seconds = 2 ** attempt + random.uniform(0, 0.5)
            print(f"网络波动（删除，第 {attempt} 次）：{e}. {delay_seconds:.1f}s 后重试...")
            time.sleep(delay_seconds)


def _time_to_seconds(time_str: str) -> float:
    """将HH:MM:SS格式转换为秒数"""
    try:
        parts = time_str.split(':')
        return int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])
    except:
        return 0.0


def _seconds_to_time(seconds: float) -> str:
    """将秒数转换为HH:MM:SS格式"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def validate_shot_duration(shots: List[Dict[str, Any]], min_duration: float = 3.0) -> List[Dict[str, Any]]:
    """验证并调整镜头时长，确保每个镜头 ≥ min_duration 秒"""
    print(f"🔍 验证镜头时长（最低 {min_duration} 秒）...")
    
    validated_shots = []
    i = 0
    
    while i < len(shots):
        current_shot = shots[i].copy()
        start_seconds = _time_to_seconds(current_shot['start_time'])
        end_seconds = _time_to_seconds(current_shot['end_time'])
        duration = end_seconds - start_seconds
        
        if duration < min_duration:
            print(f"⚠️ 镜头 {i+1} 时长不足 {min_duration}s ({duration:.1f}s)，尝试合并...")
            
            # 尝试与下一个镜头合并
            if i + 1 < len(shots):
                next_shot = shots[i + 1]
                merged_end_seconds = _time_to_seconds(next_shot['end_time'])
                merged_duration = merged_end_seconds - start_seconds
                
                if merged_duration <= 10.0:  # 合并后不超过10秒
                    # 合并镜头
                    current_shot['end_time'] = next_shot['end_time']
                    current_shot['description'] = f"{current_shot['description']}；{next_shot['description']}"
                    
                    # 合并标签
                    current_shot['tags'] = list(set(current_shot['tags'] + next_shot['tags']))
                    
                    # 合并产品信息
                    if current_shot['has_product'] or next_shot['has_product']:
                        current_shot['has_product'] = True
                        merged_products = current_shot['products'] + next_shot['products']
                        # 去重产品
                        seen_products = set()
                        unique_products = []
                        for product in merged_products:
                            product_key = f"{product['product_type']}_{product['product_name']}"
                            if product_key not in seen_products:
                                seen_products.add(product_key)
                                unique_products.append(product)
                        current_shot['products'] = unique_products
                        
                        # 更新主要产品
                        if unique_products:
                            current_shot['main_product_type'] = unique_products[0]['product_type']
                            current_shot['main_product_name'] = unique_products[0]['product_name']
                    
                    # 合并其他字段
                    current_shot['visuals'] = f"{current_shot['visuals']}；{next_shot['visuals']}"
                    current_shot['human_action'] = f"{current_shot['human_action']}；{next_shot['human_action']}"
                    current_shot['effects_subtitles'] = f"{current_shot['effects_subtitles']}；{next_shot['effects_subtitles']}"
                    
                    print(f"✅ 已合并镜头 {i+1} 和 {i+2}，新时长：{merged_duration:.1f}s")
                    validated_shots.append(current_shot)
                    i += 2  # 跳过下一个镜头（已合并）
                    continue
            
            # 如果无法合并，调整结束时间
            adjusted_end_seconds = start_seconds + min_duration
            current_shot['end_time'] = _seconds_to_time(adjusted_end_seconds)
            print(f"🔧 调整镜头 {i+1} 结束时间：{current_shot['end_time']}")
        
        validated_shots.append(current_shot)
        i += 1
    
    print(f"✅ 验证完成：{len(validated_shots)} 个镜头，所有镜头 ≥ {min_duration}s")
    return validated_shots


def analyze_video_once(video_path: str) -> Dict[str, Any]:
    """
    一次性分析视频，直接输出镜头切割结果
    支持多产品识别和3秒最低时长限制
    """
    print("🚀 启动一次性视频分析流程...")
    print(f"📊 使用模型: {ANALYSIS_MODEL}")
    
    try:
        client = genai.Client()
    except Exception as e:
        print(f"错误：初始化 Gemini Client 失败。请检查您的 API 密钥配置。 {e}")
        return None

    print(f"📁 正在上传视频文件: {video_path}...")
    video_file = None
    
    try:
        video_file = _upload_with_retry(client, file=video_path)
        print(f"📤 视频上传中，文件名称: {video_file.name}")

        while video_file.state.name == "PROCESSING":
            print(".", end="", flush=True)
            time.sleep(10)
            video_file = _files_get_with_retry(client, name=video_file.name)

        if video_file.state.name == "FAILED":
            raise Exception(f"视频处理失败: {video_file.state}")

        print("\n🎯 开始一次性镜头分析（多模态：视频+音频）...")
        
        response = _generate_with_retry(
            client,
            model=ANALYSIS_MODEL,
            contents=[SINGLE_SHOT_USER_PROMPT, video_file],
            config={
                "response_mime_type": "application/json",
                "response_schema": SINGLE_SHOT_RESPONSE_SCHEMA,
                "system_instruction": SINGLE_SHOT_SYSTEM_INSTRUCTION,
            },
            max_retries=3,
        )
        
        analysis_result = json.loads(response.text)
        shots = analysis_result.get('shots', [])
        
        if not shots:
            print("❌ 分析失败：未返回镜头数据")
            return None
        
        print(f"✅ 分析完成！识别出 {len(shots)} 个原始镜头")
        
        # 验证并调整镜头时长
        validated_shots = validate_shot_duration(shots, min_duration=3.0)
        
        # 统计产品信息
        total_products = 0
        product_types = set()
        for shot in validated_shots:
            if shot.get('has_product', False):
                total_products += len(shot.get('products', []))
                for product in shot.get('products', []):
                    product_types.add(product.get('product_type', ''))
        
        print(f"📊 最终结果: {len(validated_shots)} 个镜头")
        print(f"🏷️ 产品统计: {total_products} 个产品，{len(product_types)} 种类型")
        if product_types:
            print(f"📦 产品类型: {', '.join(product_types)}")

        return {
            "shots": validated_shots,
            "analysis_method": "single_shot_analysis",
            "model_used": ANALYSIS_MODEL,
            "total_shots": len(validated_shots),
            "total_products": total_products,
            "product_types": list(product_types)
        }

    except Exception as e:
        print(f"\n处理视频或调用 Gemini API 时发生错误: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"API 响应详情: {e.response}")
        return None
    finally:
        if video_file:
            try:
                print(f"\n🗑️ 分析完成，正在删除临时文件: {video_file.name}...")
                _files_delete_with_retry(client, name=video_file.name)
                print("✅ 临时文件已删除。")
            except Exception as e:
                print(f"警告：删除临时文件 {video_file.name} 时失败。错误：{e}")


def sanitize_filename(name):
    """清理字符串，使其可以安全地用作文件名"""
    name = re.sub(r'[\\/*?:"<>|]', "", name)
    name = name.replace(" ", "_")
    return name[:100]


def cut_video_shots_enhanced(video_path: str, shots: List[Dict[str, Any]], output_dir: str = "output"):
    """
    增强版视频切割，支持多产品信息写入素材库
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print(f"\n✂️ 准备切割视频，共 {len(shots)} 个镜头...")
    
    for idx, shot in enumerate(tqdm(shots, desc="切割进度"), start=1):
        start_time = shot.get("start_time")
        end_time = shot.get("end_time")
        description = shot.get("description", "untitled")

        if not all([start_time, end_time, description]):
            print(f"跳过无效镜头：{shot}")
            continue

        safe_description = sanitize_filename(description)
        output_filename = f"{idx:03d}_{safe_description}.mp4"
        output_path = os.path.join(output_dir, output_filename)

        try:
            # 使用 ffmpeg-python 进行切割
            (
                ffmpeg
                .input(video_path, ss=start_time, to=end_time)
                .output(output_path, c='copy', loglevel='quiet')
                .run(overwrite_output=True)
            )

            # 写入素材库（包含多产品信息）
            embedding = compute_embedding(description) or []
            
            # 处理多产品信息
            products_info = shot.get('products', [])
            main_product_name = shot.get('main_product_name', '')
            
            # 构建产品信息字符串
            product_info_text = ""
            if products_info:
                product_descriptions = []
                for product in products_info:
                    product_desc = f"{product.get('product_name', '')}({product.get('product_type', '')})"
                    if product.get('product_info'):
                        product_desc += f": {product.get('product_info', '')}"
                    product_descriptions.append(product_desc)
                product_info_text = "; ".join(product_descriptions)
            
            record = {
                "source_video": os.path.basename(video_path),
                "segment_path": output_path,
                "start_time": start_time,
                "end_time": end_time,
                "description": description,
                "type": shot.get("type"),
                "tags": shot.get("tags", []),
                "has_product": shot.get("has_product", False),
                "product_info": product_info_text,
                "main_product_name": main_product_name,
                "products_count": len(products_info),
                "visuals": shot.get("visuals", ""),
                "human_action": shot.get("human_action", ""),
                "effects_subtitles": shot.get("effects_subtitles", ""),
                "embedding": embedding,
            }
            
            saved = upsert_asset(record)
            if saved and saved.get("segment_id"):
                print(f"📚 已写入素材库: {saved['segment_id']} -> {output_filename}")
                
        except ffmpeg.Error as e:
            print(f"\n处理镜头 '{output_filename}' ({start_time}-{end_time}) 时发生 FFmpeg 错误:")
            if e.stderr:
                print(f"FFmpeg stderr: {e.stderr.decode('utf8')}")
            else:
                print("无法获取 FFmpeg 的 stderr 输出。")

    print(f"\n✅ 视频切割完成！所有镜头已保存至 '{output_dir}' 目录。")


# 兼容性函数：保持原有接口
def analyze_video(video_path: str) -> Dict[str, Any]:
    """兼容性函数：使用新的一次性分析"""
    return analyze_video_once(video_path)


def cut_video_shots(video_path: str, shots: List[Dict[str, Any]], output_dir: str = "output"):
    """兼容性函数：使用增强版切割"""
    return cut_video_shots_enhanced(video_path, shots, output_dir)


if __name__ == '__main__':
    # 本地测试
    test_video_path = 'input/test_video.mp4'
    if os.path.exists(test_video_path):
        print("🧪 开始测试一次性分析...")
        analysis_result = analyze_video_once(test_video_path)
        if analysis_result and "shots" in analysis_result:
            print("\n✅ 分析成功！")
            print(json.dumps(analysis_result, indent=2, ensure_ascii=False))
            cut_video_shots_enhanced(test_video_path, analysis_result["shots"])
        else:
            print("\n❌ 分析失败。")
    else:
        print(f"测试失败：请在 '{test_video_path}' 放置一个测试视频文件。")
