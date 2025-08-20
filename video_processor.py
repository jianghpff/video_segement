import os
import json
from google import genai
from dotenv import load_dotenv
from prompts import (
    SCENE_SYSTEM_INSTRUCTION, SCENE_USER_PROMPT, SCENE_RESPONSE_SCHEMA,
    SHOT_SYSTEM_INSTRUCTION, SHOT_USER_PROMPT, SHOT_RESPONSE_SCHEMA
)
from prompts_new import (
    ENHANCED_SHOT_SYSTEM_INSTRUCTION, ENHANCED_SHOT_USER_PROMPT, ENHANCED_SHOT_RESPONSE_SCHEMA
)
import time
import ffmpeg
from tqdm import tqdm
import re
import httpx
import ssl
import random
from asset_library import compute_embedding, upsert_asset

# 模型配置：宏观场景使用 2.5-flash，微观镜头使用 2.5-pro
SCENE_MODEL = "models/gemini-2.5-flash"
SHOT_MODEL = "models/gemini-2.5-pro"


def _generate_with_retry(client, *, model, contents, config, max_retries=3):
    """
    Wrapper for client.models.generate_content with retry/backoff to handle transient
    network/TLS issues (e.g., EOF, RemoteProtocolError).
    """
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


def _upload_with_retry(client, *, file, max_retries=3):
	attempt = 0
	while True:
		try:
			return client.files.upload(file=file)
		except (httpx.HTTPError, ssl.SSLError) as e:
			attempt += 1
			if attempt > max_retries:
				raise
			delay_seconds = 2 ** attempt + random.uniform(0, 0.5)
			print(f"网络波动（上传，第 {attempt} 次）：{e}. {delay_seconds:.1f}s 后重试...")
			time.sleep(delay_seconds)


def _files_get_with_retry(client, *, name, max_retries=3):
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

# 加载 .env 文件中的环境变量
load_dotenv()

def analyze_video(video_path):
    """
    使用分层的两阶段分析法来分析视频。
    阶段一：识别宏观场景。
    阶段二：在每个场景内识别微观镜头和动作。
    """
    print("启动两阶段视频分析流程...")
    
    try:
        client = genai.Client()
    except Exception as e:
        print(f"错误：初始化 Gemini Client 失败。请检查您的 API 密钥配置。 {e}")
        return None

    print(f"正在上传视频文件以进行宏观场景分析: {video_path}...")
    video_file = None
    all_fine_grained_shots = []

    try:
        video_file = _upload_with_retry(client, file=video_path)
        print(f"视频上传中，文件名称: {video_file.name}")

        while video_file.state.name == "PROCESSING":
            print(".", end="", flush=True)
            time.sleep(10)
            video_file = _files_get_with_retry(client, name=video_file.name)

        if video_file.state.name == "FAILED":
            raise Exception(f"视频处理失败: {video_file.state}")

        # --- 阶段一：宏观场景分析 ---
        print("\n阶段一：开始宏观场景分析...")
        scene_response = _generate_with_retry(
            client,
            model=SCENE_MODEL,
            contents=[SCENE_USER_PROMPT, video_file],
            config={
                "response_mime_type": "application/json",
                "response_schema": SCENE_RESPONSE_SCHEMA,
                "system_instruction": SCENE_SYSTEM_INSTRUCTION,
            },
            max_retries=3,
        )
        scenes = json.loads(scene_response.text).get('scenes', [])
        print(f"宏观分析完成，识别出 {len(scenes)} 个场景。")

        # --- 阶段二：微观镜头分析 ---
        print("\n阶段二：开始微观镜头分析...")
        for i, scene in enumerate(scenes):
            start_time = scene['start_time']
            end_time = scene['end_time']
            print(f"  正在分析场景 {i+1}/{len(scenes)} ({start_time} -> {end_time})...")

            shot_prompt = f"请严格分析从 {start_time} 到 {end_time} 之间的视频内容。\n\n{SHOT_USER_PROMPT}"
            
            shot_response = _generate_with_retry(
                client,
                model=SHOT_MODEL,
                contents=[shot_prompt, video_file],
                config={
                    "response_mime_type": "application/json",
                    "response_schema": SHOT_RESPONSE_SCHEMA,
                    "system_instruction": SHOT_SYSTEM_INSTRUCTION,
                },
                max_retries=3,
            )
            shots_in_scene = json.loads(shot_response.text).get('shots', [])
            print(f"  场景 {i+1} 分析完成，识别出 {len(shots_in_scene)} 个镜头。")
            all_fine_grained_shots.extend(shots_in_scene)

        # 返回包含场景元数据与镜头明细的结构
        return {"scenes": scenes, "shots": all_fine_grained_shots}

    except Exception as e:
        print(f"\n处理视频或调用 Gemini API 时发生错误: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"API 响应详情: {e.response}")
        return None
    finally:
        if video_file:
            try:
                print(f"\n分析流程结束，正在删除临时文件: {video_file.name}...")
                _files_delete_with_retry(client, name=video_file.name)
                print("临时文件已删除。")
            except Exception as e:
                print(f"警告：删除临时文件 {video_file.name} 时失败。错误：{e}")


def sanitize_filename(name):
    """
    清理字符串，使其可以安全地用作文件名。
    """
    name = re.sub(r'[\\/*?:"<>|]', "", name)
    name = name.replace(" ", "_")
    return name[:100]

def cut_video_shots(video_path, shots, output_dir="output"):
    """
    Cuts a video into smaller shots based on the provided list of shots.
    Each shot should be a dictionary with 'start_time', 'end_time', and 'description'.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print(f"\n准备切割视频，共 {len(shots)} 个镜头...")
    
    # 使用 tqdm 创建进度条
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
        filename = output_filename

        try:
            # 使用 ffmpeg-python 进行切割
            (
                ffmpeg
                .input(video_path, ss=start_time, to=end_time)
                .output(output_path, c='copy', loglevel='quiet') # c='copy' for fast, lossless cuts
                .run(overwrite_output=True)
            )

            # 写入素材库（包含向量嵌入）
            embedding = compute_embedding(description) or []
            record = {
                "source_video": os.path.basename(video_path),
                "segment_path": output_path,
                "start_time": start_time,
                "end_time": end_time,
                "description": description,
                "type": shot.get("type"),
                "tags": shot.get("tags", []),
                "embedding": embedding,
            }
            saved = upsert_asset(record)
            if saved and saved.get("segment_id"):
                print(f"已写入素材库: {saved['segment_id']} -> {output_filename}")
        except ffmpeg.Error as e:
            # 打印更详细的错误日志
            print(f"\n处理镜头 '{filename}' ({start_time}-{end_time}) 时发生 FFmpeg 错误:")
            # e.stderr 不是公开属性，但通常能提供有用信息
            if e.stderr:
                 print(f"FFmpeg stderr: {e.stderr.decode('utf8')}")
            else:
                 print("无法获取 FFmpeg 的 stderr 输出。")


    print(f"\n视频切割完成！所有镜头已保存至 '{output_dir}' 目录。")


def analyze_video_enhanced(video_path):
    """
    重构版本：使用Gemini-2.5-flash一次性完成丰富的镜头分析
    返回格式保持兼容：{"scenes": [...], "shots": [...]}
    但scenes为空，所有信息都在shots中
    """
    try:
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("❌ 请在 .env 文件中设置您的 GEMINI_API_KEY")
            return None

        client = genai.Client()
        
        print("📁 正在上传视频文件...")
        uploaded_file = _upload_with_retry(client, file=video_path)
        print(f"✅ 视频上传成功: {uploaded_file.name}")
        
        print("🤖 开始一体化视频分析（使用Gemini-2.5-flash）...")
        
        generation_config = {
            "response_mime_type": "application/json",
            "response_schema": ENHANCED_SHOT_RESPONSE_SCHEMA
        }
        
        # 等待视频处理完成
        while uploaded_file.state.name == "PROCESSING":
            print(".", end="", flush=True)
            time.sleep(10)
            uploaded_file = _files_get_with_retry(client, name=uploaded_file.name)

        if uploaded_file.state.name == "FAILED":
            raise Exception(f"视频处理失败: {uploaded_file.state}")
        
        # 使用Gemini-2.5-flash进行一次性分析
        response = _generate_with_retry(
            client,
            model="models/gemini-2.5-flash",
            contents=[ENHANCED_SHOT_USER_PROMPT, uploaded_file],
            config={
                "response_mime_type": "application/json",
                "response_schema": ENHANCED_SHOT_RESPONSE_SCHEMA,
                "system_instruction": ENHANCED_SHOT_SYSTEM_INSTRUCTION,
            }
        )
        
        if not response or not response.text:
            print("❌ Gemini 返回空响应")
            return None
            
        try:
            analysis_result = json.loads(response.text)
            shots = analysis_result.get("shots", [])
            
            if not shots:
                print("❌ 未检测到有效的镜头数据")
                return None
            
            print(f"✅ 分析完成！检测到 {len(shots)} 个镜头")
            
            # 为了保持兼容性，构造返回格式包含scenes和shots
            # scenes将基于shots数据生成摘要
            scenes = generate_scenes_from_shots(shots)
            
            return {
                "scenes": scenes,
                "shots": shots
            }
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON解析失败: {e}")
            print(f"原始响应: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ 分析过程中发生错误: {e}")
        return None


def generate_scenes_from_shots(shots):
    """
    从镜头数据生成场景摘要，保持兼容性
    """
    if not shots:
        return []
    
    # 提取整体信息
    first_shot = shots[0]
    last_shot = shots[-1]
    
    # 统计产品信息
    product_shots = [shot for shot in shots if shot.get('has_product', False)]
    product_types = list(set([shot.get('product_type', '未知') for shot in product_shots if shot.get('product_type') != '未知']))
    
    # 合并所有产品信息
    product_info_list = [shot.get('product_info', '') for shot in shots if shot.get('product_info', '').strip()]
    product_info = '; '.join(set(product_info_list)) if product_info_list else ''
    
    # 合并视觉描述
    visual_descriptions = [shot.get('description', '') for shot in shots]
    combined_description = '；'.join(visual_descriptions[:3])  # 取前3个镜头的描述
    
    # 生成场景
    scene = {
        "start_time": first_shot.get('start_time', '00:00:00'),
        "end_time": last_shot.get('end_time', '00:00:00'),
        "description": combined_description,
        "has_product": len(product_shots) > 0,
        "product_type": product_types[0] if product_types else '未知',
        "product_info": product_info,
        "visuals": first_shot.get('visuals', ''),
        "human_action": first_shot.get('human_action', ''),
        "effects_subtitles": first_shot.get('effects_subtitles', '')
    }
    
    return [scene]


# 本地测试功能
if __name__ == '__main__':
    test_video_path = 'input/Douyin_TikTok_Download_API - 2025-07-08T163658.981.mp4'  # 请替换为你的测试视频路径
    if os.path.exists(test_video_path):
        analysis_result = analyze_video(test_video_path)
        if analysis_result and "shots" in analysis_result:
            print("\n分析成功！结果如下：")
            print(json.dumps(analysis_result, indent=2, ensure_ascii=False))
            cut_video_shots(test_video_path, analysis_result["shots"])
        else:
            print("\n分析失败或返回结果格式不正确。")
    else:
        print(f"测试失败：请在 '{test_video_path}' 放置一个测试视频文件。")
