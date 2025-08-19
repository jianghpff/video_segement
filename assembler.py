import os
import json
import re
import subprocess
from typing import List, Dict, Any, Tuple

from dotenv import load_dotenv
from google import genai

from asset_library import load_assets, compute_embedding
from director import search_assets_by_brief
from producer import concat_shots, mux_voiceover, synthesize_tts_thai


load_dotenv()


SCRIPT_MODEL = "models/gemini-2.5-pro"


def generate_full_script_th(brief: str) -> str:
    client = genai.Client()
    sys_inst = (
        "你是资深广告文案撰写者。请用自然口语化的泰语，写一段完整的旁白脚本。"
        "要求：\n"
        "1) 语速自然，不要刻意放慢或拖长；\n"
        "2) 情绪积极真诚；\n"
        "3) 不要超过 120 字（泰语）。"
    )
    resp = client.models.generate_content(
        model=SCRIPT_MODEL,
        contents=["用泰语写一段旁白脚本：\n" + brief],
        config={"system_instruction": sys_inst},
    )
    txt = resp.text.strip()
    # 约束长度，避免 TTS 过长导致请求不稳定
    if len(txt) > 220:
        txt = txt[:220].strip()
    return txt


def detect_silence_segments(wav_path: str, noise_db: int = -35, min_silence: float = 0.25) -> List[Tuple[float, float]]:
    """
    Return non-silence segments [(start, end), ...] covering the whole audio.
    """
    cmd = [
        "ffmpeg", "-hide_banner", "-nostats", "-i", wav_path,
        "-af", f"silencedetect=noise={noise_db}dB:d={min_silence}",
        "-f", "null", "-"
    ]
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stderr = proc.stderr
    # Parse silence_start/end
    starts = []
    ends = []
    for line in stderr.splitlines():
        m1 = re.search(r"silence_start: (\d+\.?\d*)", line)
        if m1:
            starts.append(float(m1.group(1)))
        m2 = re.search(r"silence_end: (\d+\.?\d*)", line)
        if m2:
            ends.append(float(m2.group(1)))
    duration = _probe_duration_seconds_ffprobe(wav_path)
    # Build non-silence intervals from silence boundaries
    segments: List[Tuple[float, float]] = []
    # Merge starts/ends into pairs
    pairs: List[Tuple[float, float]] = []
    # Align arrays lengths
    # If logs begin with silence_end, treat as no leading silence
    # We simply step through stderr and reconstruct pairs in order
    current = 0.0
    si = 0
    ei = 0
    lines = stderr.splitlines()
    for line in lines:
        m1 = re.search(r"silence_start: (\d+\.?\d*)", line)
        m2 = re.search(r"silence_end: (\d+\.?\d*)", line)
        if m1:
            s = float(m1.group(1))
            if s > current:
                segments.append((current, s))
            current = s
        elif m2:
            e = float(m2.group(1))
            current = e
    if current < duration:
        segments.append((current, duration))
    # Fallback: if no starts/ends found, one segment full
    if not segments:
        segments = [(0.0, duration)]
    # Merge very short gaps
    merged = []
    for st, ed in segments:
        if ed - st <= 0.05:
            continue
        merged.append((max(0.0, st), min(duration, ed)))
    return merged


def _probe_duration_seconds_ffprobe(path: str) -> float:
    try:
        cmd = [
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", path
        ]
        out = subprocess.check_output(cmd, text=True).strip()
        return float(out)
    except Exception:
        return 0.0


def split_text_by_durations(text: str, segments: List[Tuple[float, float]]) -> List[str]:
    total_chars = len(text)
    total_secs = sum(max(0.0, ed - st) for st, ed in segments) or 1.0
    targets = [max(1, round(total_chars * (ed - st) / total_secs)) for st, ed in segments]
    diff = total_chars - sum(targets)
    for i in range(abs(diff)):
        idx = i % len(targets)
        targets[idx] += 1 if diff > 0 else -1
    parts = []
    i = 0
    for t in targets:
        parts.append(text[i:i + t])
        i += t
    if i < total_chars and parts:
        parts[-1] = parts[-1] + text[i:]
    return [p.strip() for p in parts]


def _diversify_by_source(cands: List[Dict[str, Any]], max_ratio: float) -> List[Dict[str, Any]]:
    # limit any single source_video to at most max_ratio fraction of picks
    from collections import defaultdict
    total = len(cands) or 1
    per_src_max = max(1, int(total * max_ratio))
    src_count = defaultdict(int)
    out = []
    for r in cands:
        src = r.get("source_video") or ""
        if src_count[src] < per_src_max:
            out.append(r)
            src_count[src] += 1
    return out


def select_shots_for_segment(query_text: str, target_seconds: float, top_k: int = 20, max_single_shot: float = 3.0) -> List[Dict[str, Any]]:
    assets = search_assets_by_brief(query_text, top_k=top_k)
    # 多样性：限制同源占比、并打散
    assets = _diversify_by_source(assets, max_ratio=0.5)
    picked: List[Dict[str, Any]] = []
    acc = 0.0
    for rec in assets:
        dur = float(rec.get("duration_seconds") or 0)
        if dur <= 0:
            continue
        use = min(dur, max_single_shot)
        if acc + dur > target_seconds:
            use = max(0.0, min(max_single_shot, target_seconds - acc))
        if use <= 0:
            break
        picked.append({
            "segment_path": rec["segment_path"],
            "use_seconds": use,
            "source_video": rec.get("source_video")
        })
        acc += use
        if acc >= target_seconds - 1e-3:
            break
    return picked


def build_storyboard_for_audio_segments(text_segments: List[str], time_segments: List[Tuple[float, float]]) -> List[Dict[str, Any]]:
    storyboard: List[Dict[str, Any]] = []
    for txt, (st, ed) in zip(text_segments, time_segments):
        T = max(0.0, ed - st)
        picks = select_shots_for_segment(txt, T, top_k=30)
        storyboard.extend(picks)
    return storyboard


def assemble_from_brief(brief: str, output_dir: str) -> str:
    os.makedirs(output_dir, exist_ok=True)
    work_dir = os.path.join(output_dir, "_work")
    if os.path.isdir(work_dir):
        # clean
        for root, dirs, files in os.walk(work_dir, topdown=False):
            for name in files:
                try:
                    os.remove(os.path.join(root, name))
                except Exception:
                    pass
    os.makedirs(work_dir, exist_ok=True)

    # 1) Script & full TTS (Thai)
    script = generate_full_script_th(brief)
    tts_wav = os.path.join(work_dir, "full_th.wav")
    synthesize_tts_thai(script, tts_wav, voice_name="Kore")

    # 2) Silence detection → segments
    dur = _probe_duration_seconds_ffprobe(tts_wav)
    segs = detect_silence_segments(tts_wav, noise_db=-32, min_silence=0.25)
    # 兜底：至少切成 3 段，若检测不到静音则平均切分
    if not segs or len(segs) < 3:
        parts = 3
        chunk = dur / parts if parts > 0 else dur
        segs = [(i * chunk, (i + 1) * chunk) for i in range(parts)]
    segments = segs
    # 3) Split text according to durations
    text_parts = split_text_by_durations(script, segments)

    # 4) Build storyboard by semantic match with assets
    storyboard = build_storyboard_for_audio_segments(text_parts, segments)

    # 5) Cut video to exact per-shot seconds and concat
    concat_video = os.path.join(work_dir, "video_concat.mp4")
    concat_shots(storyboard, concat_video, work_dir, override_seconds=[s['use_seconds'] for s in storyboard])

    # 6) Mux final
    final_path = os.path.join(output_dir, "final_th_audio_first.mp4")
    mux_voiceover(concat_video, tts_wav, final_path, mute_original=True)
    with open(os.path.join(output_dir, "plan_used.json"), "w", encoding="utf-8") as f:
        json.dump({"brief": brief, "script": script, "storyboard": storyboard}, f, ensure_ascii=False, indent=2)
    return final_path


if __name__ == "__main__":
    brief = "做一个泰语短视频，自然语速口语化，强调精华清爽易吸收与使用后光泽感。"
    out = assemble_from_brief(brief, output_dir="final_output")
    print(out)


