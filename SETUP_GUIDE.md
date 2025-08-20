# 视频分割项目 - 环境设置指南

## 环境设置完成状态 ✅

您的本地开发环境已经成功设置完成！以下是已完成的设置步骤：

### 1. Conda环境 ✅
- 环境名称: `video_segment`
- Python版本: 3.10.18
- 环境路径: `/Users/kekoukele/miniconda3/envs/video_segment`

### 2. FFmpeg安装 ✅
- 版本: 4.3.2
- 通过conda-forge安装
- 支持所有必需的视频处理编解码器

### 3. 项目结构 ✅
```
video_segement/
├── input/          # 放置待处理的视频文件
├── output/         # 存放处理后的视频片段
├── assets/         # 素材库存储目录
├── .env           # API密钥配置文件
└── 项目代码文件...
```

### 4. API配置 ✅
- `.env` 文件已创建
- **重要**: 请编辑 `.env` 文件，将 `YOUR_API_KEY` 替换为您的真实 Gemini API 密钥

## 使用方法

### 激活环境
```bash
conda activate video_segment
```

### 配置API密钥
1. 访问 [Google AI Studio](https://aistudio.google.com/) 获取 Gemini API 密钥
2. 编辑 `.env` 文件：
```bash
# 将下面的 YOUR_API_KEY 替换为您的真实API密钥
GEMINI_API_KEY="your_actual_api_key_here"
```

### 运行项目
1. 将视频文件放入 `input/` 目录
2. 运行主程序：
```bash
python main.py
```

### 项目功能模块

#### 基础视频处理
- `main.py` - 主入口，处理单个视频文件
- `video_processor.py` - 视频分析和切割核心功能

#### 智能编辑功能
- `director.py` - 智能导演，根据需求选择合适素材
- `producer.py` - 视频制作，TTS合成和最终输出
- `assembler.py` - 一键编辑，从创意到成品的全自动流程
- `asset_library.py` - 素材库管理和语义搜索

## 故障排除

如果遇到包导入问题，可以手动安装：
```bash
# 激活环境
conda activate video_segment

# 重新安装核心依赖
pip install --upgrade pip
pip install google-genai ffmpeg-python python-dotenv tqdm numpy gTTS
```

## 项目特色功能

1. **两阶段AI分析**：宏观场景 + 微观镜头精细识别
2. **语义化素材库**：基于向量嵌入的智能素材检索
3. **多语言TTS**：支持泰语等多语言配音生成
4. **音频优先剪辑**：根据音频节奏智能匹配视频内容
5. **端到端自动化**：从素材分析到成品输出的全流程自动化

## 注意事项

- 确保有足够的磁盘空间用于视频处理
- 首次运行时会创建素材库数据文件
- 建议测试时使用较短的视频文件（1-2分钟）
- 处理过程中请保持网络连接稳定（用于AI API调用）

---
🎉 **环境设置完成！您现在可以开始使用这个强大的AI视频处理系统了！**
