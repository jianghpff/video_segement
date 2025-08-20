#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强版批量视频处理器 - 正确的文件移动逻辑
功能：
1. 使用一次性分析处理input文件夹下的所有视频
2. 原视频完成处理后移动到"已处理"文件夹
3. 切割片段成功上传飞书后移动到"已上传"文件夹
4. 支持多产品识别和≥3秒镜头限制
"""

import os
import sys
import json
import glob
import shutil
from datetime import datetime
from typing import List, Dict, Any
from pathlib import Path

from enhanced_video_processor import analyze_video_once, cut_video_shots_enhanced
from feishu_enhanced_integration import FeishuEnhancedIntegration


class EnhancedBatchProcessor:
    def __init__(self):
        self.input_dir = "input"
        self.processed_dir = "已处理"
        self.uploaded_dir = "已上传"
        self.output_dir = "output"
        
        # 确保目录存在
        self.ensure_directories()
        
        # 处理统计
        self.stats = {
            "total_videos": 0,
            "analysis_success": 0,
            "cutting_success": 0,
            "upload_success": 0,
            "failed_videos": []
        }
    
    def ensure_directories(self):
        """确保所有必要的目录存在"""
        directories = [
            self.input_dir,
            self.processed_dir,
            self.uploaded_dir,
            self.output_dir
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            print(f"📁 确保目录存在: {directory}")
    
    def get_video_files(self) -> List[str]:
        """获取input目录下的所有视频文件"""
        video_extensions = ['*.mp4', '*.avi', '*.mov', '*.mkv', '*.wmv']
        video_files = []
        
        for ext in video_extensions:
            pattern = os.path.join(self.input_dir, ext)
            video_files.extend(glob.glob(pattern))
        
        # 按文件名排序
        video_files.sort()
        return video_files
    
    def move_file(self, source_path: str, destination_dir: str) -> str:
        """移动文件到指定目录"""
        try:
            filename = os.path.basename(source_path)
            destination_path = os.path.join(destination_dir, filename)
            
            # 如果目标文件已存在，添加时间戳
            if os.path.exists(destination_path):
                name, ext = os.path.splitext(filename)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                new_filename = f"{name}_{timestamp}{ext}"
                destination_path = os.path.join(destination_dir, new_filename)
            
            shutil.move(source_path, destination_path)
            print(f"📦 文件移动: {filename} → {destination_dir}")
            return destination_path
            
        except Exception as e:
            print(f"❌ 文件移动失败: {e}")
            return source_path
    
    def move_output_segments_to_uploaded(self, output_subdir: str, video_name: str) -> bool:
        """将output中的切割片段移动到已上传文件夹"""
        try:
            # 创建已上传目录下的视频子目录
            uploaded_video_dir = os.path.join(self.uploaded_dir, video_name)
            os.makedirs(uploaded_video_dir, exist_ok=True)
            
            # 移动所有切割片段
            if os.path.exists(output_subdir):
                moved_count = 0
                for item in os.listdir(output_subdir):
                    item_path = os.path.join(output_subdir, item)
                    if os.path.isfile(item_path):
                        destination_path = os.path.join(uploaded_video_dir, item)
                        shutil.move(item_path, destination_path)
                        moved_count += 1
                
                # 删除空的output子目录
                try:
                    os.rmdir(output_subdir)
                    print(f"📦 移动 {moved_count} 个切割片段到: {uploaded_video_dir}")
                    return True
                except OSError:
                    print(f"⚠️ output子目录非空，未删除: {output_subdir}")
                    return True
            
            return False
            
        except Exception as e:
            print(f"❌ 移动切割片段失败: {e}")
            return False
    
    def process_single_video(self, video_path: str) -> Dict[str, Any]:
        """处理单个视频文件（使用一次性分析）"""
        video_filename = os.path.basename(video_path)
        name_no_ext = os.path.splitext(video_filename)[0]
        output_subdir = os.path.join(self.output_dir, name_no_ext)
        
        result = {
            "video_path": video_path,
            "video_filename": video_filename,
            "video_name": name_no_ext,
            "analysis_success": False,
            "cutting_success": False,
            "upload_success": False,
            "analysis_result": None,
            "error_message": None,
            "total_shots": 0,
            "total_products": 0
        }
        
        print(f"\n{'='*80}")
        print(f"🎬 开始处理视频: {video_filename}")
        print(f"{'='*80}")
        
        try:
            # 步骤1: 一次性Gemini分析
            print("🚀 步骤1: 开始一次性Gemini分析（多模态+多产品）...")
            analysis_result = analyze_video_once(video_path)
            
            if not analysis_result or not analysis_result.get('shots'):
                result["error_message"] = "一次性分析失败或未返回镜头数据"
                return result
            
            result["analysis_success"] = True
            result["analysis_result"] = analysis_result
            result["total_shots"] = len(analysis_result['shots'])
            result["total_products"] = analysis_result.get('total_products', 0)
            
            print(f"✅ 分析完成: {result['total_shots']} 个镜头，{result['total_products']} 个产品")
            
            # 步骤2: 保存分析元数据
            print("📝 步骤2: 保存分析元数据...")
            os.makedirs(output_subdir, exist_ok=True)
            
            # 保存完整分析结果
            analysis_path = os.path.join(output_subdir, 'analysis_result.json')
            with open(analysis_path, 'w', encoding='utf-8') as f:
                json.dump(analysis_result, f, ensure_ascii=False, indent=2)
            print(f"✅ 分析结果已保存: {analysis_path}")
            
            # 步骤3: 镜头切割
            print("✂️ 步骤3: 开始镜头切割...")
            cut_video_shots_enhanced(video_path, analysis_result['shots'], output_dir=output_subdir)
            result["cutting_success"] = True
            print(f"✅ 视频切割完成，输出到: {output_subdir}")
            
            # 步骤4: 上传飞书
            print("📤 步骤4: 开始上传飞书（多产品支持）...")
            feishu = FeishuEnhancedIntegration()
            upload_success = feishu.upload_video_analysis_enhanced(video_path, analysis_result)
            
            if upload_success:
                result["upload_success"] = True
                print("✅ 飞书上传成功")
            else:
                result["error_message"] = "飞书上传失败"
                print("❌ 飞书上传失败")
            
        except Exception as e:
            result["error_message"] = str(e)
            print(f"❌ 处理视频异常: {e}")
        
        return result
    
    def process_all_videos(self):
        """批量处理所有视频"""
        print("\n🚀 增强版批量视频处理器启动")
        print("功能: 一次性分析 + 多产品识别 + ≥3秒镜头 + 正确文件移动")
        print("=" * 80)
        
        # 获取所有视频文件
        video_files = self.get_video_files()
        
        if not video_files:
            print("❌ input目录中未找到任何视频文件")
            return
        
        self.stats["total_videos"] = len(video_files)
        print(f"📊 发现 {len(video_files)} 个视频文件待处理")
        
        # 逐个处理视频
        for i, video_path in enumerate(video_files, 1):
            print(f"\n🎯 [{i}/{len(video_files)}] 处理视频: {os.path.basename(video_path)}")
            
            # 处理单个视频
            result = self.process_single_video(video_path)
            
            # 根据处理结果移动文件
            if result["analysis_success"] and result["cutting_success"]:
                # 分析和切割成功，移动原视频到"已处理"
                processed_path = self.move_file(video_path, self.processed_dir)
                self.stats["analysis_success"] += 1
                self.stats["cutting_success"] += 1
                
                if result["upload_success"]:
                    # 上传也成功，移动切割片段到"已上传"
                    output_subdir = os.path.join(self.output_dir, result["video_name"])
                    segments_moved = self.move_output_segments_to_uploaded(
                        output_subdir, 
                        result["video_name"]
                    )
                    
                    if segments_moved:
                        self.stats["upload_success"] += 1
                        print(f"🎉 视频 {result['video_filename']} 完全处理完成！")
                        print(f"   📊 {result['total_shots']} 个镜头，{result['total_products']} 个产品")
                    else:
                        print(f"⚠️ 视频 {result['video_filename']} 上传成功但片段移动失败")
                else:
                    print(f"⚠️ 视频 {result['video_filename']} 分析切割完成但上传失败")
            else:
                # 处理失败，记录错误但不移动文件
                self.stats["failed_videos"].append({
                    "filename": result["video_filename"],
                    "error": result["error_message"]
                })
                print(f"❌ 视频 {result['video_filename']} 处理失败: {result['error_message']}")
        
        # 显示最终统计
        self.show_final_statistics()
    
    def show_final_statistics(self):
        """显示最终处理统计"""
        print("\n" + "=" * 80)
        print("📊 增强版批量处理完成统计")
        print("=" * 80)
        
        print(f"总视频数量: {self.stats['total_videos']}")
        print(f"分析成功: {self.stats['analysis_success']}")
        print(f"切割成功: {self.stats['cutting_success']}")
        print(f"上传成功: {self.stats['upload_success']}")
        print(f"处理失败: {len(self.stats['failed_videos'])}")
        
        if self.stats["failed_videos"]:
            print("\n❌ 失败的视频:")
            for failed in self.stats["failed_videos"]:
                print(f"  - {failed['filename']}: {failed['error']}")
            print("\n💡 失败的视频仍保留在input目录，可以重新运行处理")
        
        success_rate = (self.stats["upload_success"] / self.stats["total_videos"] * 100) if self.stats["total_videos"] > 0 else 0
        print(f"\n🎯 整体成功率: {success_rate:.1f}%")
        
        print("\n📁 文件组织结构:")
        print(f"  input/ - 待处理或处理失败的原视频")
        print(f"  已处理/ - 已完成分析和切割的原视频")
        print(f"  已上传/ - 按视频名称分组的已上传切割片段")
        print(f"      └── 视频名/")
        print(f"          ├── 001_镜头描述.mp4")
        print(f"          ├── 002_镜头描述.mp4")
        print(f"          └── analysis_result.json")
        print(f"  output/ - 临时切割目录（成功上传后会清空）")
        
        print("\n🔬 分析特性:")
        print("  ✅ 一次性Gemini分析（减少API调用）")
        print("  ✅ 多模态分析（视频+音频内容）")
        print("  ✅ 多产品识别（一个镜头可识别多个产品）")
        print("  ✅ 镜头时长限制（≥3秒，自动合并短镜头）")
        print("  ✅ 中文产品名称（直接输出，无需二次提取）")
    
    def cleanup_empty_outputs(self):
        """清理空的output子目录"""
        try:
            if os.path.exists(self.output_dir):
                for item in os.listdir(self.output_dir):
                    item_path = os.path.join(self.output_dir, item)
                    if os.path.isdir(item_path) and not os.listdir(item_path):
                        os.rmdir(item_path)
                        print(f"🗑️ 清理空目录: {item_path}")
        except Exception as e:
            print(f"⚠️ 清理目录时出错: {e}")


def main():
    """主函数"""
    print("🎬 增强版批量视频处理器")
    print("新特性: 一次性分析 + 多产品识别 + 正确文件移动")
    print("=" * 80)
    
    processor = EnhancedBatchProcessor()
    
    try:
        processor.process_all_videos()
    except KeyboardInterrupt:
        print("\n\n⏹️ 用户中断处理")
    except Exception as e:
        print(f"\n\n❌ 批量处理异常: {e}")
    finally:
        processor.cleanup_empty_outputs()
        print("\n👋 增强版批量处理器退出")


if __name__ == "__main__":
    main()
