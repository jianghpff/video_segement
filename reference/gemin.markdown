Title: 视频理解

URL Source: https://ai.google.dev/gemini-api/docs/video-understanding?hl=zh-cn

Markdown Content:
[跳至主要内容](https://ai.google.dev/gemini-api/docs/video-understanding?hl=zh-cn#main-content)

*   [模型](https://ai.google.dev/gemini-api/docs)
    *   [Gemini API 文档](https://ai.google.dev/gemini-api/docs)
    *   [API 参考文档](https://ai.google.dev/api)
    *   [实战宝典](https://github.com/google-gemini/cookbook)
    *   [社区](https://discuss.ai.google.dev/c/gemini-api/)

*    解决方案 
*    代码编写协助 
*    橱窗广告 
*    社区 

*   开始使用

*   [概览](https://ai.google.dev/gemini-api/docs)
*   [快速入门](https://ai.google.dev/gemini-api/docs/quickstart)
*   [API 密钥](https://ai.google.dev/gemini-api/docs/api-key)
*   [库](https://ai.google.dev/gemini-api/docs/libraries)
*   [OpenAI 兼容性](https://ai.google.dev/gemini-api/docs/openai)
*   模型

*   [Gemini](https://ai.google.dev/gemini-api/docs/models)
*   [Imagen（图片生成）](https://ai.google.dev/gemini-api/docs/imagen)
*   [Veo（视频生成）](https://ai.google.dev/gemini-api/docs/video)
*   [Lyria（音乐生成）](https://ai.google.dev/gemini-api/docs/music-generation)
*   [Embeddings](https://ai.google.dev/gemini-api/docs/embeddings)
*   [价格](https://ai.google.dev/gemini-api/docs/pricing)
*   [速率限制](https://ai.google.dev/gemini-api/docs/rate-limits)
*   [账单信息](https://ai.google.dev/gemini-api/docs/billing)
*   核心功能

*   [文本生成](https://ai.google.dev/gemini-api/docs/text-generation)
*   [图片生成](https://ai.google.dev/gemini-api/docs/image-generation)
*   [语音生成](https://ai.google.dev/gemini-api/docs/speech-generation)
*   [长上下文](https://ai.google.dev/gemini-api/docs/long-context)
*   [结构化输出](https://ai.google.dev/gemini-api/docs/structured-output)
*   [做思考状](https://ai.google.dev/gemini-api/docs/thinking)
*   [文档理解](https://ai.google.dev/gemini-api/docs/document-processing)
*   [图片理解](https://ai.google.dev/gemini-api/docs/image-understanding)
*   [视频理解](https://ai.google.dev/gemini-api/docs/video-understanding)
*   [音频理解](https://ai.google.dev/gemini-api/docs/audio)
*   [函数调用](https://ai.google.dev/gemini-api/docs/function-calling)
*   工具

*   [Google Search](https://ai.google.dev/gemini-api/docs/google-search)
*   [代码执行](https://ai.google.dev/gemini-api/docs/code-execution)
*   [网址上下文](https://ai.google.dev/gemini-api/docs/url-context)
*   Live API

*   [开始使用](https://ai.google.dev/gemini-api/docs/live)
*   [功能](https://ai.google.dev/gemini-api/docs/live-guide)
*   [工具使用](https://ai.google.dev/gemini-api/docs/live-tools)
*   [会话管理](https://ai.google.dev/gemini-api/docs/live-session)
*   [临时令牌](https://ai.google.dev/gemini-api/docs/ephemeral-tokens)
*   指南

*   [批处理模式](https://ai.google.dev/gemini-api/docs/batch-mode)
*   [上下文缓存](https://ai.google.dev/gemini-api/docs/caching)
*   [文件 API](https://ai.google.dev/gemini-api/docs/files)
*   [令牌计数](https://ai.google.dev/gemini-api/docs/tokens)
*   [提示工程](https://ai.google.dev/gemini-api/docs/prompting-strategies)

*   资源

*   [迁移到 Gen AI SDK](https://ai.google.dev/gemini-api/docs/migrate)
*   [版本说明](https://ai.google.dev/gemini-api/docs/changelog)
*   [API 问题排查](https://ai.google.dev/gemini-api/docs/troubleshooting)
*   [微调](https://ai.google.dev/gemini-api/docs/model-tuning)

*   政策

*   [服务条款](https://ai.google.dev/gemini-api/terms)
*   [可用区域](https://ai.google.dev/gemini-api/docs/available-regions)
*   [其他使用政策](https://ai.google.dev/gemini-api/docs/usage-policies)

视频理解
----

*   本页内容
*   [视频输入](https://ai.google.dev/gemini-api/docs/video-understanding?hl=zh-cn#video-input)
    *   [上传视频文件](https://ai.google.dev/gemini-api/docs/video-understanding?hl=zh-cn#upload-video)
    *   [以内嵌方式传递视频数据](https://ai.google.dev/gemini-api/docs/video-understanding?hl=zh-cn#inline-video)
    *   [添加 YouTube 网址](https://ai.google.dev/gemini-api/docs/video-understanding?hl=zh-cn#youtube)

*   [参考内容中的时间戳](https://ai.google.dev/gemini-api/docs/video-understanding?hl=zh-cn#refer-timestamps)
*   [转写视频并提供视觉描述](https://ai.google.dev/gemini-api/docs/video-understanding?hl=zh-cn#transcribe-video)
*   [自定义视频处理](https://ai.google.dev/gemini-api/docs/video-understanding?hl=zh-cn#customize-video-processing)
    *   [设置剪辑间隔](https://ai.google.dev/gemini-api/docs/video-understanding?hl=zh-cn#clipping-intervals)
    *   [设置自定义帧速率](https://ai.google.dev/gemini-api/docs/video-understanding?hl=zh-cn#custom-frame-rate)

*   [支持的视频格式](https://ai.google.dev/gemini-api/docs/video-understanding?hl=zh-cn#supported-formats)
*   [有关视频技术方面的详细信息](https://ai.google.dev/gemini-api/docs/video-understanding?hl=zh-cn#technical-details-video)
*   [后续步骤](https://ai.google.dev/gemini-api/docs/video-understanding?hl=zh-cn#whats-next)

Gemini 模型可以处理视频，从而实现许多前沿的开发者用例，而这些用例在过去需要使用特定领域的模型才能实现。Gemini 的部分视觉功能包括：

*   描述视频、对视频进行分段并从中提取信息
*   回答与视频内容相关的问题
*   引用视频中的特定时间戳

Gemini 从一开始就具备多模态特性，我们也在不断突破可能性的界限。本指南介绍了如何使用 Gemini API 根据视频输入生成文本回答。

视频输入
----

您可以通过以下方式向 Gemini 提供视频作为输入内容：

*   在向 `generateContent` 发出请求之前，使用 File API [上传视频文件](https://ai.google.dev/gemini-api/docs/video-understanding?hl=zh-cn#upload-video)。如果文件大于 20MB、视频时长超过大约 1 分钟，或者您想在多个请求中重复使用该文件，请使用此方法。
*   通过向 `generateContent` 发出的请求[传递内嵌视频数据](https://ai.google.dev/gemini-api/docs/video-understanding?hl=zh-cn#inline-video)。此方法适用于较小的文件（小于 20MB）和较短的持续时间。
*   直接在提示中[添加 YouTube 网址](https://ai.google.dev/gemini-api/docs/video-understanding?hl=zh-cn#youtube)。

### 上传视频文件

您可以使用 [Files API](https://ai.google.dev/gemini-api/docs/files?hl=zh-cn) 上传视频文件。 如果总请求大小（包括文件、文本提示、系统指令等）超过 20 MB、视频时长较长，或者您打算在多个提示中使用同一视频，请务必使用 Files API。 File API 直接接受视频文件格式。

以下代码会下载示例视频，使用 File API 上传该视频，等待其处理完毕，然后在 `generateContent` 请求中使用文件引用。

```
from google import genai

client = genai.Client()

myfile = client.files.upload(file="path/to/sample.mp4")

response = client.models.generate_content(
    model="gemini-2.5-flash", contents=[myfile, "Summarize this video. Then create a quiz with an answer key based on the information in this video."]
)

print(response.text)
```

```
import {
  GoogleGenAI,
  createUserContent,
  createPartFromUri,
} from "@google/genai";

const ai = new GoogleGenAI({});

async function main() {
  const myfile = await ai.files.upload({
    file: "path/to/sample.mp4",
    config: { mimeType: "video/mp4" },
  });

  const response = await ai.models.generateContent({
    model: "gemini-2.5-flash",
    contents: createUserContent([
      createPartFromUri(myfile.uri, myfile.mimeType),
      "Summarize this video. Then create a quiz with an answer key based on the information in this video.",
    ]),
  });
  console.log(response.text);
}

await main();
```

```
uploadedFile, _ := client.Files.UploadFromPath(ctx, "path/to/sample.mp4", nil)

parts := []*genai.Part{
    genai.NewPartFromText("Summarize this video. Then create a quiz with an answer key based on the information in this video."),
    genai.NewPartFromURI(uploadedFile.URI, uploadedFile.MIMEType),
}

contents := []*genai.Content{
    genai.NewContentFromParts(parts, genai.RoleUser),
}

result, _ := client.Models.GenerateContent(
    ctx,
    "gemini-2.5-flash",
    contents,
    nil,
)

fmt.Println(result.Text())
```

```
VIDEO_PATH="path/to/sample.mp4"
MIME_TYPE=$(file -b --mime-type "${VIDEO_PATH}")
NUM_BYTES=$(wc -c < "${VIDEO_PATH}")
DISPLAY_NAME=VIDEO

tmp_header_file=upload-header.tmp

echo "Starting file upload..."
curl "https://generativelanguage.googleapis.com/upload/v1beta/files" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -D ${tmp_header_file} \
  -H "X-Goog-Upload-Protocol: resumable" \
  -H "X-Goog-Upload-Command: start" \
  -H "X-Goog-Upload-Header-Content-Length: ${NUM_BYTES}" \
  -H "X-Goog-Upload-Header-Content-Type: ${MIME_TYPE}" \
  -H "Content-Type: application/json" \
  -d "{'file': {'display_name': '${DISPLAY_NAME}'}}" 2> /dev/null

upload_url=$(grep -i "x-goog-upload-url: " "${tmp_header_file}" | cut -d" " -f2 | tr -d "\r")
rm "${tmp_header_file}"

echo "Uploading video data..."
curl "${upload_url}" \
  -H "Content-Length: ${NUM_BYTES}" \
  -H "X-Goog-Upload-Offset: 0" \
  -H "X-Goog-Upload-Command: upload, finalize" \
  --data-binary "@${VIDEO_PATH}" 2> /dev/null > file_info.json

file_uri=$(jq -r ".file.uri" file_info.json)
echo file_uri=$file_uri

echo "File uploaded successfully. File URI: ${file_uri}"

# --- 3. Generate content using the uploaded video file ---
echo "Generating content from video..."
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent" \
    -H "x-goog-api-key: $GEMINI_API_KEY" \
    -H 'Content-Type: application/json' \
    -X POST \
    -d '{
      "contents": [{
        "parts":[
          {"file_data":{"mime_type": "'"${MIME_TYPE}"'", "file_uri": "'"${file_uri}"'"}},
          {"text": "Summarize this video. Then create a quiz with an answer key based on the information in this video."}]
        }]
      }' 2> /dev/null > response.json

jq -r ".candidates[].content.parts[].text" response.json
```

如需详细了解如何处理媒体文件，请参阅 [Files API](https://ai.google.dev/gemini-api/docs/files?hl=zh-cn)。

### 以内嵌方式传递视频数据

您可以直接在对 `generateContent` 的请求中传递较小的视频，而无需使用 File API 上传视频文件。此方法适用于总请求大小不超过 20MB 的较短视频。

以下是提供内嵌视频数据的示例：

```
# Only for videos of size <20Mb
video_file_name = "/path/to/your/video.mp4"
video_bytes = open(video_file_name, 'rb').read()

response = client.models.generate_content(
    model='models/gemini-2.5-flash',
    contents=types.Content(
        parts=[
            types.Part(
                inline_data=types.Blob(data=video_bytes, mime_type='video/mp4')
            ),
            types.Part(text='Please summarize the video in 3 sentences.')
        ]
    )
)
```

```
import { GoogleGenAI } from "@google/genai";
import * as fs from "node:fs";

const ai = new GoogleGenAI({});
const base64VideoFile = fs.readFileSync("path/to/small-sample.mp4", {
  encoding: "base64",
});

const contents = [
  {
    inlineData: {
      mimeType: "video/mp4",
      data: base64VideoFile,
    },
  },
  { text: "Please summarize the video in 3 sentences." }
];

const response = await ai.models.generateContent({
  model: "gemini-2.5-flash",
  contents: contents,
});
console.log(response.text);
```

```
VIDEO_PATH=/path/to/your/video.mp4

if [[ "$(base64 --version 2>&1)" = *"FreeBSD"* ]]; then
  B64FLAGS="--input"
else
  B64FLAGS="-w0"
fi

curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent" \
    -H "x-goog-api-key: $GEMINI_API_KEY" \
    -H 'Content-Type: application/json' \
    -X POST \
    -d '{
      "contents": [{
        "parts":[
            {
              "inline_data": {
                "mime_type":"video/mp4",
                "data": "'$(base64 $B64FLAGS $VIDEO_PATH)'"
              }
            },
            {"text": "Please summarize the video in 3 sentences."}
        ]
      }]
    }' 2> /dev/null
```

### 添加 You Tube 网址

Gemini API 和 AI Studio 支持将 YouTube 网址作为文件数据 `Part`。您可以在提示中添加 YouTube 网址，要求模型总结、翻译或以其他方式与视频内容互动。

**限制：**

*   对于免费层级，您每天上传的 YouTube 视频时长不得超过 8 小时。
*   对于付费方案，没有视频时长限制。
*   对于 2.5 之前的模型，您每次只能上传 1 个视频。对于 2.5 之后的模型，每个请求最多可以上传 10 个视频。
*   您只能上传公开视频（不能上传私享视频或不公开列出的视频）。

以下示例展示了如何通过提示添加 YouTube 网址：

```
response = client.models.generate_content(
    model='models/gemini-2.5-flash',
    contents=types.Content(
        parts=[
            types.Part(
                file_data=types.FileData(file_uri='https://www.youtube.com/watch?v=9hE5-98ZeCg')
            ),
            types.Part(text='Please summarize the video in 3 sentences.')
        ]
    )
)
```

```
import { GoogleGenerativeAI } from "@google/generative-ai";

const genAI = new GoogleGenerativeAI(process.env.GOOGLE_API_KEY);
const model = genAI.getGenerativeModel({ model: "gemini-1.5-pro" });
const result = await model.generateContent([
  "Please summarize the video in 3 sentences.",
  {
    fileData: {
      fileUri: "https://www.youtube.com/watch?v=9hE5-98ZeCg",
    },
  },
]);
console.log(result.response.text());
```

```
package main

import (
  "context"
  "fmt"
  "os"
  "google.golang.org/genai"
)

func main() {
  ctx := context.Background()
  client, err := genai.NewClient(ctx, nil)
  if err != nil {
      log.Fatal(err)
  }

  parts := []*genai.Part{
      genai.NewPartFromText("Please summarize the video in 3 sentences."),
      genai.NewPartFromURI("https://www.youtube.com/watch?v=9hE5-98ZeCg","video/mp4"),
  }

  contents := []*genai.Content{
      genai.NewContentFromParts(parts, genai.RoleUser),
  }

  result, _ := client.Models.GenerateContent(
      ctx,
      "gemini-2.5-flash",
      contents,
      nil,
  )

  fmt.Println(result.Text())
}
```

```
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent" \
    -H "x-goog-api-key: $GEMINI_API_KEY" \
    -H 'Content-Type: application/json' \
    -X POST \
    -d '{
      "contents": [{
        "parts":[
            {"text": "Please summarize the video in 3 sentences."},
            {
              "file_data": {
                "file_uri": "https://www.youtube.com/watch?v=9hE5-98ZeCg"
              }
            }
        ]
      }]
    }' 2> /dev/null
```

参考内容中的时间戳
---------

您可以使用 `MM:SS` 格式的时间戳，询问视频中特定时间点的问题。

```
prompt = "What are the examples given at 00:05 and 00:10 supposed to show us?" # Adjusted timestamps for the NASA video
```

```
const prompt = "What are the examples given at 00:05 and 00:10 supposed to show us?";
```

```
prompt := []*genai.Part{
        genai.NewPartFromURI(currentVideoFile.URI, currentVideoFile.MIMEType),
         // Adjusted timestamps for the NASA video
        genai.NewPartFromText("What are the examples given at 00:05 and " +
            "00:10 supposed to show us?"),
    }
```

```
PROMPT="What are the examples given at 00:05 and 00:10 supposed to show us?"
```

转写视频并提供视觉描述
-----------

Gemini 模型可以通过处理音轨和视频帧，转写视频内容并提供视觉描述。对于视觉描述，模型以 **1 帧/秒**的速率对视频进行采样。此抽样率可能会影响说明的详细程度，尤其是对于视觉效果快速变化的视频。

```
prompt = "Transcribe the audio from this video, giving timestamps for salient events in the video. Also provide visual descriptions."
```

```
const prompt = "Transcribe the audio from this video, giving timestamps for salient events in the video. Also provide visual descriptions.";
```

```
prompt := []*genai.Part{
        genai.NewPartFromURI(currentVideoFile.URI, currentVideoFile.MIMEType),
        genai.NewPartFromText("Transcribe the audio from this video, giving timestamps for salient events in the video. Also " +
            "provide visual descriptions."),
    }
```

```
PROMPT="Transcribe the audio from this video, giving timestamps for salient events in the video. Also provide visual descriptions."
```

自定义视频处理
-------

您可以在 Gemini API 中通过设置剪辑间隔或提供自定义帧速率选段来自定义视频处理。

### 设置剪辑间隔

您可以通过指定包含开始和结束偏移值的 `videoMetadata` 来剪辑视频。

```
response = client.models.generate_content(
    model='models/gemini-2.5-flash',
    contents=types.Content(
        parts=[
            types.Part(
                file_data=types.FileData(file_uri='https://www.youtube.com/watch?v=XEzRZ35urlk'),
                video_metadata=types.VideoMetadata(
                    start_offset='1250s',
                    end_offset='1570s'
                )
            ),
            types.Part(text='Please summarize the video in 3 sentences.')
        ]
    )
)
```

### 设置自定义帧速率

您可以通过向 `videoMetadata` 传递 `fps` 实参来设置自定义帧速率选段。

```
# Only for videos of size <20Mb
video_file_name = "/path/to/your/video.mp4"
video_bytes = open(video_file_name, 'rb').read()

response = client.models.generate_content(
    model='models/gemini-2.5-flash',
    contents=types.Content(
        parts=[
            types.Part(
                inline_data=types.Blob(
                    data=video_bytes,
                    mime_type='video/mp4'),
                video_metadata=types.VideoMetadata(fps=5)
            ),
            types.Part(text='Please summarize the video in 3 sentences.')
        ]
    )
)
```

默认情况下，系统会按 1 帧/秒 (FPS) 的速率从视频中提取选段。对于长视频，您可能需要设置较低的 FPS（低于 1）。这对于偏静态的视频（例如讲座）尤其有用。如果您想在快速变化的画面中捕捉更多细节，则可考虑设置更高的 FPS 值。

支持的视频格式
-------

Gemini 支持以下视频格式 MIME 类型：

*   `video/mp4`
*   `video/mpeg`
*   `video/mov`
*   `video/avi`
*   `video/x-flv`
*   `video/mpg`
*   `video/webm`
*   `video/wmv`
*   `video/3gpp`

有关视频技术方面的详细信息
-------------

*   **支持的模型和上下文**：所有 Gemini 2.0 和 2.5 模型都可以处理视频数据。
    *   上下文窗口为 200 万个 token 的模型可以处理时长不超过 2 小时（默认媒体分辨率）或 6 小时（低媒体分辨率）的视频，而上下文窗口为 100 万个 token 的模型则可以处理时长不超过 1 小时（默认媒体分辨率）或 3 小时（低媒体分辨率）的视频。

*   **File API 处理**：使用 File API 时，视频的存储速率为 1 帧/秒 (FPS)，音频的处理速率则为 1Kbps（单声道）。每秒都会添加时间戳。 
    *   为了改进推理，这些比率将来可能会发生变化。
    *   您可以[设置自定义帧速率](https://ai.google.dev/gemini-api/docs/video-understanding?hl=zh-cn#custom-frame-rate)，以替换 1 FPS 的采样率。

*   **词元计算**：每秒视频的词元化方式如下： 
    *   各帧（选段率为 1 FPS）： 
        *   如果 [`mediaResolution`](https://ai.google.dev/api/generate-content?hl=zh-cn#MediaResolution) 设置为低，则每帧的令牌化数量为 66 个令牌。
        *   否则，每帧按 258 个 token 计算。

    *   音频：每秒 32 个 token。
    *   元数据也包含在内。
    *   总计：默认媒体分辨率下，每秒视频约 300 个令牌；低媒体分辨率下，每秒视频约 100 个令牌。

*   **时间戳格式**：在提示中提及视频中的特定时刻时，请使用 `MM:SS` 格式（例如，`01:15` 1 分 15 秒）。
*   **最佳实践**： 
    *   为获得最佳效果，每个提示请求仅使用一个视频。
    *   如果将文本与单个视频相结合，请将文本提示放在 `contents` 数组中的视频部分 _之后_。
    *   请注意，如果选段率为 1 FPS，快速动作序列可能会丢失细节。如有必要，可以考虑放慢此类片段的播放速度。

后续步骤
----

本指南介绍了如何上传视频文件并根据视频输入生成文本输出。如需了解详情，请参阅以下资源：

*   [系统指令](https://ai.google.dev/gemini-api/docs/text-generation?hl=zh-cn#system-instructions)：系统指令可让您根据自己的特定需求和使用情形来控制模型的行为。
*   [Files API](https://ai.google.dev/gemini-api/docs/files?hl=zh-cn)：详细了解如何上传和管理文件以供 Gemini 使用。
*   [文件提示策略](https://ai.google.dev/gemini-api/docs/files?hl=zh-cn#prompt-guide)：Gemini API 支持使用文本、图片、音频和视频数据进行提示，也称为多模态提示。
*   [安全指南](https://ai.google.dev/gemini-api/docs/safety-guidance?hl=zh-cn)：生成式 AI 模型有时会生成意料之外的输出，例如不准确、有偏见或令人反感的输出。后处理和人工评估对于限制此类输出造成的危害风险至关重要。

如未另行说明，那么本页面中的内容已根据[知识共享署名 4.0 许可](https://creativecommons.org/licenses/by/4.0/)获得了许可，并且代码示例已根据 [Apache 2.0 许可](https://www.apache.org/licenses/LICENSE-2.0)获得了许可。有关详情，请参阅 [Google 开发者网站政策](https://developers.google.com/site-policies?hl=zh-cn)。Java 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2025-08-08。
a