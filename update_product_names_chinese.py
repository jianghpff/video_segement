#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新产品名称为中文版本
将现有的泰语产品名称改为中文显示
"""

import json
import requests
import time
from typing import List, Dict, Any
from google import genai
from dotenv import load_dotenv

load_dotenv()


class ChineseProductNameUpdater:
    def __init__(self):
        self.token_api_url = "https://feishu-token-proxy.1170731839.workers.dev/"
        self.app_token = "T68zbfXIlaHT0TsOuvNc8iEZnib"
        self.table_id = "tblg3kmG712Mw9kZ"
        self.access_token = None
        
    def get_access_token(self) -> str:
        """获取飞书访问令牌"""
        response = requests.post(self.token_api_url, timeout=30)
        response.raise_for_status()
        data = response.json()
        self.access_token = data['tenant_access_token']
        print(f"✅ 获取访问令牌成功")
        return self.access_token
    
    def extract_chinese_product_name(self, product_info: str, product_type: str) -> str:
        """使用Gemini提取中文产品名称"""
        try:
            client = genai.Client()
            
            prompt = f"""
请从以下产品信息中提取简洁的中文产品名称：

产品类型：{product_type}
原始信息：{product_info}

要求：
1. 输出简洁的中文产品名称
2. 格式：品牌名 + 产品类型（如果能识别品牌的话）
3. 去除价格、优惠、送货等营销信息
4. 如果原始信息是泰语/英语，请翻译成中文
5. 优先使用通用的产品类型名称

示例：
输入："มอยซ์เจอร์ไรเซอร์ เซรั่ม" (泰语保湿精华)
输出："保湿精华"

输入："TOP SKIN 5X CERAMIDE 精华"
输出："TOP SKIN 神经酰胺精华"

请直接输出中文产品名称，不要解释：
"""
            
            response = client.models.generate_content(
                model="models/gemini-2.5-flash",
                contents=[prompt]
            )
            
            chinese_name = response.text.strip()
            print(f"🤖 中文名称提取: '{product_info}' → '{chinese_name}'")
            return chinese_name
            
        except Exception as e:
            print(f"❌ AI提取失败: {e}，使用产品类型作为备选")
            return product_type  # 返回产品类型作为备选
    
    def get_records_with_product(self) -> List[Dict]:
        """获取包含产品的记录"""
        if not self.access_token:
            self.get_access_token()
        
        records_url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{self.app_token}/tables/{self.table_id}/records"
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        
        params = {'page_size': 500}
        
        response = requests.get(records_url, headers=headers, params=params)
        response.raise_for_status()
        result = response.json()
        
        if result['code'] != 0:
            raise Exception(f"获取记录失败: {result.get('msg')}")
        
        # 筛选包含产品的记录
        records_with_product = []
        for record in result['data']['items']:
            fields = record.get('fields', {})
            has_product = fields.get('包含产品', False)
            product_info = fields.get('产品信息', '')
            
            if has_product and product_info:
                records_with_product.append({
                    'record_id': record['record_id'],
                    'product_info': product_info,
                    'product_type': fields.get('产品类型', '未知'),
                    'shot_id': fields.get('镜头ID', 'Unknown'),
                    'current_product_name': fields.get('产品名称', '')
                })
        
        print(f"📊 找到 {len(records_with_product)} 条包含产品的记录")
        return records_with_product
    
    def update_product_name(self, record_id: str, chinese_name: str) -> bool:
        """更新单条记录的产品名称为中文"""
        try:
            if not self.access_token:
                self.get_access_token()
            
            update_url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{self.app_token}/tables/{self.table_id}/records/{record_id}"
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json; charset=utf-8'
            }
            
            data = {
                "fields": {
                    "产品名称": chinese_name
                }
            }
            
            # 使用PUT方法
            response = requests.put(update_url, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            
            if result['code'] == 0:
                print(f"✅ 记录 {record_id} 中文产品名称更新成功: '{chinese_name}'")
                return True
            else:
                print(f"❌ 记录 {record_id} 更新失败: {result.get('msg')}")
                return False
                
        except Exception as e:
            print(f"❌ 更新记录异常: {e}")
            return False
    
    def update_all_to_chinese(self):
        """将所有产品名称更新为中文"""
        print("\n🇨🇳 开始将产品名称更新为中文...")
        print("=" * 60)
        
        # 获取包含产品的记录
        records = self.get_records_with_product()
        
        if not records:
            print("❌ 未找到包含产品的记录")
            return False
        
        success_count = 0
        
        for i, record_data in enumerate(records, 1):
            print(f"\n--- 处理记录 {i}/{len(records)} ---")
            print(f"镜头ID: {record_data['shot_id']}")
            print(f"当前产品名称: {record_data['current_product_name']}")
            
            # 提取中文产品名称
            chinese_name = self.extract_chinese_product_name(
                record_data['product_info'], 
                record_data['product_type']
            )
            
            # 更新记录
            if self.update_product_name(record_data['record_id'], chinese_name):
                success_count += 1
            
            # 避免API限制
            time.sleep(1)
        
        print(f"\n🎉 中文产品名称更新完成！成功更新 {success_count}/{len(records)} 条记录")
        return success_count == len(records)


def main():
    """主函数"""
    print("🇨🇳 产品名称中文化更新器")
    print("=" * 60)
    
    updater = ChineseProductNameUpdater()
    success = updater.update_all_to_chinese()
    
    if success:
        print("\n✅ 所有产品名称已更新为中文！")
        print("💡 现在飞书表中的'产品名称'列显示为中文名称")
    else:
        print("\n⚠️ 部分更新失败，请检查日志")


if __name__ == "__main__":
    main()
