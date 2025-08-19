# Gemini 智能视频切割工具

这是一个基于 Google Gemini Pro Vision 模型构建的 Python 项目，旨在智能分析长视频并将其自动化地切割成多个有意义的短片段。

## 功能

- **智能分析**: 利用 Gemini 的多模态能力，理解视频内容、场景和结构。
- **自动切割**: 根据模型返回的时间戳，精确地将视频分割成片段。
- **结构化输出**: 切割后的片段将保存在 `output/` 目录下，并可根据分析结果进行命名。

## 项目结构

```
/
├── input/                  # 存放待处理的视频
├── output/                 # 存放切割后的视频片段
├── .env                    # 存储 API 密钥
├── .gitignore              # Git 忽略配置
├── README.md               # 本文档
├── main.py                 # 项目主入口
├── prompts.py              # Gemini Prompt 模板
├── requirements.txt        # Python 依赖
└── video_processor.py      # 核心视频处理模块
```

## 安装与配置

**1. 前提条件**

您必须在您的系统上安装 [FFmpeg](https://ffmpeg.org/download.html)。请根据您的操作系统（Windows, macOS, Linux）进行安装，并确保 `ffmpeg` 命令在您的终端中可用。

您可以通过运行以下命令来检查 FFmpeg 是否安装成功：
```bash
ffmpeg -version
```

**2. 克隆并进入项目**

```bash
git clone <your-repo-url>
cd gemini-video-cutter 
```

**3. 安装 Python 依赖**

建议在虚拟环境中安装，以避免与系统库冲突。

```bash
python3 -m venv venv
source venv/bin/activate  # macOS / Linux
# venv\Scripts\activate   # Windows

pip install -r requirements.txt
```

**4. 配置 API 密钥**

将您的 Google Gemini API 密钥添加到 `.env` 文件中。

1.  打开 `.env` 文件。
2.  将 `YOUR_API_KEY` 替换为您的真实密钥。

```
GEMINI_API_KEY="YOUR_API_KEY"
```

## 如何使用

1.  将您想要切割的长视频文件放入 `input/` 目录。
2.  运行 `main.py` 脚本，并指定视频文件名。

例如，如果您的视频名为 `my_long_video.mp4`：

```bash
python main.py my_long_video.mp4
```

程序将开始处理视频，您会看到一个进度条。处理完成后，切割好的视频片段将出现在 `output/` 目录中。
