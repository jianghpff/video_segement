# ==============================================================================
# STAGE 1: MACRO ANALYSIS - SCENE DETECTION
# Goal: To divide the video into broad, narrative scenes.
# ==============================================================================

SCENE_SYSTEM_INSTRUCTION = """
你是一个专业的视频内容分析师。
你的任务是仔细观看视频，并识别出其中主要的叙事场景或主题段落，并为每个场景补充结构化元数据：
1) 是否出现产品（布尔）
2) 产品类型（精华 / 面霜 / 洗面奶 / 未知）
3) 产品相关信息（从包装、UI 贴图、字幕等可见文字中尽量提取品牌、关键词、外语文本等）
4) 画面内容（人物/服饰/背景/道具等视觉要点）
5) 人物动作（简明的动作线）
6) 特效 / 字幕（如评论气泡、“THIS!” 箭头、高亮标注等 UI/贴图元素及其含义）

要求：
- 如无法确定，使用“未知”或给出最合理的“不确定”结论，避免臆测。
- 输出必须严格符合下方 schema 的 JSON，且只能输出 JSON，不得包含其他文本。
"""

SCENE_USER_PROMPT = """
请将这个视频分解为一系列有意义、连贯的场景，并为每个场景补充以下信息：
1. `start_time`: 场景开始的时间戳，格式为 "HH:MM:SS"。
2. `end_time`: 场景结束的时间戳，格式为 "HH:MM:SS"。
3. `description`: 对该场景核心内容的简洁描述。
4. `has_product`: 该场景是否出现产品（true/false）。
5. `product_type`: 产品类型，取值限定为 ["精华", "面霜", "洗面奶", "未知"]。
6. `product_info`: 与产品相关的信息（尽量从画面可见文字中提取，包含品牌、包装文案、外语文本等）。
7. `visuals`: 画面内容（人物、服饰、背景、道具等视觉要点）。
8. `human_action`: 人物动作（简明动作线）。
9. `effects_subtitles`: 特效/字幕/贴图元素及含义（如评论气泡、“THIS!” 箭头等）。
"""

SCENE_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "scenes": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "start_time": {
                        "type": "string",
                        "description": "场景开始的时间戳，格式为 HH:MM:SS"
                    },
                    "end_time": {
                        "type": "string",
                        "description": "场景结束的时间戳，格式为 HH:MM:SS"
                    },
                    "description": {
                        "type": "string",
                        "description": "对该场景核心内容的简洁描述"
                    },
                    "has_product": {
                        "type": "boolean",
                        "description": "该场景是否出现产品"
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
                    "visuals": {
                        "type": "string",
                        "description": "画面内容摘要（人物/服饰/背景/道具等）"
                    },
                    "human_action": {
                        "type": "string",
                        "description": "人物动作（简明动作线）"
                    },
                    "effects_subtitles": {
                        "type": "string",
                        "description": "特效/字幕/贴图元素及其含义（如评论气泡、THIS! 箭头等）"
                    }
                },
                "required": [
                    "start_time", "end_time", "description",
                    "has_product", "product_type", "product_info",
                    "visuals", "human_action", "effects_subtitles"
                ]
            }
        }
    },
    "required": ["scenes"]
}


# ==============================================================================
# STAGE 2: MICRO ANALYSIS - SHOT & ACTION TAGGING
# Goal: To break down each scene into atomic shots, classifying and tagging them.
# ==============================================================================

SHOT_SYSTEM_INSTRUCTION = """
你是一位经验丰富的影视行业场记（Shot Logger）。
你的任务是逐帧观看这段视频，并识别出其中每一个独立的、有意义的视觉镜头或微小动作。
你的描述必须极其简洁，只聚焦于视觉动作本身。
你必须对每个镜头进行分类并提供相关的关键词标签。
请始终以符合所提供 schema 的 JSON 格式作为唯一输出来响应。
"""

SHOT_USER_PROMPT = """
请分析这段视频。将其分解为一系列原子化的视觉事件或镜头。

为每个镜头提供：
1. `start_time`: 镜头开始的时间戳，格式为 "HH:MM:SS"。
2. `end_time`: 镜头结束的时间戳，格式为 "HH:MM:SS"。
3. `description`: 对视觉动作的超简洁描述（例如：“镜头从左向右平移扫过产品”）。
4. `type`: 镜头的类型。对于补充性镜头，如产品特写、环境镜头或情绪反应，请使用 'B-Roll'。对于包含关键主体的主要动作，请使用 'Primary Shot'。
5. `tags`: 一个与镜头内容相关的关键词标签列表（例如：["产品特写", "快节奏", "微笑"]）。
"""

SHOT_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "shots": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
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
                        "description": "对镜头视觉内容的超简洁描述"
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
                    }
                },
                "required": ["start_time", "end_time", "description", "type", "tags"]
            }
        }
    },
    "required": ["shots"]
}
