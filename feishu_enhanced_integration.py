#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书增强集成模块 - 支持视频上传和扁平化镜头表设计
每个镜头作为一条独立记录上传到飞书多维表格
"""

import json
import requests
import os
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path


class FeishuEnhancedIntegration:
    def __init__(self):
        self.token_api_url = "https://feishu-token-proxy.1170731839.workers.dev/"
        self.app_token = "T68zbfXIlaHT0TsOuvNc8iEZnib"
        self.table_id = "tblg3kmG712Mw9kZ"
        self.access_token = None
        
        # 新的字段映射（扁平化镜头表 - 兼容现有字段）
        self.shot_fields = {
            "原视频文件名": "text",
            "镜头序号": "number", 
            "镜头ID": "text",
            "开始时间": "text",
            "结束时间": "text",
            "镜头时长": "text",
            "镜头描述": "text",
            "镜头类型": "select",
            "镜头标签": "text",
            "包含产品": "checkbox",
            "产品信息": "text",  # 合并所有产品信息（包含中文名称和数量）
            "视觉描述": "text",
            "人物动作": "text",
            "特效字幕": "text",
            "镜头视频": "attachment",
            "处理时间": "text",
            "AI分析质量": "number"
        }
        
    def get_access_token(self) -> str:
        """从API获取飞书访问令牌"""
        for attempt in range(3):
            try:
                print(f"正在获取新的飞书访问令牌... (尝试 {attempt + 1}/3)")
                response = requests.post(self.token_api_url, timeout=30)
                response.raise_for_status()
                
                data = response.json()
                self.access_token = data['tenant_access_token']
                
                print(f"✅ 成功获取访问令牌，过期时间: {data.get('expires_at')}")
                return self.access_token
                
            except Exception as e:
                if attempt < 2:
                    wait_time = (attempt + 1) * 3
                    print(f"⚠️ 尝试失败: {e}，等待 {wait_time} 秒后重试...")
                    time.sleep(wait_time)
                else:
                    print(f"❌ 获取访问令牌失败: {e}")
                    raise
    
    def upload_video_file(self, video_path: str, filename: str = None) -> str:
        """上传单个视频文件到飞书，返回file_token"""
        try:
            if not self.access_token:
                self.get_access_token()
            
            if not filename:
                filename = os.path.basename(video_path)
            
            # 读取视频文件
            with open(video_path, 'rb') as f:
                video_buffer = f.read()
            
            print(f"📤 正在上传视频文件: {filename} ({len(video_buffer)} bytes)")
            
            # 准备上传数据
            upload_url = 'https://open.feishu.cn/open-apis/drive/v1/medias/upload_all'
            
            files = {
                'file_name': (None, filename),
                'parent_type': (None, 'bitable_file'),
                'parent_node': (None, self.app_token),
                'size': (None, str(len(video_buffer))),
                'file': (filename, video_buffer, 'video/mp4')
            }
            
            headers = {
                'Authorization': f'Bearer {self.access_token}'
            }
            
            response = requests.post(upload_url, headers=headers, files=files, timeout=120)
            response.raise_for_status()
            
            result = response.json()
            
            if result.get('code') == 0:
                file_token = result['data']['file_token']
                print(f"✅ 视频上传成功: {filename} -> {file_token}")
                return file_token
            else:
                raise Exception(f"上传失败: {result.get('msg')}")
                
        except Exception as e:
            print(f"❌ 视频上传失败: {e}")
            return None
    
    def ensure_shot_table_fields(self) -> Dict[str, str]:
        """确保表格中存在所需的镜头字段"""
        try:
            if not self.access_token:
                self.get_access_token()
            
            # 获取现有字段
            fields_url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{self.app_token}/tables/{self.table_id}/fields"
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json; charset=utf-8'
            }
            
            response = requests.get(fields_url, headers=headers)
            response.raise_for_status()
            result = response.json()
            
            if result['code'] != 0:
                raise Exception(f"获取字段失败: {result.get('msg')}")
            
            existing_fields = {field['field_name']: field['field_id'] for field in result['data']['items']}
            print(f"现有字段: {list(existing_fields.keys())}")
            
            field_mapping = {}
            
            # 检查并创建缺失的字段
            for field_name, field_type in self.shot_fields.items():
                if field_name in existing_fields:
                    field_mapping[field_name] = existing_fields[field_name]
                    print(f"字段已存在: {field_name}")
                else:
                    # 创建新字段
                    field_id = self.create_field(field_name, field_type, headers)
                    if field_id:
                        field_mapping[field_name] = field_id
                        print(f"✅ 成功创建字段: {field_name}")
            
            return field_mapping
            
        except Exception as e:
            print(f"❌ 字段设置失败: {e}")
            return {}
    
    def create_field(self, field_name: str, field_type: str, headers: Dict) -> str:
        """创建新字段"""
        try:
            fields_url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{self.app_token}/tables/{self.table_id}/fields"
            
            # 字段类型映射
            type_mapping = {
                "text": {"type": 1},  # 多行文本
                "number": {"type": 2},  # 数字
                "select": {"type": 1},  # 暂时改为文本类型，避免单选字段创建问题
                "checkbox": {"type": 7},  # 复选框
                "attachment": {"type": 17}  # 附件
            }
            
            if field_type not in type_mapping:
                field_type = "text"  # 默认为文本
            
            create_data = {
                "field_name": field_name,
                "ui_type": field_type.title(),
                **type_mapping[field_type]
            }
            
            response = requests.post(fields_url, headers=headers, json=create_data)
            response.raise_for_status()
            result = response.json()
            
            if result['code'] == 0:
                return result['data']['field']['field_id']
            else:
                print(f"⚠️ 创建字段 {field_name} 失败: {result.get('msg')}")
                return None
                
        except Exception as e:
            print(f"❌ 创建字段异常: {e}")
            return None
    
    def create_shot_record(self, shot_data: Dict, video_file_token: str = None) -> bool:
        """创建单个镜头记录（支持多产品字段）"""
        try:
            if not self.access_token:
                self.get_access_token()
            
            print("🔧 创建镜头记录（支持多产品）")
            
            # 构建记录数据 - 直接使用字段名称
            fields = {}
            
            # 基础信息
            fields["原视频文件名"] = shot_data.get("original_video_name", "")
            fields["镜头序号"] = shot_data.get("shot_number", 0)
            fields["镜头ID"] = shot_data.get("shot_id", "")
            
            # 时间信息
            fields["开始时间"] = shot_data.get("start_time", "")
            fields["结束时间"] = shot_data.get("end_time", "")
            fields["镜头时长"] = shot_data.get("duration", "")
            
            # 内容描述
            fields["镜头描述"] = shot_data.get("description", "")
            
            tags = shot_data.get("tags", [])
            fields["镜头标签"] = ", ".join(tags) if tags else ""
            
            # 多产品信息处理（合并到现有字段）
            has_product = shot_data.get("has_product", False)
            fields["包含产品"] = has_product
            
            if has_product:
                # 处理多产品列表
                products = shot_data.get("products", [])
                if products:
                    # 构建详细的产品信息字符串
                    product_info_parts = []
                    
                    # 添加产品数量信息
                    product_info_parts.append(f"【产品数量】{len(products)}个")
                    
                    # 添加主要产品名称
                    main_product = products[0] if products else {}
                    main_product_name = main_product.get("product_name", "")
                    if main_product_name:
                        product_info_parts.append(f"【主要产品】{main_product_name}")
                    
                    # 添加所有产品详细信息
                    product_details = []
                    for i, product in enumerate(products, 1):
                        detail = f"{i}.{product.get('product_name', '')}({product.get('product_type', '')})"
                        if product.get('product_info'):
                            detail += f" - {product.get('product_info', '')}"
                        product_details.append(detail)
                    
                    if product_details:
                        product_info_parts.append(f"【产品详情】{'; '.join(product_details)}")
                    
                    fields["产品信息"] = " | ".join(product_info_parts)
                else:
                    fields["产品信息"] = ""
            else:
                fields["产品信息"] = ""
            
            # 视觉内容
            fields["视觉描述"] = shot_data.get("visuals", "")
            fields["人物动作"] = shot_data.get("human_action", "")
            fields["特效字幕"] = shot_data.get("effects_subtitles", "")
            
            # 视频附件
            if video_file_token:
                fields["镜头视频"] = [
                    {
                        "file_token": video_file_token,
                        "name": shot_data.get("video_filename", "镜头视频.mp4")
                    }
                ]
            
            # 元数据
            fields["处理时间"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            fields["AI分析质量"] = 5  # 默认满分
            
            # 创建记录
            create_url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{self.app_token}/tables/{self.table_id}/records"
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json; charset=utf-8'
            }
            
            data = {"fields": fields}
            
            print(f"📤 正在创建镜头记录: {shot_data.get('shot_id', 'Unknown')}")
            print(f"请求数据字段数量: {len(fields)}")
            print(f"字段ID列表: {list(fields.keys())}")
            
            response = requests.post(create_url, headers=headers, json=data)
            response.raise_for_status()
            
            result = response.json()
            
            if result.get('code') == 0:
                record_id = result['data']['record']['record_id']
                print(f"✅ 成功创建记录，ID: {record_id}")
                return True
            else:
                print(f"❌ 创建记录失败: {result.get('msg')}")
                print(f"详细错误: {result}")
                return False
                
        except Exception as e:
            print(f"❌ 创建记录异常: {e}")
            return False
    
    def upload_video_analysis_enhanced(self, video_path: str, analysis_result: Dict) -> bool:
        """上传完整的视频分析结果（扁平化镜头表模式）"""
        try:
            print(f"\n🚀 开始上传视频分析结果到飞书表格（扁平化镜头表模式）")
            print(f"视频: {video_path}")
            
            video_filename = os.path.basename(video_path)
            video_base_name = os.path.splitext(video_filename)[0]
            shots = analysis_result.get('shots', [])
            
            if not shots:
                print("❌ 没有找到镜头数据")
                return False
            
            # 获取切割后的视频文件目录
            output_dir = f"output/{video_base_name}"
            
            success_count = 0
            total_shots = len(shots)
            
            print(f"📊 准备处理 {total_shots} 个镜头")
            
            for i, shot in enumerate(shots, 1):
                try:
                    print(f"\n--- 处理镜头 {i}/{total_shots} ---")
                    
                    # 构建镜头数据（支持多产品）
                    shot_data = {
                        "original_video_name": video_filename,
                        "shot_number": i,
                        "shot_id": f"{video_base_name}_shot_{i:03d}",
                        "start_time": shot.get("start_time", ""),
                        "end_time": shot.get("end_time", ""),
                        "duration": self.calculate_duration(shot.get("start_time", ""), shot.get("end_time", "")),
                        "description": shot.get("description", ""),
                        "type": shot.get("type", ""),
                        "tags": shot.get("tags", []),
                        "has_product": shot.get("has_product", False),
                        "products": shot.get("products", []),  # 多产品支持
                        "main_product_name": shot.get("main_product_name", ""),
                        "visuals": shot.get("visuals", ""),
                        "human_action": shot.get("human_action", ""),
                        "effects_subtitles": shot.get("effects_subtitles", "")
                    }
                    
                    # 查找对应的视频文件
                    video_files = list(Path(output_dir).glob(f"{i:03d}_*.mp4"))
                    video_file_token = None
                    
                    if video_files:
                        video_file_path = str(video_files[0])
                        video_filename = os.path.basename(video_file_path)
                        shot_data["video_filename"] = video_filename
                        
                        # 上传视频文件
                        print(f"📤 上传镜头视频: {video_filename}")
                        video_file_token = self.upload_video_file(video_file_path, video_filename)
                        
                        if not video_file_token:
                            print(f"⚠️ 镜头 {i} 的视频上传失败，跳过文件关联")
                    else:
                        print(f"⚠️ 未找到镜头 {i} 对应的视频文件")
                    
                    # 创建镜头记录
                    if self.create_shot_record(shot_data, video_file_token):
                        success_count += 1
                        print(f"✅ 镜头 {i} 处理成功")
                    else:
                        print(f"❌ 镜头 {i} 处理失败")
                    
                    # 添加延迟避免API限制
                    time.sleep(1)
                    
                except Exception as e:
                    print(f"❌ 镜头 {i} 处理异常: {e}")
                    continue
            
            print(f"\n🎉 上传完成！成功处理 {success_count}/{total_shots} 个镜头")
            return success_count > 0
            
        except Exception as e:
            print(f"❌ 整体上传过程异常: {e}")
            return False
    

    
    def calculate_duration(self, start_time: str, end_time: str) -> str:
        """计算镜头时长"""
        try:
            def time_to_seconds(time_str):
                parts = time_str.split(':')
                return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
            
            start_seconds = time_to_seconds(start_time)
            end_seconds = time_to_seconds(end_time)
            duration_seconds = end_seconds - start_seconds
            
            return f"{duration_seconds}秒"
        except:
            return "未知"


def main():
    """测试函数"""
    # 测试扁平化镜头表上传
    import json
    
    # 读取分析结果
    with open('output/Douyin_TikTok_Download_API (2)/scenes_meta.json', 'r', encoding='utf-8') as f:
        scenes = json.load(f)
    
    # 模拟镜头数据（从实际输出获取）
    shots = [
        {
            'start_time': '00:00:00',
            'end_time': '00:00:19',
            'description': '女士手持银色罐装面霜，向镜头介绍产品特点和适合人群',
            'type': 'Primary Shot',
            'tags': ['产品介绍', '面霜', '成分讲解'],
            'has_product': True,
            'product_type': '面霜',
            'product_info': 'TOP SKIN, 5X CERAMIDE, 4D HA, CENTELLA, PANTHENOL',
            'visuals': '女士，粉色西装外套，白色内搭，佩戴戒指',
            'human_action': '女士面向镜头，手持产品，边说边点头',
            'effects_subtitles': '泰语字幕和产品成分信息图'
        },
        {
            'start_time': '00:00:19',
            'end_time': '00:00:25',
            'description': '女士拧开面霜的银色盖子，展示产品内部的白色膏体',
            'type': 'Primary Shot',
            'tags': ['产品开箱', '面霜展示'],
            'has_product': True,
            'product_type': '面霜',
            'product_info': 'TOP SKIN',
            'visuals': '女士，产品为银色瓶盖，深蓝色瓶身',
            'human_action': '女士用双手将面霜盖子拧开',
            'effects_subtitles': '泰语字幕'
        }
    ]
    
    analysis_result = {
        'scenes': scenes,
        'shots': shots
    }
    
    # 执行上传
    feishu = FeishuEnhancedIntegration()
    success = feishu.upload_video_analysis_enhanced('input/Douyin_TikTok_Download_API (2).mp4', analysis_result)
    print(f'\n📊 最终结果: {success}')


if __name__ == "__main__":
    main()
