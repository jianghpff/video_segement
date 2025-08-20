# 飞书多维表操作规则手册

## 核心规则 (必须遵守)

### 1. API方法选择
- ✅ **更新记录**：使用 `PUT` 方法，不是 `PATCH`
- ✅ **创建记录**：使用 `POST` 方法
- ✅ **查询记录**：使用 `GET` 方法
- ❌ **错误示例**：使用 `PATCH` 更新会返回 404

### 2. 字段操作最佳实践
- ✅ **推荐**：使用字段名称，如 `"产品名称"`
- ⚠️ **可选**：使用字段ID，如 `"fldrN1pMnu"`，但不够稳定
- ✅ **字段创建**：先检查是否存在，避免重复创建

### 3. API配置 (项目专用)
```python
APP_TOKEN = "T68zbfXIlaHT0TsOuvNc8iEZnib"
TABLE_ID = "tblg3kmG712Mw9kZ"
TOKEN_API = "https://feishu-token-proxy.1170731839.workers.dev/"
```

## 标准操作流程

### 获取访问令牌
```python
response = requests.post(TOKEN_API_URL, timeout=30)
token = response.json()['tenant_access_token']
```

### 更新记录 (关键！)
```python
# 正确方法：PUT
url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records/{record_id}"
data = {"fields": {"产品名称": "新值"}}
response = requests.put(url, headers=headers, json=data)  # 注意：PUT不是PATCH
```

### 创建字段
```python
# 字段类型映射
FIELD_TYPES = {
    "text": {"type": 1, "ui_type": "Text"},
    "number": {"type": 2, "ui_type": "Number"}, 
    "checkbox": {"type": 7, "ui_type": "Checkbox"},
    "attachment": {"type": 17, "ui_type": "Attachment"}
}
```

### 文件上传
```python
files = {
    'file_name': (None, filename),
    'parent_type': (None, 'bitable_file'),  # 关键参数
    'parent_node': (None, app_token),
    'size': (None, str(file_size)),
    'file': (filename, file_content, 'video/mp4')
}
```

## 错误处理规则

### 常见错误码速查
- **404**：方法错误（使用PUT不是PATCH）或记录不存在
- **401**：令牌过期，重新获取
- **403**：权限不足，检查应用配置
- **429**：限流，增加请求间隔

### 重试机制
```python
for attempt in range(3):
    try:
        # API调用
        break
    except Exception as e:
        if attempt < 2:
            time.sleep((attempt + 1) * 2)  # 指数退避
        else:
            raise
```

### 批量操作防限流
```python
for i, operation in enumerate(operations):
    # 执行操作
    if i < len(operations) - 1:
        time.sleep(1)  # 每次操作间隔1秒
```

## 字段设计标准

### 视频镜头表标准字段
```
原视频文件名 (text)
镜头序号 (number)
镜头ID (text)
开始时间 (text)
结束时间 (text)
镜头时长 (text)
镜头描述 (text)
包含产品 (checkbox)
产品信息 (text) - 原始信息
产品名称 (text) - AI提取的纯净名称
视觉描述 (text)
人物动作 (text)
特效字幕 (text)
镜头视频 (attachment)
处理时间 (text)
AI分析质量 (number)
```

## 性能优化规则

1. **令牌缓存**：检查过期时间，避免频繁申请
2. **批量操作**：合并多个字段更新到一次API调用
3. **错误恢复**：网络错误自动重试，业务错误记录日志
4. **内存管理**：大文件分片上传，避免内存溢出

## 调试技巧

### 验证API调用
```python
print(f"URL: {url}")
print(f"Method: {method}")
print(f"Headers: {headers}")
print(f"Data: {data}")
print(f"Response: {response.status_code} - {response.text}")
```

### 记录操作日志
```python
def log_operation(operation, success, details=""):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "✅" if success else "❌"
    print(f"[{timestamp}] {status} {operation} - {details}")
```

---

**记住**：遇到404错误，第一反应检查是否使用了PUT方法！
