#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
单视频测试脚本 - 测试一次性分析和多产品识别
"""

import os
import sys
from enhanced_batch_processor import EnhancedBatchProcessor

def test_single_video():
    """测试单个视频处理"""
    
    # 选择第一个视频进行测试
    test_video = "input/Douyin_TikTok_Download_API (77).mp4"
    
    if not os.path.exists(test_video):
        print(f"❌ 测试视频不存在: {test_video}")
        return
    
    print("🧪 单视频功能测试")
    print("=" * 50)
    print(f"📹 测试视频: {os.path.basename(test_video)}")
    
    # 创建处理器
    processor = EnhancedBatchProcessor()
    
    try:
        # 处理单个视频
        result = processor.process_single_video(test_video)
        
        # 显示结果
        print("\n📊 测试结果:")
        print(f"分析成功: {result['analysis_success']}")
        print(f"切割成功: {result['cutting_success']}")
        print(f"上传成功: {result['upload_success']}")
        
        if result['analysis_success']:
            print(f"镜头数量: {result['total_shots']}")
            print(f"产品数量: {result['total_products']}")
        
        if result['error_message']:
            print(f"错误信息: {result['error_message']}")
        
        # 如果处理成功，移动文件
        if result["analysis_success"] and result["cutting_success"]:
            processed_path = processor.move_file(test_video, processor.processed_dir)
            print(f"✅ 原视频已移动到: {processor.processed_dir}")
            
            if result["upload_success"]:
                output_subdir = os.path.join(processor.output_dir, result["video_name"])
                segments_moved = processor.move_output_segments_to_uploaded(
                    output_subdir, 
                    result["video_name"]
                )
                if segments_moved:
                    print(f"✅ 切割片段已移动到: {processor.uploaded_dir}")
        
        print("\n🎉 单视频测试完成!")
        
    except Exception as e:
        print(f"❌ 测试异常: {e}")

if __name__ == "__main__":
    test_single_video()
