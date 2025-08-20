#!/usr/bin/env python3
"""调试飞书记录更新问题"""

import requests
import json

# 飞书配置
TOKEN_API_URL = "https://feishu-token-proxy.1170731839.workers.dev/"
APP_TOKEN = "T68zbfXIlaHT0TsOuvNc8iEZnib"
TABLE_ID = "tblg3kmG712Mw9kZ"

def get_access_token():
    response = requests.post(TOKEN_API_URL, timeout=30)
    response.raise_for_status()
    data = response.json()
    return data['tenant_access_token']

def get_all_records(access_token):
    records_url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    params = {'page_size': 500}
    response = requests.get(records_url, headers=headers, params=params)
    response.raise_for_status()
    result = response.json()
    
    return result['data']['items']

def test_update_record(access_token, record_id):
    """测试更新单个记录"""
    # 方法1: 使用PUT而不是PATCH
    update_url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records/{record_id}"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json; charset=utf-8'
    }
    
    # 测试使用字段名称
    data = {
        "fields": {
            "产品名称": "测试产品名称"
        }
    }
    
    print(f"   使用URL: {update_url}")
    
    # 先尝试PUT
    response = requests.put(update_url, headers=headers, json=data)
    return response

def main():
    print("🔍 调试飞书记录更新问题")
    print("=" * 50)
    
    # 获取访问令牌
    print("1. 获取访问令牌...")
    token = get_access_token()
    print(f"✅ 获取成功: {token[:20]}...")
    
    # 获取所有记录
    print("\n2. 获取所有记录...")
    records = get_all_records(token)
    print(f"✅ 找到 {len(records)} 条记录")
    
    # 显示记录详情
    print("\n3. 记录详情:")
    for i, record in enumerate(records, 1):
        record_id = record['record_id']
        fields = record.get('fields', {})
        shot_id = fields.get('镜头ID', 'Unknown')
        has_product = fields.get('包含产品', False)
        
        print(f"  {i}. ID: {record_id}")
        print(f"     镜头: {shot_id}")
        print(f"     有产品: {has_product}")
        print()
    
    # 测试更新第一条记录
    if records:
        print("4. 测试更新第一条记录...")
        test_record = records[0]
        test_id = test_record['record_id']
        print(f"   测试记录ID: {test_id}")
        
        try:
            response = test_update_record(token, test_id)
            print(f"   状态码: {response.status_code}")
            print(f"   响应: {response.text}")
            
            if response.status_code == 200:
                print("   ✅ 更新成功!")
            else:
                print(f"   ❌ 更新失败: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ 请求异常: {e}")

if __name__ == "__main__":
    main()
