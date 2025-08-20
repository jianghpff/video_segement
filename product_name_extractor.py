#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
产品名称提取和飞书表更新模块
方案一：在现有表基础上新增"产品名称"字段并批量更新
"""

import json
import requests
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
from google import genai
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


class ProductNameExtractor:
    def __init__(self):
        self.token_api_url = "https://feishu-token-proxy.1170731839.workers.dev/"
        self.app_token = "T68zbfXIlaHT0TsOuvNc8iEZnib"
        self.table_id = "tblg3kmG712Mw9kZ"
        self.access_token = None
        
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
    
    def add_product_name_field(self) -> str:
        """在飞书表中新增'产品名称'字段"""
        try:
            if not self.access_token:
                self.get_access_token()
            
            fields_url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{self.app_token}/tables/{self.table_id}/fields"
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json; charset=utf-8'
            }
            
            # 先检查字段是否已存在
            response = requests.get(fields_url, headers=headers)
            response.raise_for_status()
            result = response.json()
            
            if result['code'] != 0:
                raise Exception(f"获取字段失败: {result.get('msg')}")
            
            existing_fields = {field['field_name']: field['field_id'] for field in result['data']['items']}
            
            if '产品名称' in existing_fields:
                print(f"✅ '产品名称'字段已存在，字段ID: {existing_fields['产品名称']}")
                return existing_fields['产品名称']
            
            # 创建新字段
            create_data = {
                "field_name": "产品名称",
                "type": 1,  # 多行文本
                "ui_type": "Text"
            }
            
            print("📝 正在创建'产品名称'字段...")
            response = requests.post(fields_url, headers=headers, json=create_data)
            response.raise_for_status()
            result = response.json()
            
            if result['code'] == 0:
                field_id = result['data']['field']['field_id']
                print(f"✅ 成功创建'产品名称'字段，ID: {field_id}")
                return field_id
            else:
                raise Exception(f"创建字段失败: {result.get('msg')}")
                
        except Exception as e:
            print(f"❌ 创建字段异常: {e}")
            return None
    
    def extract_product_name_with_ai(self, product_info: str, product_type: str) -> str:
        """使用Gemini从产品信息中提取纯净的产品名称"""
        try:
            client = genai.Client()
            
            prompt = f"""
请从以下产品信息中提取纯净的产品名称（品牌名+产品类型），去除价格、促销信息等：

产品类型：{product_type}
原始信息：{product_info}

要求：
1. 只提取产品的核心名称，如品牌名+产品类型
2. 保留原语言（泰语/英语等）
3. 去除价格、优惠、送货等营销信息
4. 如果无法提取，返回产品类型即可
5. 输出格式：直接输出产品名称，不要解释

示例：
输入："TOP SKIN 5X CERAMIDE 4D HA CENTELLA PANTHENOL 149泰铢包邮"
输出："TOP SKIN 5X CERAMIDE 精华"
"""
            
            response = client.models.generate_content(
                model="models/gemini-2.5-flash",
                contents=[prompt]
            )
            
            extracted_name = response.text.strip()
            print(f"🤖 AI提取结果: '{product_info}' → '{extracted_name}'")
            return extracted_name
            
        except Exception as e:
            print(f"❌ AI提取失败: {e}，使用产品类型作为备选")
            return product_type
    
    def get_all_records(self) -> List[Dict]:
        """获取表中所有记录"""
        try:
            if not self.access_token:
                self.get_access_token()
            
            records_url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{self.app_token}/tables/{self.table_id}/records"
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json'
            }
            
            params = {
                'page_size': 500  # 获取所有记录
            }
            
            response = requests.get(records_url, headers=headers, params=params)
            response.raise_for_status()
            result = response.json()
            
            if result['code'] != 0:
                raise Exception(f"获取记录失败: {result.get('msg')}")
            
            records = result['data']['items']
            print(f"📊 获取到 {len(records)} 条记录")
            return records
            
        except Exception as e:
            print(f"❌ 获取记录失败: {e}")
            return []
    
    def update_record_product_name(self, record_id: str, product_name: str, product_name_field_id: str) -> bool:
        """更新单条记录的产品名称"""
        try:
            if not self.access_token:
                self.get_access_token()
            
            update_url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{self.app_token}/tables/{self.table_id}/records/{record_id}"
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json; charset=utf-8'
            }
            
            # 使用字段名称（更稳定）
            data = {
                "fields": {
                    "产品名称": product_name
                }
            }
            
            response = requests.put(update_url, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            
            if result['code'] == 0:
                print(f"✅ 记录 {record_id} 产品名称更新成功: '{product_name}'")
                return True
            else:
                print(f"❌ 记录 {record_id} 更新失败: {result.get('msg')}")
                return False
                
        except Exception as e:
            print(f"❌ 更新记录异常: {e}")
            return False
    
    def process_all_records(self):
        """处理所有记录：提取产品名称并更新"""
        print("\n🚀 开始批量提取产品名称并更新飞书表...")
        
        # 1. 添加产品名称字段
        print("\n📝 步骤1: 确保'产品名称'字段存在")
        product_name_field_id = self.add_product_name_field()
        if not product_name_field_id:
            print("❌ 无法创建或获取'产品名称'字段，停止处理")
            return False
        
        # 2. 获取所有记录
        print("\n📊 步骤2: 获取现有记录")
        records = self.get_all_records()
        if not records:
            print("❌ 未获取到任何记录")
            return False
        
        # 3. 筛选需要处理的记录（包含产品的镜头）
        records_to_process = []
        for record in records:
            fields = record.get('fields', {})
            # 检查是否包含产品
            has_product = fields.get('包含产品', False)
            product_info = fields.get('产品信息', '')
            product_type = fields.get('产品类型', '')
            
            if has_product and product_info:
                records_to_process.append({
                    'record_id': record['record_id'],
                    'product_info': product_info,
                    'product_type': product_type,
                    'shot_id': fields.get('镜头ID', 'Unknown')
                })
        
        print(f"📋 找到 {len(records_to_process)} 条包含产品的记录需要处理")
        
        # 4. 批量处理
        print("\n🤖 步骤3: AI提取产品名称并更新")
        success_count = 0
        
        for i, record_data in enumerate(records_to_process, 1):
            print(f"\n--- 处理记录 {i}/{len(records_to_process)} ---")
            print(f"镜头ID: {record_data['shot_id']}")
            
            # AI提取产品名称
            product_name = self.extract_product_name_with_ai(
                record_data['product_info'], 
                record_data['product_type']
            )
            
            # 更新记录
            if self.update_record_product_name(
                record_data['record_id'], 
                product_name, 
                product_name_field_id
            ):
                success_count += 1
            
            # 避免API限制
            time.sleep(1)
        
        print(f"\n🎉 批量更新完成！成功更新 {success_count}/{len(records_to_process)} 条记录")
        return success_count == len(records_to_process)


def main():
    """主函数"""
    print("🔧 产品名称提取器 - 方案一实施")
    print("=" * 60)
    
    extractor = ProductNameExtractor()
    success = extractor.process_all_records()
    
    if success:
        print("\n✅ 所有产品名称提取和更新完成！")
        print("💡 现在飞书表中有独立的'产品名称'列，便于筛选和统计")
    else:
        print("\n⚠️ 部分处理失败，请检查日志")


if __name__ == "__main__":
    main()
