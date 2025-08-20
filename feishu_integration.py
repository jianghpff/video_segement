#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书多维表格集成模块
将视频分割结果上传到指定的飞书多维表格
"""

import json
import requests
import time
from datetime import datetime
from typing import Dict, List, Any, Optional


class FeishuIntegration:
    def __init__(self):
        self.token_api_url = "https://feishu-token-proxy.1170731839.workers.dev/"
        self.app_token = "T68zbfXIlaHT0TsOuvNc8iEZnib"
        self.table_id = "tblg3kmG712Mw9kZ"
        self.access_token = None
        self.token_expires_at = None
        
    def get_access_token(self) -> str:
        """从API获取飞书访问令牌"""
        try:
            # 检查现有token是否仍然有效
            if self.access_token and self.token_expires_at:
                current_time = datetime.now()
                if current_time < datetime.fromisoformat(self.token_expires_at.replace('Z', '+00:00')):
                    print("使用缓存的访问令牌")
                    return self.access_token
            
            # 重试机制
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    print(f"正在获取新的飞书访问令牌... (尝试 {attempt + 1}/{max_retries})")
                    response = requests.post(self.token_api_url, timeout=30)
                    response.raise_for_status()
                    
                    data = response.json()
                    self.access_token = data['tenant_access_token']
                    self.token_expires_at = data['expires_at']
                    
                    print(f"✅ 成功获取访问令牌，过期时间: {self.token_expires_at}")
                    return self.access_token
                    
                except requests.exceptions.Timeout:
                    if attempt < max_retries - 1:
                        print(f"⏰ 超时，等待 {(attempt + 1) * 5} 秒后重试...")
                        time.sleep((attempt + 1) * 5)
                        continue
                    else:
                        print("❌ 多次尝试后仍然超时")
                        raise
                except Exception as e:
                    if attempt < max_retries - 1:
                        print(f"⚠️ 尝试失败: {e}，等待 {(attempt + 1) * 3} 秒后重试...")
                        time.sleep((attempt + 1) * 3)
                        continue
                    else:
                        raise
            
        except Exception as e:
            print(f"❌ 获取访问令牌失败: {e}")
            raise
    
    def ensure_table_fields(self, access_token: str) -> Dict[str, str]:
        """确保表格包含所需字段，返回字段ID映射"""
        fields_url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{self.app_token}/tables/{self.table_id}/fields"
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        try:
            # 获取现有字段
            response = requests.get(fields_url, headers=headers)
            response.raise_for_status()
            data = response.json()
            
            if data['code'] != 0:
                raise Exception(f"获取字段失败: {data.get('msg', 'Unknown error')}")
            
            existing_fields = {field['field_name']: field['field_id'] for field in data['data']['items']}
            print(f"现有字段: {list(existing_fields.keys())}")
            
            # 定义需要的字段
            required_fields = {
                '视频文件名': 1,  # 文本
                '场景数量': 2,    # 数字
                '镜头数量': 2,    # 数字
                '总时长': 1,     # 文本
                '场景详情': 1,   # 文本（JSON格式）
                '镜头详情': 1,   # 文本（JSON格式）
                '产品类型': 1,   # 文本
                '处理时间': 1,   # 文本
                '处理状态': 1,   # 文本
                '素材库路径': 1, # 文本
            }
            
            field_mapping = {}
            
            # 创建缺失的字段
            for field_name, field_type in required_fields.items():
                if field_name in existing_fields:
                    field_mapping[field_name] = existing_fields[field_name]
                    print(f"字段已存在: {field_name}")
                else:
                    print(f"创建新字段: {field_name}")
                    create_data = {
                        'field_name': field_name,
                        'type': field_type
                    }
                    
                    create_response = requests.post(fields_url, headers=headers, json=create_data)
                    create_response.raise_for_status()
                    create_result = create_response.json()
                    
                    print(f"创建字段响应: {create_result}")  # 调试输出
                    
                    if create_result['code'] != 0:
                        print(f"⚠️ 创建字段 {field_name} 失败: {create_result.get('msg')}")
                        continue
                    
                    # 尝试不同的响应结构
                    field_id = None
                    if 'data' in create_result:
                        data = create_result['data']
                        if 'field_id' in data:
                            field_id = data['field_id']
                        elif 'field' in data and 'field_id' in data['field']:
                            field_id = data['field']['field_id']
                    
                    if field_id:
                        field_mapping[field_name] = field_id
                        print(f"✅ 成功创建字段: {field_name} (ID: {field_id})")
                    else:
                        print(f"⚠️ 无法获取字段ID: {field_name}")
            
            return field_mapping
            
        except Exception as e:
            print(f"❌ 字段处理失败: {e}")
            raise
    
    def format_video_data(self, video_path: str, analysis_result: Dict) -> Dict[str, Any]:
        """格式化视频数据为飞书表格记录"""
        import os
        
        scenes = analysis_result.get('scenes', [])
        shots = analysis_result.get('shots', [])
        
        # 提取产品信息
        product_types = set()
        for scene in scenes:
            if scene.get('has_product') and scene.get('product_type'):
                product_types.add(scene['product_type'])
        
        # 计算总时长（从最后一个镜头的结束时间）
        total_duration = "未知"
        if shots:
            last_shot = shots[-1]
            total_duration = last_shot.get('end_time', '未知')
        
        # 格式化场景详情
        scenes_summary = []
        for i, scene in enumerate(scenes, 1):
            scenes_summary.append({
                '场景': i,
                '时间段': f"{scene.get('start_time', '00:00:00')} - {scene.get('end_time', '00:00:00')}",
                '描述': scene.get('description', ''),
                '有产品': scene.get('has_product', False),
                '产品类型': scene.get('product_type', ''),
                '视觉要点': scene.get('visuals', ''),
                '人物动作': scene.get('human_action', ''),
                '特效字幕': scene.get('effects_subtitles', '')
            })
        
        # 格式化镜头详情
        shots_summary = []
        for i, shot in enumerate(shots, 1):
            shots_summary.append({
                '镜头': i,
                '时间段': f"{shot.get('start_time', '00:00:00')} - {shot.get('end_time', '00:00:00')}",
                '描述': shot.get('description', ''),
                '类型': shot.get('type', ''),
                '标签': shot.get('tags', [])
            })
        
        # 生成输出路径
        video_name = os.path.splitext(os.path.basename(video_path))[0]
        output_dir = f"output/{video_name}"
        
        return {
            '视频文件名': os.path.basename(video_path),
            '场景数量': len(scenes),
            '镜头数量': len(shots),
            '总时长': total_duration,
            '场景详情': json.dumps(scenes_summary, ensure_ascii=False, indent=2),
            '镜头详情': json.dumps(shots_summary, ensure_ascii=False, indent=2),
            '产品类型': '、'.join(product_types) if product_types else '未识别',
            '处理时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            '处理状态': '已完成',
            '素材库路径': output_dir
        }
    
    def upload_record(self, record_data: Dict[str, Any]) -> bool:
        """上传记录到飞书表格"""
        try:
            access_token = self.get_access_token()
            field_mapping = self.ensure_table_fields(access_token)
            
            # 构建请求数据
            fields = {}
            print(f"可用字段映射: {field_mapping}")
            print(f"要上传的数据字段: {list(record_data.keys())}")
            
            for field_name, value in record_data.items():
                if field_name in field_mapping:
                    field_id = field_mapping[field_name]
                    fields[field_id] = value
                    print(f"映射字段: {field_name} -> {field_id} = {str(value)[:50]}...")
                else:
                    print(f"⚠️ 字段 {field_name} 不存在于映射中")
            
            create_url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{self.app_token}/tables/{self.table_id}/records"
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            
            data = {'fields': fields}
            
            print(f"正在上传记录到飞书表格...")
            print(f"请求数据: {data}")
            
            response = requests.post(create_url, headers=headers, json=data)
            response.raise_for_status()
            
            result = response.json()
            print(f"响应结果: {result}")
            
            if result['code'] != 0:
                raise Exception(f"上传失败: {result.get('msg', 'Unknown error')}")
            
            record_id = result['data']['record']['record_id']
            print(f"✅ 成功上传记录，ID: {record_id}")
            return True
            
        except Exception as e:
            print(f"❌ 上传记录失败: {e}")
            return False
    
    def upload_video_analysis(self, video_path: str, analysis_result: Dict) -> bool:
        """上传视频分析结果的主入口"""
        print(f"\n🚀 开始上传视频分析结果到飞书表格")
        print(f"视频: {video_path}")
        print(f"应用Token: {self.app_token}")
        print(f"表格ID: {self.table_id}")
        
        try:
            # 格式化数据
            record_data = self.format_video_data(video_path, analysis_result)
            
            # 上传到飞书
            success = self.upload_record(record_data)
            
            if success:
                print(f"🎉 视频分析结果已成功上传到飞书表格！")
                print(f"📊 场景数量: {record_data['场景数量']}")
                print(f"📹 镜头数量: {record_data['镜头数量']}")
                print(f"⏱️ 总时长: {record_data['总时长']}")
                print(f"🏷️ 产品类型: {record_data['产品类型']}")
            
            return success
            
        except Exception as e:
            print(f"❌ 上传过程发生错误: {e}")
            return False


def test_feishu_integration():
    """测试飞书集成功能"""
    integration = FeishuIntegration()
    
    # 测试获取访问令牌
    try:
        token = integration.get_access_token()
        print(f"测试成功，获取到令牌: {token[:20]}...")
        
        # 测试字段检查
        field_mapping = integration.ensure_table_fields(token)
        print(f"字段映射: {field_mapping}")
        
        return True
    except Exception as e:
        print(f"测试失败: {e}")
        return False


if __name__ == "__main__":
    # 运行测试
    test_feishu_integration()
