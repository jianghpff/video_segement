#!/usr/bin/env python3
"""
仅上传镜头元数据（不上传视频文件）
当网络稳定时可以单独运行此脚本
"""

import json
import os
from feishu_enhanced_integration import FeishuEnhancedIntegration

def upload_metadata_only():
    """仅上传镜头元数据到飞书"""
    
    # 查找最新的分析结果
    video_name = "Douyin_TikTok_Download_API (2)"
    output_dir = f"output/{video_name}"
    scenes_meta_path = os.path.join(output_dir, "scenes_meta.json")
    
    if not os.path.exists(scenes_meta_path):
        print(f"❌ 找不到分析结果: {scenes_meta_path}")
        return False
    
    # 读取分析结果
    try:
        with open(scenes_meta_path, "r", encoding="utf-8") as f:
            scenes = json.load(f)
        print(f"📊 读取到 {len(scenes)} 个场景数据")
    except Exception as e:
        print(f"❌ 读取分析结果失败: {e}")
        return False
    
    # 从场景数据重构镜头数据（简化版）
    shots = []
    for i, scene in enumerate(scenes, 1):
        shot_data = {
            "original_video_name": f"{video_name}.mp4",
            "shot_number": i,
            "shot_id": f"{video_name}_shot_{i:03d}",
            "start_time": scene.get("start_time", ""),
            "end_time": scene.get("end_time", ""),
            "duration": "计算中",  # 简化处理
            "description": scene.get("description", ""),
            "type": "Primary Shot",  # 默认类型
            "tags": ["元数据", "重新上传"],
            "has_product": scene.get("has_product", False),
            "product_type": scene.get("product_type", "未知"),
            "product_info": scene.get("product_info", ""),
            "visuals": scene.get("visuals", ""),
            "human_action": scene.get("human_action", ""),
            "effects_subtitles": scene.get("effects_subtitles", "")
        }
        shots.append(shot_data)
    
    # 上传到飞书
    feishu = FeishuEnhancedIntegration()
    
    success_count = 0
    total_shots = len(shots)
    
    print(f"\n🚀 开始上传 {total_shots} 个镜头的元数据...")
    
    for i, shot_data in enumerate(shots, 1):
        print(f"\n--- 处理镜头 {i}/{total_shots} ---")
        print(f"镜头ID: {shot_data['shot_id']}")
        
        try:
            success = feishu.create_shot_record(shot_data, None)  # 不上传视频文件
            
            if success:
                success_count += 1
                print(f"✅ 镜头 {i} 元数据上传成功")
            else:
                print(f"❌ 镜头 {i} 元数据上传失败")
                
        except Exception as e:
            print(f"❌ 镜头 {i} 上传异常: {e}")
    
    print(f"\n🎉 元数据上传完成！成功 {success_count}/{total_shots} 个镜头")
    
    return success_count == total_shots

if __name__ == "__main__":
    print("🔄 仅上传镜头元数据模式")
    print("-" * 50)
    
    success = upload_metadata_only()
    
    if success:
        print("\n✅ 所有元数据上传成功！")
    else:
        print("\n⚠️  部分元数据上传失败，请检查网络后重试")
