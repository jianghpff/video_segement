# ==============================================================================
# 一次性镜头分析 - 支持多产品、3秒最低时长限制
# ==============================================================================

SINGLE_SHOT_SYSTEM_INSTRUCTION = """
你是专业的视频内容分析师和镜头切割专家。
你的任务是一次性分析整个视频，直接输出最终的镜头切割结果。

要求：
1. 结合视频画面和音频内容全面分析，识别所有出现的产品
2. 每个镜头时长必须 ≥ 3秒，≤ 10秒
3. 镜头切割要保持内容完整性，避免动作或话题被截断
4. 一个镜头可能包含多个产品，请全部识别并标注主要产品
5. 输出中文产品名称和详细的镜头元数据
6. 如果某段内容不足3秒，请与相邻内容合并形成≥3秒的镜头

请始终以符合所提供 schema 的 JSON 格式作为唯一输出来响应。
绝不要在 JSON 之外添加任何解释、介绍或总结性文本。
"""

SINGLE_SHOT_USER_PROMPT = """
请一次性分析这个视频，直接输出镜头切割结果。

为每个镜头提供：
1. `start_time`: 镜头开始时间，格式为 "HH:MM:SS"
2. `end_time`: 镜头结束时间，格式为 "HH:MM:SS"（确保时长 ≥ 3秒）
3. `description`: 镜头的简洁描述
4. `type`: 镜头类型（"Primary Shot" 或 "B-Roll"）
5. `tags`: 相关标签列表
6. `has_product`: 是否包含产品
7. `products`: 该镜头中的所有产品（数组格式）
8. `main_product_type`: 主要产品类型
9. `main_product_name`: 主要产品的中文名称
10. `visuals`: 画面视觉内容描述
11. `human_action`: 人物动作描述
12. `effects_subtitles`: 特效、字幕、UI元素描述

特别注意：
- 仔细听取音频内容，结合画面识别产品
- 确保每个镜头时长 ≥ 3秒
- 如果一个镜头有多个产品，在products数组中全部列出
- 产品名称使用中文表达
"""

SINGLE_SHOT_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "shots": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "start_time": {
                        "type": "string",
                        "description": "镜头开始时间，格式为 HH:MM:SS"
                    },
                    "end_time": {
                        "type": "string",
                        "description": "镜头结束时间，格式为 HH:MM:SS"
                    },
                    "description": {
                        "type": "string",
                        "description": "镜头的简洁描述"
                    },
                    "type": {
                        "type": "string",
                        "enum": ["Primary Shot", "B-Roll"],
                        "description": "镜头类型"
                    },
                    "tags": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "相关标签列表"
                    },
                    "has_product": {
                        "type": "boolean",
                        "description": "该镜头是否包含产品"
                    },
                    "products": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "product_type": {
                                    "type": "string",
                                    "description": "产品类型（如：精华、面霜、洗面奶）"
                                },
                                "product_name": {
                                    "type": "string", 
                                    "description": "产品的中文名称"
                                },
                                "product_info": {
                                    "type": "string",
                                    "description": "从画面和音频中识别的产品相关信息"
                                }
                            },
                            "required": ["product_type", "product_name", "product_info"]
                        },
                        "description": "该镜头中出现的所有产品"
                    },
                    "main_product_type": {
                        "type": "string", 
                        "description": "主要产品类型（如果有多个产品）"
                    },
                    "main_product_name": {
                        "type": "string",
                        "description": "主要产品的中文名称"
                    },
                    "visuals": {
                        "type": "string",
                        "description": "画面视觉内容描述（人物、服饰、背景、道具等）"
                    },
                    "human_action": {
                        "type": "string", 
                        "description": "人物动作描述"
                    },
                    "effects_subtitles": {
                        "type": "string",
                        "description": "特效、字幕、UI元素及其含义"
                    }
                },
                "required": [
                    "start_time", "end_time", "description", "type", "tags",
                    "has_product", "products", "main_product_type", "main_product_name",
                    "visuals", "human_action", "effects_subtitles"
                ]
            }
        }
    },
    "required": ["shots"]
}
