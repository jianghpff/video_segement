import os
import json
import shutil
import base64
import wave
import re
from typing import List, Dict, Any

from dotenv import load_dotenv
import ffmpeg
from google import genai
from google.genai import types
import httpx
import ssl
import time
import random


load_dotenv()


def _save_wave(filename: str, pcm_bytes: bytes, channels: int = 1, rate: int = 24000, sample_width: int = 2) -> str:
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm_bytes)
    print(f"[TTS] 保存 WAV: {filename}")
    return filename


def _tts_generate_with_retry(client: genai.Client, text: str, voice_name: str, max_retries: int = 4):
    attempt = 0
    while True:
        try:
            return client.models.generate_content(
                model="gemini-2.5-flash-preview-tts",
                contents=text,
                config=types.GenerateContentConfig(
                    response_modalities=["AUDIO"],
                    speech_config=types.SpeechConfig(
                        voice_config=types.VoiceConfig(
                            prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name=voice_name)
                        )
                    ),
                ),
            )
        except (httpx.HTTPError, ssl.SSLError) as e:
            attempt += 1
            if attempt > max_retries:
                raise
            delay = 2 ** attempt + random.uniform(0, 0.5)
            print(f"[TTS] 网络波动，第{attempt}次重试：{e}，{delay:.1f}s 后重试...")
            time.sleep(delay)


def _split_text_for_tts(text: str, max_len: int = 180) -> List[str]:
    if len(text) <= max_len:
        return [text]
    # 按标点优先切分，再按长度兜底
    parts: List[str] = []
    cur = ""
    for ch in text:
        cur += ch
        if len(cur) >= max_len or ch in ".。!?！？\n":
            parts.append(cur.strip())
            cur = ""
    if cur.strip():
        parts.append(cur.strip())
    return parts


def synthesize_tts_thai(text: str, out_wav_path: str, voice_name: str = "Kore") -> str:
    """
    Generate Thai TTS using Gemini TTS (gemini-2.5-flash-preview-tts) and save to WAV.
    """
    print(f"[TTS] 生成泰语，音色: {voice_name}，文本长度: {len(text)} -> {out_wav_path}")
    client = genai.Client()
    # 若文本过长，分段合成后拼接
    chunks = _split_text_for_tts(text, max_len=250)
    if len(chunks) == 1:
        resp = _tts_generate_with_retry(client, text, voice_name)
        data = None
        try:
            data = resp.candidates[0].content.parts[0].inline_data.data
        except Exception:
            pass
        if data is None:
            raise RuntimeError("Gemini TTS 未返回音频数据")
        if isinstance(data, str):
            try:
                pcm_bytes = base64.b64decode(data)
            except Exception:
                pcm_bytes = data.encode("utf-8", errors="ignore")
        else:
            pcm_bytes = data
        return _save_wave(out_wav_path, pcm_bytes)
    else:
        # 多段合成
        tmp_wavs: List[str] = []
        for idx, part in enumerate(chunks, start=1):
            part_out = out_wav_path + f".part{idx:02d}.wav"
            resp = _tts_generate_with_retry(client, part, voice_name)
            data = None
            try:
                data = resp.candidates[0].content.parts[0].inline_data.data
            except Exception:
                pass
            if data is None:
                # 生成失败则用短静音代替
                _generate_silence_wav(0.1, part_out)
            else:
                if isinstance(data, str):
                    try:
                        pcm_bytes = base64.b64decode(data)
                    except Exception:
                        pcm_bytes = data.encode("utf-8", errors="ignore")
                else:
                    pcm_bytes = data
                _save_wave(part_out, pcm_bytes)
            tmp_wavs.append(part_out)
        # 拼接
        concat_audios(tmp_wavs, out_wav_path)
        # 清理
        for p in tmp_wavs:
            try:
                os.remove(p)
            except Exception:
                pass
        return out_wav_path


def split_script_to_segments(script: str, storyboard: List[Dict[str, Any]]) -> List[str]:
    """
    Split a full script into N segments roughly proportional to each shot's use_seconds.
    Simple heuristic: allocate by character count; try to break near punctuation.
    """
    text = script.strip()
    if not text:
        return ["" for _ in storyboard]

    total_chars = len(text)
    total_secs = sum(float(s.get("use_seconds", 0) or 0) for s in storyboard) or 1.0
    targets = [max(1, round(total_chars * float(s.get("use_seconds", 0) or 0) / total_secs)) for s in storyboard]

    # Adjust targets to sum to total_chars
    diff = total_chars - sum(targets)
    for i in range(abs(diff)):
        idx = i % len(targets)
        targets[idx] += 1 if diff > 0 else -1

    print(f"[Split] 总字符: {total_chars}，总时长: {total_secs:.2f}s，目标字符分配: {targets}")
    segments: List[str] = []
    i = 0
    for t in targets:
        if i >= total_chars:
            segments.append("")
            continue
        j = min(total_chars, i + t)
        # try to snap to nearest punctuation within ±10 chars
        window_start = max(i, j - 10)
        window_end = min(total_chars, j + 10)
        window = text[window_start:window_end]
        m = None
        # Thai text may not have spaces; prefer punctuation-like breaks
        for pattern in [r"[。．！？!?]\s*", r"[,，、]\s*", r"\s+"]:
            matches = list(re.finditer(pattern, window))
            if matches:
                # pick the break closest to center
                center = j - window_start
                m = min(matches, key=lambda x: abs(x.end() - center))
                j = window_start + m.end()
                break
        seg = text[i:j]
        seg_clean = seg.strip()
        segments.append(seg_clean)
        print(f"[Split] 片段 {len(segments):02d}: 字数≈{len(seg_clean)} 文本: {seg_clean[:30]}...")
        i = j

    # Append any leftover to last segment
    if i < total_chars and segments:
        segments[-1] = (segments[-1] + " " + text[i:]).strip()

    return segments


def synthesize_segments_thai(lines: List[str], work_dir: str, voice_name: str = "Kore") -> List[str]:
    """
    Generate per-segment Thai TTS WAV files using Gemini.
    """
    print(f"[TTS] 开始逐镜头合成，共 {len(lines)} 段")
    paths: List[str] = []
    for idx, line in enumerate(lines, start=1):
        out_wav = os.path.join(work_dir, f"tts_seg_{idx:03d}.wav")
        if not line.strip():
            # generate a short silence (50ms)
            # Create 0.05s of silence at 24kHz mono pcm_s16le
            num_samples = int(0.05 * 24000)
            pcm = b"\x00\x00" * num_samples
            _save_wave(out_wav, pcm)
        else:
            synthesize_tts_thai(line, out_wav, voice_name=voice_name)
        paths.append(out_wav)
        print(f"[TTS] 段 {idx:02d} -> {out_wav}")
    return paths


def concat_audios(wavs: List[str], out_wav_path: str) -> str:
    os.makedirs(os.path.dirname(out_wav_path), exist_ok=True)
    list_path = out_wav_path + ".list.txt"
    with open(list_path, "w", encoding="utf-8") as f:
        for p in wavs:
            abs_p = os.path.abspath(p)
            f.write(f"file '{abs_p}'\n")
    print(f"[Concat-Audio] 拼接 {len(wavs)} 段音频 -> {out_wav_path}")
    (
        ffmpeg
        .input(list_path, f='concat', safe=0)
        .output(out_wav_path, acodec='pcm_s16le', ar=24000, ac=1, loglevel='quiet')
        .overwrite_output()
        .run()
    )
    dur = _probe_duration_seconds(out_wav_path)
    print(f"[Concat-Audio] 完成: {out_wav_path} 时长: {dur:.2f}s")
    return out_wav_path


def _trim_shot(input_path: str, use_seconds: float, out_path: str) -> str:
    """
    Trim a shot to desired seconds (re-encode for accurate trim) and save.
    """
    try:
        (
            ffmpeg
            .input(input_path)
            .output(
                out_path,
                t=use_seconds,
                vcodec='libx264',
                an=None,  # drop audio to avoid concat codec mismatches
                r=30,
                vf='scale=trunc(iw/2)*2:trunc(ih/2)*2,format=yuv420p',
                preset='veryfast', movflags='+faststart',
                loglevel='quiet'
            )
            .overwrite_output()
            .run()
        )
    except ffmpeg.Error as e:
        try:
            print(f"FFmpeg trim error for {input_path}:\n{e.stderr.decode('utf-8', 'ignore')}")
        except Exception:
            print("FFmpeg trim error (no stderr)")
        raise
    return out_path


def concat_shots(storyboard: List[Dict[str, Any]], out_video_path: str, work_dir: str, override_seconds: List[float] = None) -> str:
    """
    Trim per-shot according to `use_seconds` and concatenate into a single video.
    """
    os.makedirs(work_dir, exist_ok=True)
    trimmed_files: List[str] = []

    print(f"[Concat-Video] 需要拼接 {len(storyboard)} 个镜头，输出: {out_video_path}")
    for i, item in enumerate(storyboard, start=1):
        seg_path = item["segment_path"]
        if not os.path.exists(seg_path):
            print(f"警告：片段不存在，跳过 -> {seg_path}")
            continue
        if override_seconds is not None and len(override_seconds) >= i:
            use_seconds = float(override_seconds[i-1] or 0)
        else:
            use_seconds = float(item.get("use_seconds", 0))
        if use_seconds <= 0:
            continue
        trimmed = os.path.join(work_dir, f"trim_{i:03d}.mp4")
        _trim_shot(seg_path, use_seconds, trimmed)
        trimmed_files.append(trimmed)

    if not trimmed_files:
        raise RuntimeError("No trimmed files were produced from storyboard")

    concat_list_path = os.path.join(work_dir, "concat_list.txt")
    with open(concat_list_path, "w", encoding="utf-8") as f:
        for p in trimmed_files:
            abs_p = os.path.abspath(p)
            f.write(f"file '{abs_p}'\n")
    print(f"[Concat-Video] 列表文件: {concat_list_path}")

    # Re-encode on concat to avoid codec mismatch issues
    try:
        (
            ffmpeg
            .input(concat_list_path, f='concat', safe=0)
            .output(out_video_path, vcodec='libx264', an=None,
                    movflags='+faststart', preset='veryfast', pix_fmt='yuv420p', loglevel='quiet')
            .overwrite_output()
            .run()
        )
        print(f"[Concat-Video] 完成: {out_video_path}")
    except ffmpeg.Error as e:
        try:
            print(f"FFmpeg concat error:\n{e.stderr.decode('utf-8', 'ignore')}")
        except Exception:
            print("FFmpeg concat error (no stderr)")
        raise
    return out_video_path


def _probe_duration_seconds(path: str) -> float:
    try:
        info = ffmpeg.probe(path)
        for stream in info.get('streams', []):
            if stream.get('codec_type') in ('audio', 'video'):
                if 'duration' in stream:
                    return float(stream['duration'])
        if 'format' in info and 'duration' in info['format']:
            return float(info['format']['duration'])
    except Exception:
        pass
    return 0.0


def _time_stretch_audio(in_path: str, out_path: str, factor: float) -> str:
    """
    Time-stretch audio using atempo filters. Chains factors to stay within [0.5, 2.0].
    """
    if factor <= 0:
        raise ValueError("factor must be > 0")
    factors = []
    f = factor
    while f > 2.0:
        factors.append(2.0)
        f /= 2.0
    while f < 0.5:
        factors.append(0.5)
        f /= 0.5
    factors.append(f)

    print(f"[Stretch] {in_path} -> factor={factor:.3f} -> {out_path}")
    inp = ffmpeg.input(in_path)
    a = inp.audio
    for r in factors:
        a = ffmpeg.filter(a, 'atempo', r)
    (
        ffmpeg
        .output(a, out_path, acodec='pcm_s16le', ar=24000, ac=1, loglevel='quiet')
        .overwrite_output()
        .run()
    )
    return out_path


def _generate_silence_wav(duration_sec: float, out_wav: str) -> str:
    """
    Generate a PCM WAV silence of given duration at 24kHz mono.
    """
    if duration_sec <= 0:
        # generate minimal silence 10ms
        duration_sec = 0.01
    (
        ffmpeg
        .input('anullsrc=r=24000:cl=mono', f='lavfi')
        .output(out_wav, t=duration_sec, acodec='pcm_s16le', ar=24000, ac=1, loglevel='quiet')
        .overwrite_output()
        .run()
    )
    return out_wav


def _enforce_exact_duration_audio(in_path: str, out_path: str, target_sec: float) -> str:
    """
    Force audio to exact target duration by trimming or padding with silence, then trimming.
    """
    cur = _probe_duration_seconds(in_path)
    print(f"[ForceDur] {in_path} 当前 {cur:.3f}s -> 目标 {target_sec:.3f}s -> {out_path}")
    if target_sec <= 0:
        # nothing sensible to do
        shutil.copyfile(in_path, out_path)
        return out_path

    if cur >= target_sec:
        # Trim to exact target
        (
            ffmpeg
            .input(in_path)
            .output(out_path, af=f"atrim=0:{target_sec}", acodec='pcm_s16le', ar=24000, ac=1, loglevel='quiet')
            .overwrite_output()
            .run()
        )
    else:
        # Pad with silence to reach target, then atrim as safeguard
        pad_needed = max(0.0, target_sec - cur)
        sil = out_path + ".sil.wav"
        _generate_silence_wav(pad_needed + 0.1, sil)  # add small guard
        concat_tmp = out_path + ".concat.wav"
        list_path = out_path + ".list.txt"
        with open(list_path, 'w', encoding='utf-8') as f:
            f.write(f"file '{os.path.abspath(in_path)}'\n")
            f.write(f"file '{os.path.abspath(sil)}'\n")
        (
            ffmpeg
            .input(list_path, f='concat', safe=0)
            .output(concat_tmp, acodec='pcm_s16le', ar=24000, ac=1, loglevel='quiet')
            .overwrite_output()
            .run()
        )
        (
            ffmpeg
            .input(concat_tmp)
            .output(out_path, af=f"atrim=0:{target_sec}", acodec='pcm_s16le', ar=24000, ac=1, loglevel='quiet')
            .overwrite_output()
            .run()
        )
        try:
            os.remove(sil)
            os.remove(concat_tmp)
            os.remove(list_path)
        except Exception:
            pass
    final_dur = _probe_duration_seconds(out_path)
    print(f"[ForceDur] 完成: {out_path} 时长 {final_dur:.3f}s")
    return out_path


def mux_voiceover(video_path: str, tts_audio_path: str, out_path: str, mute_original: bool = True) -> str:
    """
    Combine video with TTS audio. If mute_original, discard original audio.
    """
    if mute_original:
        in_v = ffmpeg.input(video_path)
        in_a = ffmpeg.input(tts_audio_path)
        try:
            (
                ffmpeg
                .output(in_v.video, in_a.audio, out_path,
                        vcodec='copy', acodec='aac', audio_bitrate='192k', ar=48000, ac=2,
                        shortest=None, loglevel='quiet')
                .overwrite_output()
                .run()
            )
        except ffmpeg.Error as e:
            try:
                print(f"FFmpeg mux error (mute_original):\n{e.stderr.decode('utf-8', 'ignore')}")
            except Exception:
                print("FFmpeg mux error (mute_original) - no stderr")
            raise
    else:
        # Mix original audio with TTS (simple amix)
        in_v = ffmpeg.input(video_path)
        in_a = ffmpeg.input(tts_audio_path)
        mixed = ffmpeg.filter([in_v.audio, in_a.audio], 'amix', inputs=2, duration='shortest')
        try:
            (
                ffmpeg
                .output(in_v.video, mixed, out_path, vcodec='copy', acodec='aac', audio_bitrate='192k', ar=48000, ac=2,
                        shortest=None, loglevel='quiet')
                .overwrite_output()
                .run()
            )
        except ffmpeg.Error as e:
            try:
                print(f"FFmpeg mux error (mix):\n{e.stderr.decode('utf-8', 'ignore')}")
            except Exception:
                print("FFmpeg mux error (mix) - no stderr")
            raise
    return out_path


def produce_from_plan(plan: Dict[str, Any], output_dir: str, language: str = "th") -> str:
    os.makedirs(output_dir, exist_ok=True)
    storyboard = plan.get("storyboard", [])
    script = plan.get("voiceover_script", "")
    if not storyboard:
        raise RuntimeError("Empty storyboard in plan")
    if not script:
        raise RuntimeError("Empty voiceover_script in plan")

    work_dir = os.path.join(output_dir, "_work")
    if os.path.isdir(work_dir):
        shutil.rmtree(work_dir)
    os.makedirs(work_dir, exist_ok=True)

    # 1) Split script to per-shot lines（音频优先，先生成精准音频）
    lines = split_script_to_segments(script, storyboard)
    # 2) Per-shot TTS
    seg_tts_paths = synthesize_segments_thai(lines, work_dir, voice_name="Kore")
    # 3) Per-shot length match (stretch to near + force exact)
    matched_paths: List[str] = []
    exact_seconds: List[float] = []
    for i, (p, shot) in enumerate(zip(seg_tts_paths, storyboard), start=1):
        goal = float(shot.get("use_seconds", 0) or 0)
        if goal <= 0:
            matched_paths.append(p)
            exact_seconds.append(_probe_duration_seconds(p))
            continue
        cur = _probe_duration_seconds(p)
        if cur > 0 and abs(cur - goal) > 0.05:
            factor = goal / cur
            stretched = os.path.join(work_dir, f"tts_seg_{i:03d}_matched.wav")
            _time_stretch_audio(p, stretched, factor)
            # enforce exact
            exact = os.path.join(work_dir, f"tts_seg_{i:03d}_exact.wav")
            _enforce_exact_duration_audio(stretched, exact, goal)
            matched_paths.append(exact)
            exact_seconds.append(_probe_duration_seconds(exact))
        else:
            # even if close, still enforce exact to avoid累积误差
            exact = os.path.join(work_dir, f"tts_seg_{i:03d}_exact.wav")
            _enforce_exact_duration_audio(p, exact, goal)
            matched_paths.append(exact)
            exact_seconds.append(_probe_duration_seconds(exact))
    # 4) Concat all audio segments
    tts_final = os.path.join(work_dir, "voiceover_th_concat.wav")
    concat_audios(matched_paths, tts_final)
    # 5) Cut video according to exact audio seconds (音频主导重剪视频)
    concat_path = os.path.join(work_dir, "video_concat.mp4")
    concat_shots(storyboard, concat_path, work_dir, override_seconds=exact_seconds)
    # 6) Mux to final
    final_path = os.path.join(output_dir, "final_th.mp4")
    mux_voiceover(concat_path, tts_final, final_path, mute_original=True)

    return final_path


if __name__ == "__main__":
    # Example: read plan.json and produce
    plan_path = os.path.join("assets", "last_plan_th.json")
    if not os.path.exists(plan_path):
        raise SystemExit("No plan file found. Generate plan via director first.")
    with open(plan_path, "r", encoding="utf-8") as f:
        plan = json.load(f)
    out = produce_from_plan(plan, output_dir="final_output", language="th")
    print(f"✅  已生成成片: {out}")


