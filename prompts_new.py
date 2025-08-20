# ==============================================================================
# 一体化视频分析 - 丰富镜头分析
# Goal: 一次性完成镜头切分，同时包含丰富的场景级元数据
# ==============================================================================

ENHANCED_SHOT_SYSTEM_INSTRUCTION = """
你是一个专业的视频内容分析师和影视场记，擅长精确的镜头分割。

🎬 核心任务：将视频分解为5-10个独立的镜头片段，绝不能将整个视频当作一个镜头！

镜头分割原则：
- 每当人物动作改变时，创建新镜头（如：举起产品、打开盖子、展示内容、闻味道等）
- 每当产品展示角度变化时，创建新镜头
- 每当画面重点转移时，创建新镜头
- 典型镜头长度：3-15秒

对于每个镜头，你需要提供：
1) 精确的时间范围（秒级精度）
2) 该镜头中的具体视觉动作
3) 镜头类型和相关标签
4) 产品相关信息（品牌、类型等）
5) 视觉要素（人物、服饰、背景等）
6) 人物在该镜头中的具体动作
7) 特效、字幕、UI元素等

要求：
- 必须产生5-10个镜头，不能少于5个
- 镜头时间不能重叠，要连续覆盖整个视频
- 每个镜头要有明确的视觉变化点
- 输出必须是严格的JSON格式，不包含其他文本
"""

ENHANCED_SHOT_USER_PROMPT = """
请仔细观看这个视频，将其分解为多个精确的镜头片段。每个镜头应该代表一个独立的视觉动作或事件。

🔥 重要：请将视频切分为5-10个具体的镜头片段，不要将整个视频当作一个镜头！

镜头切分原则：
- 当人物动作发生变化时（如：拿起产品 → 打开盖子 → 展示内容 → 闻味道 → 微笑推荐）
- 当产品展示角度改变时
- 当画面焦点转移时
- 每个镜头通常持续3-15秒

为每个镜头提供详细信息：

镜头基础信息：
1. `start_time`: 镜头开始的精确时间戳，格式为 "HH:MM:SS"
2. `end_time`: 镜头结束的精确时间戳，格式为 "HH:MM:SS"
3. `description`: 对该镜头中具体视觉动作的简洁描述
4. `type`: 镜头类型 ["Primary Shot", "B-Roll"]
5. `tags`: 相关关键词标签列表

产品相关信息：
6. `has_product`: 该镜头是否出现产品 (true/false)
7. `product_type`: 产品类型 ["精华", "面霜", "洗面奶", "未知"]
8. `product_info`: 从画面中可见的产品相关信息（品牌、包装文案、外语文本等）

视觉内容分析：
9. `visuals`: 画面内容摘要（人物、服饰、背景、道具等视觉要点）
10. `human_action`: 在该镜头中人物的具体动作和表情
11. `effects_subtitles`: 特效、字幕、贴图元素及其含义（如评论气泡、箭头等）

示例分割（44秒视频）：
- 镜头1: 00:00:00-00:00:08 女士手持产品对镜头介绍
- 镜头2: 00:00:08-00:00:15 女士打开产品盖子
- 镜头3: 00:00:15-00:00:25 女士展示产品内部膏体
- 镜头4: 00:00:25-00:00:32 女士将产品凑近鼻子闻
- 镜头5: 00:00:32-00:00:44 女士微笑继续推荐

请按此模式详细分割视频！
"""

ENHANCED_SHOT_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "shots": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    # 镜头基础信息
                    "start_time": {
                        "type": "string",
                        "description": "镜头开始的时间戳，格式为 HH:MM:SS"
                    },
                    "end_time": {
                        "type": "string",
                        "description": "镜头结束的时间戳，格式为 HH:MM:SS"
                    },
                    "description": {
                        "type": "string",
                        "description": "对镜头视觉内容和动作的简洁描述"
                    },
                    "type": {
                        "type": "string",
                        "enum": ["Primary Shot", "B-Roll"],
                        "description": "镜头的分类"
                    },
                    "tags": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "相关关键词标签的列表"
                    },
                    
                    # 产品相关信息
                    "has_product": {
                        "type": "boolean",
                        "description": "该镜头是否出现产品"
                    },
                    "product_type": {
                        "type": "string",
                        "enum": ["精华", "面霜", "洗面奶", "未知"],
                        "description": "产品类型"
                    },
                    "product_info": {
                        "type": "string",
                        "description": "从画面中可见的与产品相关的信息（品牌、包装文案、外语文本等）"
                    },
                    
                    # 视觉内容分析
                    "visuals": {
                        "type": "string",
                        "description": "画面内容摘要（人物/服饰/背景/道具等）"
                    },
                    "human_action": {
                        "type": "string",
                        "description": "人物动作和表情描述"
                    },
                    "effects_subtitles": {
                        "type": "string",
                        "description": "特效/字幕/贴图元素及其含义（如评论气泡、箭头等）"
                    }
                },
                "required": [
                    "start_time", "end_time", "description", "type", "tags",
                    "has_product", "product_type", "product_info",
                    "visuals", "human_action", "effects_subtitles"
                ]
            }
        }
    },
    "required": ["shots"]
}
