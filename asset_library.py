import os
import json
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from google import genai
import httpx
import ssl
import time
import random


# Initialize env (for GEMINI_API_KEY)
load_dotenv()


ASSETS_DIR = "assets"
METADATA_PATH = os.path.join(ASSETS_DIR, "metadata.json")
EMBEDDING_MODEL = "models/text-embedding-004"


def _ensure_store() -> None:
    if not os.path.isdir(ASSETS_DIR):
        os.makedirs(ASSETS_DIR, exist_ok=True)
    if not os.path.exists(METADATA_PATH):
        with open(METADATA_PATH, "w", encoding="utf-8") as f:
            json.dump({"assets": []}, f, ensure_ascii=False, indent=2)


def _read_store() -> Dict[str, Any]:
    _ensure_store()
    with open(METADATA_PATH, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {"assets": []}


def _write_store(payload: Dict[str, Any]) -> None:
    _ensure_store()
    with open(METADATA_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def load_assets() -> List[Dict[str, Any]]:
    return _read_store().get("assets", [])


def _extract_embedding_values(resp: Any) -> Optional[List[float]]:
    # Try new-style response objects
    try:
        # common: resp.embedding.values (GenAI SDK)
        emb = getattr(resp, "embedding", None)
        if emb is not None:
            vals = getattr(emb, "values", None)
            if isinstance(vals, list) and vals and isinstance(vals[0], (int, float)):
                return vals
            if isinstance(emb, dict):
                vals = emb.get("values") or emb.get("value")
                if isinstance(vals, list):
                    return vals
        # sometimes: resp.embeddings[0].values
        embs = getattr(resp, "embeddings", None) or getattr(resp, "data", None)
        if isinstance(embs, list) and embs:
            first = embs[0]
            vals = getattr(first, "values", None)
            if isinstance(vals, list):
                return vals
            if isinstance(first, dict):
                vals = first.get("values")
                if isinstance(vals, list):
                    return vals
    except Exception:
        pass

    # Try dict-style responses
    if isinstance(resp, dict):
        if "embedding" in resp:
            emb = resp["embedding"]
            if isinstance(emb, dict):
                values = emb.get("values") or emb.get("value")
                if isinstance(values, list):
                    return values
        # Common older layout
        if "data" in resp and isinstance(resp["data"], list) and resp["data"]:
            maybe = resp["data"][0]
            if isinstance(maybe, dict) and "embedding" in maybe:
                emb = maybe["embedding"]
                if isinstance(emb, dict) and "values" in emb:
                    return emb["values"]
    return None


def compute_embedding(text: str) -> Optional[List[float]]:
    """
    Compute text embedding using the latest google-genai client.
    Tries the new client.models.embed_content first; falls back to legacy helper if needed.
    """
    if not text:
        return None

    client = genai.Client()

    # Try new-style API with retries
    attempt = 0
    while attempt < 3:
        try:
            resp = client.models.embed_content(model=EMBEDDING_MODEL, contents=text)
            values = _extract_embedding_values(resp)
            if values:
                return values
            break
        except (httpx.HTTPError, ssl.SSLError) as e:
            attempt += 1
            delay = 2 ** attempt + random.uniform(0, 0.5)
            print(f"[Embedding] retry {attempt}: {e} -> wait {delay:.1f}s")
            time.sleep(delay)
        except Exception as e:
            print(f"[Embedding] primary embed_content error: {e}")
            break

    # Fallback to legacy genai.embed_content if available
    try:
        import google.generativeai as legacy_genai  # type: ignore
        resp = legacy_genai.embed_content(model=EMBEDDING_MODEL, content=text)
        values = _extract_embedding_values(resp)
        if values:
            return values
    except Exception as e:
        print(f"[Embedding] legacy embed_content error: {e}")

    return None


def backfill_missing_embeddings() -> int:
    """Compute and fill embeddings for any assets without embeddings. Returns count updated."""
    store = _read_store()
    assets = store.get("assets", [])
    updated = 0
    for rec in assets:
        emb = rec.get("embedding")
        if not emb or not isinstance(emb, list):
            desc = rec.get("description") or ""
            vals = compute_embedding(desc)
            if vals:
                rec["embedding"] = vals
                updated += 1
    if updated:
        _write_store(store)
    print(f"[Embedding] backfill updated: {updated}")
    return updated


def _hms_to_seconds(hms: str) -> Optional[float]:
    try:
        hh, mm, ss = hms.split(":")
        return int(hh) * 3600 + int(mm) * 60 + float(ss)
    except Exception:
        return None


def upsert_asset(record: Dict[str, Any]) -> Dict[str, Any]:
    store = _read_store()
    assets = store.get("assets", [])

    # Assign an id if missing
    if "segment_id" not in record:
        record["segment_id"] = f"seg_{len(assets) + 1:06d}"

    # Enrich duration if possible
    if record.get("start_time") and record.get("end_time") and "duration_seconds" not in record:
        st = _hms_to_seconds(record["start_time"])
        et = _hms_to_seconds(record["end_time"])
        if st is not None and et is not None and et >= st:
            record["duration_seconds"] = round(et - st, 3)

    assets.append(record)
    store["assets"] = assets
    _write_store(store)
    return record


