import os
import json
from typing import List, Dict, Any

import numpy as np
from dotenv import load_dotenv
from google import genai

from asset_library import load_assets, compute_embedding


load_dotenv()

DIRECTOR_MODEL = "models/gemini-2.5-pro"


def _cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    if a.size == 0 or b.size == 0:
        return 0.0
    denom = (np.linalg.norm(a) * np.linalg.norm(b))
    if denom == 0:
        return 0.0
    return float(np.dot(a, b) / denom)


def search_assets_by_brief(brief: str, top_k: int = 12) -> List[Dict[str, Any]]:
    assets = load_assets()
    if not assets:
        return []
    query_emb = compute_embedding(brief) or []
    query_vec = np.array(query_emb, dtype=np.float32)

    scored: List[tuple[float, Dict[str, Any]]] = []
    for rec in assets:
        emb = np.array(rec.get("embedding", []), dtype=np.float32)
        score = _cosine_similarity(query_vec, emb)
        scored.append((score, rec))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [rec for score, rec in scored[:top_k]]


def plan_storyboard_and_script(brief: str, candidates: List[Dict[str, Any]], language: str = "th") -> Dict[str, Any]:
    """
    Use Gemini to generate a storyboard (ordered shot list) and a voiceover script
    given the creative brief and candidate assets from the library.
    """
    client = genai.Client()

    examples = [
        {
            "segment_path": c.get("segment_path"),
            "description": c.get("description"),
            "type": c.get("type"),
            "tags": c.get("tags", []),
            "duration_seconds": c.get("duration_seconds"),
        }
        for c in candidates
    ]

    lang_hint = "泰语" if language == "th" else ("中文" if language in ("zh", "zh-cn", "zh-hans") else language)
    system_instruction = (
        "你是资深广告片导演。请根据给定的候选镜头，生成：\n"
        "1) 有顺序的镜头清单（每项包含 segment_path 与建议使用时长秒数）\n"
        f"2) 一段完整的{lang_hint}旁白脚本（时长与镜头总时长匹配，语气自然口语化）。\n"
        "不要输出多余解释，只输出 JSON。"
    )

    response = client.models.generate_content(
        model=DIRECTOR_MODEL,
        contents=[
            "创作目标:\n" + brief + "\n\n候选镜头(示例):\n" + json.dumps(examples, ensure_ascii=False, indent=2)
        ],
        config={
            "response_mime_type": "application/json",
            "response_schema": {
                "type": "object",
                "properties": {
                    "storyboard": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "segment_path": {"type": "string"},
                                "use_seconds": {"type": "number"}
                            },
                            "required": ["segment_path", "use_seconds"]
                        }
                    },
                    "voiceover_script": {"type": "string"}
                },
                "required": ["storyboard", "voiceover_script"]
            },
            "system_instruction": system_instruction,
        },
    )

    try:
        return json.loads(response.text)
    except Exception:
        return {"storyboard": [], "voiceover_script": ""}


if __name__ == "__main__":
    # Demo brief
    brief = "做一个15-25秒的小红书风格种草视频，突出精华‘清爽易吸收’与‘使用后光泽感’，语气真诚自然。"
    top = search_assets_by_brief(brief, top_k=12)
    plan = plan_storyboard_and_script(brief, top)
    print(json.dumps(plan, ensure_ascii=False, indent=2))


