Title: 语音生成（文本转语音）

URL Source: https://ai.google.dev/gemini-api/docs/speech-generation?hl=zh-cn

Markdown Content:
[跳至主要内容](https://ai.google.dev/gemini-api/docs/speech-generation?hl=zh-cn#main-content)

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
*   [Open AI 兼容性](https://ai.google.dev/gemini-api/docs/openai)
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

语音生成（文本转语音）
-----------

*   本页内容
*   [单说话者文字转语音](https://ai.google.dev/gemini-api/docs/speech-generation?hl=zh-cn#single-speaker)
*   [多说话人文字转语音](https://ai.google.dev/gemini-api/docs/speech-generation?hl=zh-cn#multi-speaker)
*   [使用提示控制说话风格](https://ai.google.dev/gemini-api/docs/speech-generation?hl=zh-cn#controllable)
*   [生成用于转换为音频的提示](https://ai.google.dev/gemini-api/docs/speech-generation?hl=zh-cn#prompt-tts)
*   [语音选项](https://ai.google.dev/gemini-api/docs/speech-generation?hl=zh-cn#voices)
*   [支持的语言](https://ai.google.dev/gemini-api/docs/speech-generation?hl=zh-cn#languages)
*   [支持的模型](https://ai.google.dev/gemini-api/docs/speech-generation?hl=zh-cn#supported-models)
*   [限制](https://ai.google.dev/gemini-api/docs/speech-generation?hl=zh-cn#limitations)
*   [后续步骤](https://ai.google.dev/gemini-api/docs/speech-generation?hl=zh-cn#whats-next)

Gemini API 可以使用原生文字转语音 (TTS) 生成功能将文本输入转换为单人或多人音频。文字转语音 (TTS) 生成是 _[可控](https://ai.google.dev/gemini-api/docs/speech-generation?hl=zh-cn#controllable)_ 的，这意味着您可以使用自然语言来构建互动，并指导音频的 _风格_、_口音_、_节奏_ 和 _音调_。

TTS 功能不同于通过 [Live API](https://ai.google.dev/gemini-api/docs/live?hl=zh-cn) 提供的语音生成功能，后者专为交互式非结构化音频以及多模态输入和输出而设计。虽然 Live API 在动态对话情境中表现出色，但通过 Gemini API 实现的 TTS 专门针对需要精确朗读文本并对风格和声音进行精细控制的场景，例如播客或有声读物生成。

本指南介绍了如何根据文本生成单发言人和多发言人音频。

准备工作
----

请确保您使用的是具有原生文字转语音 (TTS) 功能的 Gemini 2.5 模型变体，如[支持的模型](https://ai.google.dev/gemini-api/docs/speech-generation?hl=zh-cn#supported-models)部分中所列。为获得最佳效果，请考虑哪种模型最适合您的特定使用情形。

在开始构建之前，您可能会发现[在 AI Studio 中测试 Gemini 2.5 TTS 模型](https://aistudio.google.com/generate-speech?hl=zh-cn)很有用。

单说话者文字转语音
---------

如需将文本转换为单人音频，请将响应模态设置为“音频”，并传递一个设置了 `VoiceConfig` 的 `SpeechConfig` 对象。您需要从预建的[输出语音](https://ai.google.dev/gemini-api/docs/speech-generation?hl=zh-cn#voices)中选择一个语音名称。

此示例将模型生成的输出音频保存到 Wave 文件中：

```
from google import genai
from google.genai import types
import wave

# Set up the wave file to save the output:
def wave_file(filename, pcm, channels=1, rate=24000, sample_width=2):
   with wave.open(filename, "wb") as wf:
      wf.setnchannels(channels)
      wf.setsampwidth(sample_width)
      wf.setframerate(rate)
      wf.writeframes(pcm)

client = genai.Client()

response = client.models.generate_content(
   model="gemini-2.5-flash-preview-tts",
   contents="Say cheerfully: Have a wonderful day!",
   config=types.GenerateContentConfig(
      response_modalities=["AUDIO"],
      speech_config=types.SpeechConfig(
         voice_config=types.VoiceConfig(
            prebuilt_voice_config=types.PrebuiltVoiceConfig(
               voice_name='Kore',
            )
         )
      ),
   )
)

data = response.candidates[0].content.parts[0].inline_data.data

file_name='out.wav'
wave_file(file_name, data) # Saves the file to current directory
```

```
import {GoogleGenAI} from '@google/genai';
import wav from 'wav';

async function saveWaveFile(
   filename,
   pcmData,
   channels = 1,
   rate = 24000,
   sampleWidth = 2,
) {
   return new Promise((resolve, reject) => {
      const writer = new wav.FileWriter(filename, {
            channels,
            sampleRate: rate,
            bitDepth: sampleWidth * 8,
      });

      writer.on('finish', resolve);
      writer.on('error', reject);

      writer.write(pcmData);
      writer.end();
   });
}

async function main() {
   const ai = new GoogleGenAI({});

   const response = await ai.models.generateContent({
      model: "gemini-2.5-flash-preview-tts",
      contents: [{ parts: [{ text: 'Say cheerfully: Have a wonderful day!' }] }],
      config: {
            responseModalities: ['AUDIO'],
            speechConfig: {
               voiceConfig: {
                  prebuiltVoiceConfig: { voiceName: 'Kore' },
               },
            },
      },
   });

   const data = response.candidates?.[0]?.content?.parts?.[0]?.inlineData?.data;
   const audioBuffer = Buffer.from(data, 'base64');

   const fileName = 'out.wav';
   await saveWaveFile(fileName, audioBuffer);
}
await main();
```

```
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-tts:generateContent" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
        "contents": [{
          "parts":[{
            "text": "Say cheerfully: Have a wonderful day!"
          }]
        }],
        "generationConfig": {
          "responseModalities": ["AUDIO"],
          "speechConfig": {
            "voiceConfig": {
              "prebuiltVoiceConfig": {
                "voiceName": "Kore"
              }
            }
          }
        },
        "model": "gemini-2.5-flash-preview-tts",
    }' | jq -r '.candidates[0].content.parts[0].inlineData.data' | \
          base64 --decode >out.pcm
# You may need to install ffmpeg.
ffmpeg -f s16le -ar 24000 -ac 1 -i out.pcm out.wav
```

多说话人文字转语音
---------

对于多扬声器音频，您需要一个 `MultiSpeakerVoiceConfig` 对象，其中每个扬声器（最多 2 个）都配置为 `SpeakerVoiceConfig`。您需要使用与[提示](https://ai.google.dev/gemini-api/docs/speech-generation?hl=zh-cn#controllable)中相同的名称来定义每个 `speaker`：

```
from google import genai
from google.genai import types
import wave

# Set up the wave file to save the output:
def wave_file(filename, pcm, channels=1, rate=24000, sample_width=2):
   with wave.open(filename, "wb") as wf:
      wf.setnchannels(channels)
      wf.setsampwidth(sample_width)
      wf.setframerate(rate)
      wf.writeframes(pcm)

client = genai.Client()

prompt = """TTS the following conversation between Joe and Jane:
         Joe: How's it going today Jane?
         Jane: Not too bad, how about you?"""

response = client.models.generate_content(
   model="gemini-2.5-flash-preview-tts",
   contents=prompt,
   config=types.GenerateContentConfig(
      response_modalities=["AUDIO"],
      speech_config=types.SpeechConfig(
         multi_speaker_voice_config=types.MultiSpeakerVoiceConfig(
            speaker_voice_configs=[
               types.SpeakerVoiceConfig(
                  speaker='Joe',
                  voice_config=types.VoiceConfig(
                     prebuilt_voice_config=types.PrebuiltVoiceConfig(
                        voice_name='Kore',
                     )
                  )
               ),
               types.SpeakerVoiceConfig(
                  speaker='Jane',
                  voice_config=types.VoiceConfig(
                     prebuilt_voice_config=types.PrebuiltVoiceConfig(
                        voice_name='Puck',
                     )
                  )
               ),
            ]
         )
      )
   )
)

data = response.candidates[0].content.parts[0].inline_data.data

file_name='out.wav'
wave_file(file_name, data) # Saves the file to current directory
```

```
import {GoogleGenAI} from '@google/genai';
import wav from 'wav';

async function saveWaveFile(
   filename,
   pcmData,
   channels = 1,
   rate = 24000,
   sampleWidth = 2,
) {
   return new Promise((resolve, reject) => {
      const writer = new wav.FileWriter(filename, {
            channels,
            sampleRate: rate,
            bitDepth: sampleWidth * 8,
      });

      writer.on('finish', resolve);
      writer.on('error', reject);

      writer.write(pcmData);
      writer.end();
   });
}

async function main() {
   const ai = new GoogleGenAI({});

   const prompt = `TTS the following conversation between Joe and Jane:
         Joe: How's it going today Jane?
         Jane: Not too bad, how about you?`;

   const response = await ai.models.generateContent({
      model: "gemini-2.5-flash-preview-tts",
      contents: [{ parts: [{ text: prompt }] }],
      config: {
            responseModalities: ['AUDIO'],
            speechConfig: {
               multiSpeakerVoiceConfig: {
                  speakerVoiceConfigs: [
                        {
                           speaker: 'Joe',
                           voiceConfig: {
                              prebuiltVoiceConfig: { voiceName: 'Kore' }
                           }
                        },
                        {
                           speaker: 'Jane',
                           voiceConfig: {
                              prebuiltVoiceConfig: { voiceName: 'Puck' }
                           }
                        }
                  ]
               }
            }
      }
   });

   const data = response.candidates?.[0]?.content?.parts?.[0]?.inlineData?.data;
   const audioBuffer = Buffer.from(data, 'base64');

   const fileName = 'out.wav';
   await saveWaveFile(fileName, audioBuffer);
}

await main();
```

```
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-tts:generateContent" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
  "contents": [{
    "parts":[{
      "text": "TTS the following conversation between Joe and Jane:
                Joe: Hows it going today Jane?
                Jane: Not too bad, how about you?"
    }]
  }],
  "generationConfig": {
    "responseModalities": ["AUDIO"],
    "speechConfig": {
      "multiSpeakerVoiceConfig": {
        "speakerVoiceConfigs": [{
            "speaker": "Joe",
            "voiceConfig": {
              "prebuiltVoiceConfig": {
                "voiceName": "Kore"
              }
            }
          }, {
            "speaker": "Jane",
            "voiceConfig": {
              "prebuiltVoiceConfig": {
                "voiceName": "Puck"
              }
            }
          }]
      }
    }
  },
  "model": "gemini-2.5-flash-preview-tts",
}' | jq -r '.candidates[0].content.parts[0].inlineData.data' | \
    base64 --decode > out.pcm
# You may need to install ffmpeg.
ffmpeg -f s16le -ar 24000 -ac 1 -i out.pcm out.wav
```

使用提示控制说话风格
----------

您可以使用自然语言提示来控制单人或多人 TTS 的风格、语气、口音和语速。 例如，在单音箱提示中，您可以说：

```
Say in an spooky whisper:
"By the pricking of my thumbs...
Something wicked this way comes"
```

在多位发言者的提示中，为模型提供每位发言者的姓名和相应的转写内容。您还可以单独为每个音箱提供指导：

```
Make Speaker1 sound tired and bored, and Speaker2 sound excited and happy:

Speaker1: So... what's on the agenda today?
Speaker2: You're never going to guess!
```

不妨尝试使用与您想要传达的风格或情感相对应的[语音选项](https://ai.google.dev/gemini-api/docs/speech-generation?hl=zh-cn#voices)，以进一步强调。例如，在前面的提示中，_恩克拉多斯_ 的气息声可能强调“疲惫”和“无聊”，而 _Puck_ 的欢快语气可能与“兴奋”和“快乐”相得益彰。

生成用于转换为音频的提示
------------

TTS 模型仅输出音频，但您可以先使用[其他模型](https://ai.google.dev/gemini-api/docs/models?hl=zh-cn)生成转写内容，然后将该转写内容传递给 TTS 模型以进行朗读。

```
from google import genai
from google.genai import types

client = genai.Client()

transcript = client.models.generate_content(
   model="gemini-2.0-flash",
   contents="""Generate a short transcript around 100 words that reads
            like it was clipped from a podcast by excited herpetologists.
            The hosts names are Dr. Anya and Liam.""").text

response = client.models.generate_content(
   model="gemini-2.5-flash-preview-tts",
   contents=transcript,
   config=types.GenerateContentConfig(
      response_modalities=["AUDIO"],
      speech_config=types.SpeechConfig(
         multi_speaker_voice_config=types.MultiSpeakerVoiceConfig(
            speaker_voice_configs=[
               types.SpeakerVoiceConfig(
                  speaker='Dr. Anya',
                  voice_config=types.VoiceConfig(
                     prebuilt_voice_config=types.PrebuiltVoiceConfig(
                        voice_name='Kore',
                     )
                  )
               ),
               types.SpeakerVoiceConfig(
                  speaker='Liam',
                  voice_config=types.VoiceConfig(
                     prebuilt_voice_config=types.PrebuiltVoiceConfig(
                        voice_name='Puck',
                     )
                  )
               ),
            ]
         )
      )
   )
)

# ...Code to stream or save the output
```

```
import { GoogleGenAI } from "@google/genai";

const ai = new GoogleGenAI({});

async function main() {

const transcript = await ai.models.generateContent({
   model: "gemini-2.0-flash",
   contents: "Generate a short transcript around 100 words that reads like it was clipped from a podcast by excited herpetologists. The hosts names are Dr. Anya and Liam.",
   })

const response = await ai.models.generateContent({
   model: "gemini-2.5-flash-preview-tts",
   contents: transcript,
   config: {
      responseModalities: ['AUDIO'],
      speechConfig: {
         multiSpeakerVoiceConfig: {
            speakerVoiceConfigs: [
                   {
                     speaker: "Dr. Anya",
                     voiceConfig: {
                        prebuiltVoiceConfig: {voiceName: "Kore"},
                     }
                  },
                  {
                     speaker: "Liam",
                     voiceConfig: {
                        prebuiltVoiceConfig: {voiceName: "Puck"},
                    }
                  }
                ]
              }
            }
      }
  });
}
// ..JavaScript code for exporting .wav file for output audio

await main();
```

语音选项
----

TTS 模型在 `voice_name` 字段中支持以下 30 种语音选项：

**Zephyr** - _明亮_**Puck** - _欢快_**Charon** - _信息丰富_
**Kore** -- _坚定_**Fenrir** - _Excitable_**Leda** - _青春_
**Orus** - _公司_**Aoede** - _Breezy_**Callirrhoe** - _随和_
**Autonoe** - _明亮_**Enceladus** - _气声_**Iapetus** - _清晰_
**Umbriel** - _随和_**Algieba** - _平滑_**Despina** - _平滑_
**Erinome** - _清除_**Algenib** - _Gravelly_**Rasalgethi** - _信息丰富_
**Laomedeia** - _欢快_**Achernar** - _软_**Alnilam** - _Firm_
**Schedar** - _均匀_**Gacrux** - _成人_**Pulcherrima** - _转发_
**Achird** - _友好_**Zubenelgenubi** -- _随意_**Vindemiatrix** - _温柔_
**Sadachbia** - _活泼_**Sadaltager** - _知识渊博_**Sulafat** - _偏高_

您可以在 [AI Studio](https://aistudio.google.com/generate-speech?hl=zh-cn) 中试听所有语音选项。

支持的语言
-----

TTS 模型会自动检测输入语言。支持以下 24 种语言：

| 语言 | BCP-47 代码 | 语言 | BCP-47 代码 |
| --- | --- | --- | --- |
| 阿拉伯语（埃及语） | `ar-EG` | 德语（德国） | `de-DE` |
| 英语（美国） | `en-US` | 西班牙语（美国） | `es-US` |
| 法语（法国） | `fr-FR` | 印地语（印度） | `hi-IN` |
| 印度尼西亚语（印度尼西亚） | `id-ID` | 意大利语（意大利） | `it-IT` |
| 日语（日本） | `ja-JP` | 韩语（韩国） | `ko-KR` |
| 葡萄牙语（巴西） | `pt-BR` | 俄语（俄罗斯） | `ru-RU` |
| 荷兰语（荷兰） | `nl-NL` | 波兰语（波兰） | `pl-PL` |
| 泰语（泰国） | `th-TH` | 土耳其语（土耳其） | `tr-TR` |
| 越南语（越南） | `vi-VN` | 罗马尼亚语（罗马尼亚） | `ro-RO` |
| 乌克兰语（乌克兰） | `uk-UA` | 孟加拉语（孟加拉） | `bn-BD` |
| 英语（印度） | `en-IN`和`hi-IN`套装 | 马拉地语（印度） | `mr-IN` |
| 泰米尔语（印度） | `ta-IN` | 泰卢固语（印度） | `te-IN` |

支持的模型
-----

| 型号 | 一位说话者 | 多扬声器 |
| --- | --- | --- |
| [Gemini 2.5 Flash 预览版 TTS](https://ai.google.dev/gemini-api/docs/models?hl=zh-cn#gemini-2.5-flash-preview-tts) | ✔️ | ✔️ |
| [Gemini 2.5 Pro 预览版 TTS](https://ai.google.dev/gemini-api/docs/models?hl=zh-cn#gemini-2.5-pro-preview-tts) | ✔️ | ✔️ |

限制
--

*   TTS 模型只能接收文本输入并生成音频输出。
*   TTS 会话的[上下文窗口](https://ai.google.dev/gemini-api/docs/long-context?hl=zh-cn)限制为 3.2 万个 token。
*   如需了解语言支持，请参阅[语言](https://ai.google.dev/gemini-api/docs/speech-generation?hl=zh-cn#languages)部分。

后续步骤
----

*   不妨试试[音频生成实战宝典](https://colab.research.google.com/github/google-gemini/cookbook/blob/main/quickstarts/Get_started_TTS.ipynb?hl=zh-cn)。
*   Gemini 的 [Live API](https://ai.google.dev/gemini-api/docs/live?hl=zh-cn) 提供交互式音频生成选项，您可以将其与其他模态交织使用。
*   如需了解如何处理音频 _输入_，请参阅[音频理解](https://ai.google.dev/gemini-api/docs/audio?hl=zh-cn)指南。

如未另行说明，那么本页面中的内容已根据[知识共享署名 4.0 许可](https://creativecommons.org/licenses/by/4.0/)获得了许可，并且代码示例已根据 [Apache 2.0 许可](https://www.apache.org/licenses/LICENSE-2.0)获得了许可。有关详情，请参阅 [Google 开发者网站政策](https://developers.google.com/site-policies?hl=zh-cn)。Java 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2025-08-01。
a