#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复飞书字段 - 确保所有多产品字段存在
"""

import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

class FeishuFieldFixer:
    def __init__(self):
        self.token_api_url = "https://feishu-token-proxy.1170731839.workers.dev/"
        self.app_token = "T68zbfXIlaHT0TsOuvNc8iEZnib"
        self.table_id = "tblg3kmG712Mw9kZ"
        self.access_token = None
        
        # 需要的新字段
        self.required_fields = {
            "产品列表": {"type": 1, "description": "JSON格式存储多个产品"},  # 文本
            "主要产品名称": {"type": 1, "description": "中文主产品名称"},  # 文本  
            "产品数量": {"type": 2, "description": "该镜头中的产品数量"}  # 数字
        }
    
    def get_access_token(self) -> str:
        """获取飞书访问令牌"""
        try:
            response = requests.get(self.token_api_url, timeout=10)
            response.raise_for_status()
            data = response.json()
            self.access_token = data.get('access_token')
            print(f"✅ 获取访问令牌成功")
            return self.access_token
        except Exception as e:
            print(f"❌ 获取访问令牌失败: {e}")
            return None
    
    def get_existing_fields(self):
        """获取表格现有字段"""
        if not self.access_token:
            self.get_access_token()
        
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{self.app_token}/tables/{self.table_id}/fields"
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json; charset=utf-8'
        }
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            result = response.json()
            
            fields = result.get('data', {}).get('items', [])
            field_names = [field.get('field_name', '') for field in fields]
            
            print(f"📋 现有字段 ({len(field_names)} 个):")
            for name in sorted(field_names):
                print(f"  - {name}")
            
            return field_names
            
        except Exception as e:
            print(f"❌ 获取字段失败: {e}")
            return []
    
    def create_field(self, field_name: str, field_config: dict):
        """创建新字段"""
        if not self.access_token:
            self.get_access_token()
        
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{self.app_token}/tables/{self.table_id}/fields"
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json; charset=utf-8'
        }
        
        data = {
            "field_name": field_name,
            "type": field_config["type"],
            "description": {
                "text": field_config["description"]
            }
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            
            field_id = result.get('data', {}).get('field', {}).get('field_id')
            print(f"✅ 字段创建成功: {field_name} -> {field_id}")
            time.sleep(1)  # 避免API限流
            return True
            
        except Exception as e:
            print(f"❌ 字段创建失败 {field_name}: {e}")
            return False
    
    def fix_all_fields(self):
        """修复所有缺失字段"""
        print("🔧 开始修复飞书表格字段...")
        
        # 获取现有字段
        existing_fields = self.get_existing_fields()
        
        # 检查缺失字段
        missing_fields = []
        for field_name in self.required_fields.keys():
            if field_name not in existing_fields:
                missing_fields.append(field_name)
        
        if not missing_fields:
            print("✅ 所有字段都已存在，无需修复")
            return True
        
        print(f"\n🔍 发现 {len(missing_fields)} 个缺失字段:")
        for field_name in missing_fields:
            print(f"  - {field_name}")
        
        # 创建缺失字段
        success_count = 0
        for field_name in missing_fields:
            print(f"\n📝 正在创建字段: {field_name}")
            if self.create_field(field_name, self.required_fields[field_name]):
                success_count += 1
            else:
                print(f"❌ 创建字段失败: {field_name}")
        
        print(f"\n📊 字段修复结果: {success_count}/{len(missing_fields)} 成功")
        
        if success_count == len(missing_fields):
            print("✅ 所有字段修复完成！")
            return True
        else:
            print("❌ 部分字段修复失败")
            return False

def main():
    fixer = FeishuFieldFixer()
    fixer.fix_all_fields()

if __name__ == "__main__":
    main()
