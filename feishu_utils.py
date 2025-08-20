#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书多维表通用工具类 - 可复用的飞书操作封装
根据实践经验总结的标准化操作模块
"""

import requests
import time
import json
from typing import Dict, List, Any, Optional
from datetime import datetime


class FeishuBitableUtils:
    """飞书多维表通用工具类"""
    
    def __init__(self, app_token: str = "T68zbfXIlaHT0TsOuvNc8iEZnib", 
                 table_id: str = "tblg3kmG712Mw9kZ"):
        """
        初始化飞书工具
        
        Args:
            app_token: 多维表应用Token
            table_id: 表格ID
        """
        self.token_api_url = "https://feishu-token-proxy.1170731839.workers.dev/"
        self.app_token = app_token
        self.table_id = table_id
        self.access_token = None
        self.token_expires_at = None
        
    def get_access_token(self, max_retries: int = 3) -> str:
        """
        获取飞书访问令牌 - 带重试机制
        
        返回: 访问令牌字符串
        异常: 获取失败时抛出异常
        """
        for attempt in range(max_retries):
            try:
                response = requests.post(self.token_api_url, timeout=30)
                response.raise_for_status()
                
                data = response.json()
                self.access_token = data['tenant_access_token']
                self.token_expires_at = data.get('expires_at')
                
                print(f"✅ 获取飞书令牌成功 (尝试 {attempt + 1}/{max_retries})")
                return self.access_token
                
            except Exception as e:
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 3
                    print(f"⚠️ 获取令牌失败，{wait_time}s后重试: {e}")
                    time.sleep(wait_time)
                else:
                    raise Exception(f"获取访问令牌最终失败: {e}")
    
    def ensure_field_exists(self, field_name: str, field_type: str = "text") -> str:
        """
        确保字段存在，不存在则创建
        
        Args:
            field_name: 字段名称
            field_type: 字段类型 (text/number/checkbox/attachment)
            
        返回: 字段ID
        """
        if not self.access_token:
            self.get_access_token()
        
        fields_url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{self.app_token}/tables/{self.table_id}/fields"
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json; charset=utf-8'
        }
        
        # 获取现有字段
        response = requests.get(fields_url, headers=headers)
        response.raise_for_status()
        result = response.json()
        
        if result['code'] != 0:
            raise Exception(f"获取字段失败: {result.get('msg')}")
        
        existing_fields = {field['field_name']: field['field_id'] for field in result['data']['items']}
        
        if field_name in existing_fields:
            print(f"✅ 字段已存在: {field_name}")
            return existing_fields[field_name]
        
        # 创建新字段
        type_mapping = {
            "text": {"type": 1, "ui_type": "Text"},
            "number": {"type": 2, "ui_type": "Number"},
            "checkbox": {"type": 7, "ui_type": "Checkbox"},
            "attachment": {"type": 17, "ui_type": "Attachment"}
        }
        
        if field_type not in type_mapping:
            field_type = "text"
        
        create_data = {
            "field_name": field_name,
            **type_mapping[field_type]
        }
        
        response = requests.post(fields_url, headers=headers, json=create_data)
        response.raise_for_status()
        result = response.json()
        
        if result['code'] == 0:
            field_id = result['data']['field']['field_id']
            print(f"✅ 成功创建字段: {field_name} (ID: {field_id})")
            return field_id
        else:
            raise Exception(f"创建字段失败: {result.get('msg')}")
    
    def upload_file(self, file_path: str, filename: str = None) -> str:
        """
        上传文件到飞书并返回file_token
        
        Args:
            file_path: 本地文件路径
            filename: 文件名（可选）
            
        返回: file_token字符串
        """
        if not self.access_token:
            self.get_access_token()
        
        if not filename:
            import os
            filename = os.path.basename(file_path)
        
        with open(file_path, 'rb') as f:
            file_content = f.read()
        
        upload_url = 'https://open.feishu.cn/open-apis/drive/v1/medias/upload_all'
        
        files = {
            'file_name': (None, filename),
            'parent_type': (None, 'bitable_file'),
            'parent_node': (None, self.app_token),
            'size': (None, str(len(file_content))),
            'file': (filename, file_content, 'video/mp4')
        }
        
        headers = {'Authorization': f'Bearer {self.access_token}'}
        
        response = requests.post(upload_url, headers=headers, files=files, timeout=120)
        response.raise_for_status()
        
        result = response.json()
        
        if result.get('code') == 0:
            file_token = result['data']['file_token']
            print(f"✅ 文件上传成功: {filename} -> {file_token}")
            return file_token
        else:
            raise Exception(f"文件上传失败: {result.get('msg')}")
    
    def create_record(self, fields_data: Dict[str, Any]) -> str:
        """
        创建新记录
        
        Args:
            fields_data: 字段数据字典，键为字段名称，值为字段值
            
        返回: 记录ID
        """
        if not self.access_token:
            self.get_access_token()
        
        create_url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{self.app_token}/tables/{self.table_id}/records"
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json; charset=utf-8'
        }
        
        data = {"fields": fields_data}
        
        response = requests.post(create_url, headers=headers, json=data)
        response.raise_for_status()
        
        result = response.json()
        
        if result.get('code') == 0:
            record_id = result['data']['record']['record_id']
            print(f"✅ 记录创建成功: {record_id}")
            return record_id
        else:
            raise Exception(f"创建记录失败: {result.get('msg')}")
    
    def update_record(self, record_id: str, fields_data: Dict[str, Any]) -> bool:
        """
        更新记录 - 关键：使用PUT方法而不是PATCH
        
        Args:
            record_id: 记录ID
            fields_data: 要更新的字段数据
            
        返回: 是否成功
        """
        if not self.access_token:
            self.get_access_token()
        
        update_url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{self.app_token}/tables/{self.table_id}/records/{record_id}"
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json; charset=utf-8'
        }
        
        data = {"fields": fields_data}
        
        # 关键：使用PUT而不是PATCH
        response = requests.put(update_url, headers=headers, json=data)
        response.raise_for_status()
        
        result = response.json()
        
        if result['code'] == 0:
            print(f"✅ 记录更新成功: {record_id}")
            return True
        else:
            print(f"❌ 记录更新失败: {result.get('msg')}")
            return False
    
    def get_all_records(self, page_size: int = 500) -> List[Dict]:
        """
        获取表中所有记录
        
        Args:
            page_size: 每页记录数
            
        返回: 记录列表
        """
        if not self.access_token:
            self.get_access_token()
        
        records_url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{self.app_token}/tables/{self.table_id}/records"
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        
        params = {'page_size': page_size}
        
        response = requests.get(records_url, headers=headers, params=params)
        response.raise_for_status()
        result = response.json()
        
        if result['code'] != 0:
            raise Exception(f"获取记录失败: {result.get('msg')}")
        
        records = result['data']['items']
        print(f"📊 获取到 {len(records)} 条记录")
        return records
    
    def batch_update_records(self, updates: List[Dict[str, Any]], delay: float = 1.0) -> int:
        """
        批量更新记录
        
        Args:
            updates: 更新列表，每项包含 {'record_id': str, 'fields': dict}
            delay: 操作间隔秒数，避免API限流
            
        返回: 成功更新的记录数
        """
        success_count = 0
        total = len(updates)
        
        print(f"🚀 开始批量更新 {total} 条记录...")
        
        for i, update_data in enumerate(updates, 1):
            try:
                record_id = update_data['record_id']
                fields = update_data['fields']
                
                if self.update_record(record_id, fields):
                    success_count += 1
                
                # 避免API限流
                if i < total:
                    time.sleep(delay)
                    
            except Exception as e:
                print(f"❌ 记录 {i} 更新异常: {e}")
                continue
        
        print(f"🎉 批量更新完成: {success_count}/{total}")
        return success_count


# 使用示例和最佳实践
def demo_usage():
    """演示如何使用飞书工具类"""
    
    # 1. 初始化工具
    feishu = FeishuBitableUtils()
    
    # 2. 确保字段存在
    product_field_id = feishu.ensure_field_exists("产品名称", "text")
    
    # 3. 上传文件
    # file_token = feishu.upload_file("/path/to/video.mp4", "镜头001.mp4")
    
    # 4. 创建记录
    # record_id = feishu.create_record({
    #     "镜头描述": "产品介绍镜头",
    #     "包含产品": True,
    #     "产品名称": "มอยซ์เจอร์ไรเซอร์ เซรั่ม",
    #     # "镜头视频": [{"file_token": file_token, "name": "镜头001.mp4"}]
    # })
    
    # 5. 批量更新
    # updates = [
    #     {"record_id": "rec123", "fields": {"产品名称": "新产品名"}},
    #     {"record_id": "rec456", "fields": {"产品名称": "另一个产品"}}
    # ]
    # feishu.batch_update_records(updates)
    
    print("✅ 飞书工具使用示例完成")


if __name__ == "__main__":
    demo_usage()
