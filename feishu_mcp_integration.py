#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书MCP集成模块
使用MCP工具上传视频分析结果到飞书多维表格
"""

import json
import requests
import os
from datetime import datetime
from typing import Dict, List, Any, Optional


class FeishuMCPIntegration:
    def __init__(self):
        self.token_api_url = "https://feishu-token-proxy.1170731839.workers.dev/"
        self.app_token = "T68zbfXIlaHT0TsOuvNc8iEZnib"
        self.table_id = "tblg3kmG712Mw9kZ"
        self.access_token = None
        
    def get_access_token(self) -> str:
        """从API获取飞书访问令牌"""
        try:
            response = requests.post(self.token_api_url, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            self.access_token = data['tenant_access_token']
            
            print(f"✅ 成功获取访问令牌，过期时间: {data.get('expires_at')}")
            return self.access_token
            
        except Exception as e:
            print(f"❌ 获取访问令牌失败: {e}")
            raise
    
    def create_record_via_api(self, record_data: Dict) -> bool:
        """通过直接API调用创建记录"""
        try:
            if not self.access_token:
                self.get_access_token()
            
            url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{self.app_token}/tables/{self.table_id}/records"
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json; charset=utf-8'
            }
            
            data = {
                "fields": record_data
            }
            
            print(f"📤 正在上传记录到飞书表格...")
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            
            result = response.json()
            
            if result.get('code') == 0:
                record_id = result['data']['record']['record_id']
                print(f"✅ 成功上传记录，ID: {record_id}")
                return True
            else:
                print(f"❌ 上传失败: {result.get('msg')}")
                return False
                
        except Exception as e:
            print(f"❌ 上传异常: {e}")
            return False
    
    def upload_video_analysis(self, video_path: str, analysis_result: Dict) -> bool:
        """上传视频分析结果"""
        try:
            print(f"\n🚀 开始上传视频分析结果到飞书表格")
            print(f"视频: {video_path}")
            
            # 提取数据
            video_filename = os.path.basename(video_path)
            scenes = analysis_result.get('scenes', [])
            shots = analysis_result.get('shots', [])
            
            # 计算视频总时长（从最后一个镜头或场景）
            total_duration = "00:00:00"
            if shots and len(shots) > 0:
                last_shot = shots[-1]
                total_duration = last_shot.get('end_time', '00:00:00')
            elif scenes and len(scenes) > 0:
                last_scene = scenes[-1]
                total_duration = last_scene.get('end_time', '00:00:00')
            
            # 提取产品信息
            product_type = "未知"
            if scenes and len(scenes) > 0:
                first_scene = scenes[0]
                product_type = first_scene.get('product_type', '未知')
            
            # 格式化场景详情
            scene_details = []
            for i, scene in enumerate(scenes, 1):
                scene_info = {
                    "场景": i,
                    "时间段": f"{scene.get('start_time', '')} - {scene.get('end_time', '')}",
                    "描述": scene.get('description', ''),
                    "有产品": scene.get('has_product', False),
                    "产品类型": scene.get('product_type', ''),
                    "产品信息": scene.get('product_info', ''),
                    "视觉要点": scene.get('visuals', ''),
                    "人物动作": scene.get('human_action', ''),
                    "特效字幕": scene.get('effects_subtitles', '')
                }
                scene_details.append(scene_info)
            
            # 格式化镜头详情
            shot_details = []
            for i, shot in enumerate(shots, 1):
                shot_info = {
                    "镜头": i,
                    "时间段": f"{shot.get('start_time', '')} - {shot.get('end_time', '')}",
                    "描述": shot.get('description', ''),
                    "类型": shot.get('type', ''),
                    "标签": shot.get('tags', [])
                }
                shot_details.append(shot_info)
            
            # 构建记录数据
            record_data = {
                "视频文件名": video_filename,
                "场景数量": len(scenes),
                "镜头数量": len(shots),
                "总时长": total_duration,
                "场景详情": json.dumps(scene_details, ensure_ascii=False, indent=2),
                "镜头详情": json.dumps(shot_details, ensure_ascii=False, indent=2),
                "产品类型": product_type,
                "处理时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "处理状态": "已完成",
                "素材库路径": f"output/{os.path.splitext(video_filename)[0]}"
            }
            
            # 上传记录
            success = self.create_record_via_api(record_data)
            
            if success:
                print("🎉 视频分析结果已成功上传到飞书多维表格!")
                return True
            else:
                print("⚠️ 飞书上传失败，但本地分析已完成")
                return False
                
        except Exception as e:
            print(f"❌ 上传过程发生异常: {e}")
            return False


def main():
    """测试函数"""
    # 读取分析结果
    with open('output/Douyin_TikTok_Download_API (2)/scenes_meta.json', 'r', encoding='utf-8') as f:
        scenes = json.load(f)
    
    # 模拟镜头数据
    shots = [
        {
            'start_time': '00:00:00',
            'end_time': '00:19:12',
            'description': '女子手持银色护肤品罐，对着镜头讲解',
            'type': 'Primary Shot',
            'tags': ['网红', '产品评测', '护肤品']
        },
        {
            'start_time': '00:19:12',
            'end_time': '00:25:27',
            'description': '女子打开护肤品罐，展示内部膏体',
            'type': 'B-Roll',
            'tags': ['产品开箱', '质地展示']
        },
        {
            'start_time': '00:25:27',
            'end_time': '00:32:00',
            'description': '女子将产品凑近鼻子闻',
            'type': 'Primary Shot',
            'tags': ['感官体验', '无香料']
        },
        {
            'start_time': '00:32:00',
            'end_time': '00:44:00',
            'description': '女子微笑继续讲解推荐',
            'type': 'Primary Shot',
            'tags': ['微笑', '积极反应', '产品推荐']
        }
    ]
    
    analysis_result = {
        'scenes': scenes,
        'shots': shots
    }
    
    # 执行上传
    feishu = FeishuMCPIntegration()
    success = feishu.upload_video_analysis('input/Douyin_TikTok_Download_API (2).mp4', analysis_result)
    print(f'上传结果: {success}')


if __name__ == "__main__":
    main()
