print("脚本开始执行...")
import os
import sys
from video_processor import analyze_video, cut_video_shots
import glob
import json

def process_video(video_path):
    """
    对单个视频文件执行分析和切割的完整流程。
    """
    video_filename = os.path.basename(video_path)
    print("-" * 60)
    print(f"▶️  开始处理视频: {video_filename}")
    print("-" * 60)

    # 步骤 1: 使用 Gemini 分析视频
    analysis_result = analyze_video(video_path)

    if analysis_result and "shots" in analysis_result and analysis_result["shots"]:
        # 打印 Gemini 返回的 JSON 结果
        print("\n💡 Gemini 精细化分析结果:")
        print(json.dumps(analysis_result, indent=2, ensure_ascii=False))

        # 步骤 2: 根据分析结果切割视频
        # 为每个视频创建一个独立的输出子目录
        video_name_without_ext = os.path.splitext(video_filename)[0]
        output_subdir = os.path.join("output", video_name_without_ext)
        
        # 若包含场景级元数据，先落盘保存，便于后续审片/检索
        try:
            if analysis_result.get("scenes"):
                os.makedirs(output_subdir, exist_ok=True)
                scenes_path = os.path.join(output_subdir, "scenes_meta.json")
                with open(scenes_path, "w", encoding="utf-8") as f:
                    json.dump(analysis_result["scenes"], f, ensure_ascii=False, indent=2)
                print(f"📝 已保存场景级元数据: {scenes_path}")
        except Exception as e:
            print(f"警告：保存场景级元数据失败：{e}")

        cut_video_shots(video_path, analysis_result["shots"], output_dir=output_subdir)
        print(f"✅  成功处理完视频: {video_filename}")
    else:
        print(f"❌  处理失败：未能从 Gemini 获取 '{video_filename}' 的有效镜头信息。")
    
    print("-" * 60 + "\n")


def main():
    """
    项目主入口函数。
    【测试模式】目前设置为只处理单个视频文件。
    """
    input_dir = "input"
    
    # 检查 input 目录是否存在
    if not os.path.isdir(input_dir):
        print(f"错误：输入目录 '{input_dir}' 不存在。")
        print("请创建一个 'input' 目录并将您的视频文件放入其中。")
        sys.exit(1)
        
    # --- 单点聚焦测试 ---
    # 我们暂时只处理一个文件，以验证新流程并评估性能。
    all_videos = glob.glob(os.path.join(input_dir, "*.mp4"))
    if not all_videos:
        print(f"在 '{input_dir}' 目录中未找到任何 .mp4 文件。")
        sys.exit(0)
        
    test_video_path = all_videos[0]  # 自动选择找到的第一个视频进行测试
    print(f"--- 单点聚焦测试模式 ---")
    print(f"将只处理第一个视频: {os.path.basename(test_video_path)}")
    print(f"------------------------")
    
    video_files = [test_video_path]
    
    # # 查找所有 .mp4 文件 (恢复批量处理时使用)
    # video_files = glob.glob(os.path.join(input_dir, "*.mp4"))

    # if not video_files:
    #     print(f"在 '{input_dir}' 目录中未找到任何 .mp4 文件。")
    #     sys.exit(0)

    print(f"共找到 {len(video_files)} 个视频文件待处理。")
    
    for video_path in video_files:
        process_video(video_path)

    print("🎉 所有视频文件已处理完毕！")

if __name__ == "__main__":
    main()
