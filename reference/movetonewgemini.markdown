Title: 迁移到 Google GenAI SDK

URL Source: https://ai.google.dev/gemini-api/docs/migrate?hl=zh-cn

Published Time: Fri, 01 Aug 2025 17:39:05 GMT

Markdown Content:
[跳至主要内容](https://ai.google.dev/gemini-api/docs/migrate?hl=zh-cn#main-content)

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

*   本页内容
*   [安装](https://ai.google.dev/gemini-api/docs/migrate?hl=zh-cn#install-sdk)
*   [API 访问权限](https://ai.google.dev/gemini-api/docs/migrate?hl=zh-cn#client)
*   [身份验证](https://ai.google.dev/gemini-api/docs/migrate?hl=zh-cn#authenticate)
*   [生成内容](https://ai.google.dev/gemini-api/docs/migrate?hl=zh-cn#generate-content)
    *   [文本](https://ai.google.dev/gemini-api/docs/migrate?hl=zh-cn#text)
    *   [图片](https://ai.google.dev/gemini-api/docs/migrate?hl=zh-cn#image)
    *   [流式](https://ai.google.dev/gemini-api/docs/migrate?hl=zh-cn#streaming)

*   [配置](https://ai.google.dev/gemini-api/docs/migrate?hl=zh-cn#configuration)
*   [安全设置](https://ai.google.dev/gemini-api/docs/migrate?hl=zh-cn#safety-settings)
*   [异步](https://ai.google.dev/gemini-api/docs/migrate?hl=zh-cn#async)
*   [聊天](https://ai.google.dev/gemini-api/docs/migrate?hl=zh-cn#chat)
*   [函数调用](https://ai.google.dev/gemini-api/docs/migrate?hl=zh-cn#function-calling)
    *   [自动函数调用](https://ai.google.dev/gemini-api/docs/migrate?hl=zh-cn#automatic-function)

*   [代码执行](https://ai.google.dev/gemini-api/docs/migrate?hl=zh-cn#code-execution)
*   [搜索接地](https://ai.google.dev/gemini-api/docs/migrate?hl=zh-cn#search-grounding)
*   [JSON 响应](https://ai.google.dev/gemini-api/docs/migrate?hl=zh-cn#json-response)
*   [文件](https://ai.google.dev/gemini-api/docs/migrate?hl=zh-cn#files)
    *   [上传](https://ai.google.dev/gemini-api/docs/migrate?hl=zh-cn#upload)
    *   [列出和获取](https://ai.google.dev/gemini-api/docs/migrate?hl=zh-cn#list-and-get)
    *   [删除](https://ai.google.dev/gemini-api/docs/migrate?hl=zh-cn#delete)

*   [上下文缓存](https://ai.google.dev/gemini-api/docs/migrate?hl=zh-cn#context-caching)
*   [统计 token 数量](https://ai.google.dev/gemini-api/docs/migrate?hl=zh-cn#count-tokens)
*   [生成图片](https://ai.google.dev/gemini-api/docs/migrate?hl=zh-cn#generate-images)
*   [嵌入内容](https://ai.google.dev/gemini-api/docs/migrate?hl=zh-cn#embed-content)
*   [调整模型](https://ai.google.dev/gemini-api/docs/migrate?hl=zh-cn#tune-model)

自 2024 年末发布的 Gemini 2.0 开始，我们推出了一组名为 [Google GenAI SDK](https://ai.google.dev/gemini-api/docs/libraries?hl=zh-cn) 的新库。它通过[更新的客户端架构](https://ai.google.dev/gemini-api/docs/migrate?hl=zh-cn#client)提供改进的开发者体验，并[简化开发者工作流程与企业工作流程之间的过渡](https://ai.google.dev/gemini-api/docs/migrate-to-cloud?hl=zh-cn)。

Google GenAI SDK 现已在所有受支持的平台上[正式发布 (GA)](https://ai.google.dev/gemini-api/docs/libraries?hl=zh-cn#new-libraries)。如果您使用的是我们的某个[旧版库](https://ai.google.dev/gemini-api/docs/libraries?hl=zh-cn#previous-sdks)，我们强烈建议您进行迁移。

本指南提供了迁移前后的代码示例，可帮助您入门。

安装
--

**之前**

```
pip install -U -q "google-generativeai"
```

```
npm install @google/generative-ai
```

```
go get github.com/google/generative-ai-go
```

**之后**

```
pip install -U -q "google-genai"
```

```
npm install @google/genai
```

```
go get google.golang.org/genai
```

API 访问权限
--------

旧版 SDK 使用各种临时方法在后台隐式处理 API 客户端。这使得管理客户端和凭据变得困难。 现在，您可以通过中央 `Client` 对象进行互动。此 `Client` 对象充当各种 API 服务（例如，`models`、`chats`、`files`、`tunings`），从而提高一致性并简化不同 API 调用中的凭据和配置管理。

**之前（API 访问权限不太集中）**

旧版 SDK 未明确使用顶级客户端对象来处理大多数 API 调用。您将直接实例化 `GenerativeModel` 对象并与之交互。

```
import google.generativeai as genai

# Directly create and use model objects
model = genai.GenerativeModel('gemini-1.5-flash')
response = model.generate_content(...)
chat = model.start_chat(...)
```

虽然 `GoogleGenerativeAI` 是模型和聊天功能的中心点，但文件和缓存管理等其他功能通常需要导入和实例化完全独立的客户端类。

```
import { GoogleGenerativeAI } from "@google/generative-ai";
import { GoogleAIFileManager, GoogleAICacheManager } from "@google/generative-ai/server"; // For files/caching

const genAI = new GoogleGenerativeAI("YOUR_API_KEY");
const fileManager = new GoogleAIFileManager("YOUR_API_KEY");
const cacheManager = new GoogleAICacheManager("YOUR_API_KEY");

// Get a model instance, then call methods on it
const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });
const result = await model.generateContent(...);
const chat = model.startChat(...);

// Call methods on separate client objects for other services
const uploadedFile = await fileManager.uploadFile(...);
const cache = await cacheManager.create(...);
```

`genai.NewClient` 函数创建了一个客户端，但生成模型操作通常是在从该客户端获得的单独 `GenerativeModel` 实例上调用的。其他服务可能通过不同的软件包或模式进行访问。

```
import (
      "github.com/google/generative-ai-go/genai"
      "github.com/google/generative-ai-go/genai/fileman" // For files
      "google.golang.org/api/option"
)

client, err := genai.NewClient(ctx, option.WithAPIKey("YOUR_API_KEY"))
fileClient, err := fileman.NewClient(ctx, option.WithAPIKey("YOUR_API_KEY"))

// Get a model instance, then call methods on it
model := client.GenerativeModel("gemini-1.5-flash")
resp, err := model.GenerateContent(...)
cs := model.StartChat()

// Call methods on separate client objects for other services
uploadedFile, err := fileClient.UploadFile(...)
```

**之后（集中式客户端对象）**

```
from google import genai

# Create a single client object
client = genai.Client()

# Access API methods through services on the client object
response = client.models.generate_content(...)
chat = client.chats.create(...)
my_file = client.files.upload(...)
tuning_job = client.tunings.tune(...)
```

```
import { GoogleGenAI } from "@google/genai";

// Create a single client object
const ai = new GoogleGenAI({apiKey: "YOUR_API_KEY"});

// Access API methods through services on the client object
const response = await ai.models.generateContent(...);
const chat = ai.chats.create(...);
const uploadedFile = await ai.files.upload(...);
const cache = await ai.caches.create(...);
```

```
import "google.golang.org/genai"

// Create a single client object
client, err := genai.NewClient(ctx, nil)

// Access API methods through services on the client object
result, err := client.Models.GenerateContent(...)
chat, err := client.Chats.Create(...)
uploadedFile, err := client.Files.Upload(...)
tuningJob, err := client.Tunings.Tune(...)
```

身份验证
----

旧版库和新版库均使用 API 密钥进行身份验证。您可以在 Google AI Studio 中[创建](https://aistudio.google.com/app/apikey?hl=zh-cn) API 密钥。

**之前**

旧版 SDK 会隐式处理 API 客户端对象。

```
import google.generativeai as genai

genai.configure(api_key=...)
```

```
import { GoogleGenerativeAI } from "@google/generative-ai";

const genAI = new GoogleGenerativeAI("GOOGLE_API_KEY");
```

导入 Google 库：

```
import (
      "github.com/google/generative-ai-go/genai"
      "google.golang.org/api/option"
)
```

创建客户端：

```
client, err := genai.NewClient(ctx, option.WithAPIKey("GOOGLE_API_KEY"))
```

**之后**

借助 Google GenAI SDK，您可以先创建一个 API 客户端，然后使用该客户端调用 API。 如果您未向客户端传递 API 密钥，新 SDK 将从 `GEMINI_API_KEY` 或 `GOOGLE_API_KEY` 环境变量中获取您的 API 密钥。

```
export GEMINI_API_KEY="YOUR_API_KEY"
```

```
from google import genai

client = genai.Client() # Set the API key using the GEMINI_API_KEY env var.
                        # Alternatively, you could set the API key explicitly:
                        # client = genai.Client(api_key="your_api_key")
```

```
import { GoogleGenAI } from "@google/genai";

const ai = new GoogleGenAI({apiKey: "GEMINI_API_KEY"});
```

导入 GenAI 库：

```
import "google.golang.org/genai"
```

创建客户端：

```
client, err := genai.NewClient(ctx, &genai.ClientConfig{
        Backend:  genai.BackendGeminiAPI,
})
```

生成内容
----

### 文本

**之前**

之前，没有客户端对象，您可以通过 `GenerativeModel` 对象直接访问 API。

```
import google.generativeai as genai

model = genai.GenerativeModel('gemini-1.5-flash')
response = model.generate_content(
    'Tell me a story in 300 words'
)
print(response.text)
```

```
import { GoogleGenerativeAI } from "@google/generative-ai";

const genAI = new GoogleGenerativeAI(process.env.API_KEY);
const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });
const prompt = "Tell me a story in 300 words";

const result = await model.generateContent(prompt);
console.log(result.response.text());
```

```
ctx := context.Background()
client, err := genai.NewClient(ctx, option.WithAPIKey("GOOGLE_API_KEY"))
if err != nil {
    log.Fatal(err)
}
defer client.Close()

model := client.GenerativeModel("gemini-1.5-flash")
resp, err := model.GenerateContent(ctx, genai.Text("Tell me a story in 300 words."))
if err != nil {
    log.Fatal(err)
}

printResponse(resp) // utility for printing response parts
```

**之后**

新的 Google GenAI SDK 通过 `Client` 对象提供对所有 API 方法的访问权限。除了少数有状态的特殊情况（`chat` 和实时 API `session`），这些都是无状态函数。为了实用性和一致性，返回的对象是 `pydantic` 类。

```
from google import genai
client = genai.Client()

response = client.models.generate_content(
    model='gemini-2.0-flash',
    contents='Tell me a story in 300 words.'
)
print(response.text)

print(response.model_dump_json(
    exclude_none=True, indent=4))
```

```
import { GoogleGenAI } from "@google/genai";

const ai = new GoogleGenAI({ apiKey: "GOOGLE_API_KEY" });

const response = await ai.models.generateContent({
  model: "gemini-2.0-flash",
  contents: "Tell me a story in 300 words.",
});
console.log(response.text);
```

```
ctx := context.Background()
  client, err := genai.NewClient(ctx, nil)
if err != nil {
    log.Fatal(err)
}

result, err := client.Models.GenerateContent(ctx, "gemini-2.0-flash", genai.Text("Tell me a story in 300 words."), nil)
if err != nil {
    log.Fatal(err)
}
debugPrint(result) // utility for printing result
```

### 图片

**之前**

```
import google.generativeai as genai

model = genai.GenerativeModel('gemini-1.5-flash')
response = model.generate_content([
    'Tell me a story based on this image',
    Image.open(image_path)
])
print(response.text)
```

```
import { GoogleGenerativeAI } from "@google/generative-ai";

const genAI = new GoogleGenerativeAI("GOOGLE_API_KEY");
const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });

function fileToGenerativePart(path, mimeType) {
  return {
    inlineData: {
      data: Buffer.from(fs.readFileSync(path)).toString("base64"),
      mimeType,
    },
  };
}

const prompt = "Tell me a story based on this image";

const imagePart = fileToGenerativePart(
  `path/to/organ.jpg`,
  "image/jpeg",
);

const result = await model.generateContent([prompt, imagePart]);
console.log(result.response.text());
```

```
ctx := context.Background()
client, err := genai.NewClient(ctx, option.WithAPIKey("GOOGLE_API_KEY"))
if err != nil {
    log.Fatal(err)
}
defer client.Close()

model := client.GenerativeModel("gemini-1.5-flash")

imgData, err := os.ReadFile("path/to/organ.jpg")
if err != nil {
    log.Fatal(err)
}

resp, err := model.GenerateContent(ctx,
    genai.Text("Tell me about this instrument"),
    genai.ImageData("jpeg", imgData))
if err != nil {
    log.Fatal(err)
}

printResponse(resp) // utility for printing response
```

**之后**

新版 SDK 中包含许多相同的便利功能。例如，系统会自动转换 `PIL.Image` 对象。

```
from google import genai
from PIL import Image

client = genai.Client()

response = client.models.generate_content(
    model='gemini-2.0-flash',
    contents=[
        'Tell me a story based on this image',
        Image.open(image_path)
    ]
)
print(response.text)
```

```
import {GoogleGenAI} from '@google/genai';

const ai = new GoogleGenAI({ apiKey: "GOOGLE_API_KEY" });

const organ = await ai.files.upload({
  file: "path/to/organ.jpg",
});

const response = await ai.models.generateContent({
  model: "gemini-2.0-flash",
  contents: [
    createUserContent([
      "Tell me a story based on this image",
      createPartFromUri(organ.uri, organ.mimeType)
    ]),
  ],
});
console.log(response.text);
```

```
ctx := context.Background()
client, err := genai.NewClient(ctx, nil)
if err != nil {
    log.Fatal(err)
}

imgData, err := os.ReadFile("path/to/organ.jpg")
if err != nil {
    log.Fatal(err)
}

parts := []*genai.Part{
    {Text: "Tell me a story based on this image"},
    {InlineData: &genai.Blob{Data: imgData, MIMEType: "image/jpeg"}},
}
contents := []*genai.Content{
    {Parts: parts},
}

result, err := client.Models.GenerateContent(ctx, "gemini-2.0-flash", contents, nil)
if err != nil {
    log.Fatal(err)
}
debugPrint(result) // utility for printing result
```

### 流式

**之前**

```
import google.generativeai as genai

response = model.generate_content(
    "Write a cute story about cats.",
    stream=True)
for chunk in response:
    print(chunk.text)
```

```
import { GoogleGenerativeAI } from "@google/generative-ai";

const genAI = new GoogleGenerativeAI("GOOGLE_API_KEY");
const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });

const prompt = "Write a story about a magic backpack.";

const result = await model.generateContentStream(prompt);

// Print text as it comes in.
for await (const chunk of result.stream) {
  const chunkText = chunk.text();
  process.stdout.write(chunkText);
}
```

```
ctx := context.Background()
client, err := genai.NewClient(ctx, option.WithAPIKey("GOOGLE_API_KEY"))
if err != nil {
    log.Fatal(err)
}
defer client.Close()

model := client.GenerativeModel("gemini-1.5-flash")
iter := model.GenerateContentStream(ctx, genai.Text("Write a story about a magic backpack."))
for {
    resp, err := iter.Next()
    if err == iterator.Done {
        break
    }
    if err != nil {
        log.Fatal(err)
    }
    printResponse(resp) // utility for printing the response
}
```

**之后**

```
from google import genai

client = genai.Client()

for chunk in client.models.generate_content_stream(
  model='gemini-2.0-flash',
  contents='Tell me a story in 300 words.'
):
    print(chunk.text)
```

```
import {GoogleGenAI} from '@google/genai';

const ai = new GoogleGenAI({ apiKey: "GOOGLE_API_KEY" });

const response = await ai.models.generateContentStream({
  model: "gemini-2.0-flash",
  contents: "Write a story about a magic backpack.",
});
let text = "";
for await (const chunk of response) {
  console.log(chunk.text);
  text += chunk.text;
}
```

```
ctx := context.Background()
client, err := genai.NewClient(ctx, nil)
if err != nil {
    log.Fatal(err)
}

for result, err := range client.Models.GenerateContentStream(
    ctx,
    "gemini-2.0-flash",
    genai.Text("Write a story about a magic backpack."),
    nil,
) {
    if err != nil {
        log.Fatal(err)
    }
    fmt.Print(result.Candidates[0].Content.Parts[0].Text)
}
```

配置
--

**之前**

```
import google.generativeai as genai

model = genai.GenerativeModel(
  'gemini-1.5-flash',
    system_instruction='you are a story teller for kids under 5 years old',
    generation_config=genai.GenerationConfig(
      max_output_tokens=400,
      top_k=2,
      top_p=0.5,
      temperature=0.5,
      response_mime_type='application/json',
      stop_sequences=['\n'],
    )
)
response = model.generate_content('tell me a story in 100 words')
```

```
import { GoogleGenerativeAI } from "@google/generative-ai";

const genAI = new GoogleGenerativeAI("GOOGLE_API_KEY");
const model = genAI.getGenerativeModel({
  model: "gemini-1.5-flash",
  generationConfig: {
    candidateCount: 1,
    stopSequences: ["x"],
    maxOutputTokens: 20,
    temperature: 1.0,
  },
});

const result = await model.generateContent(
  "Tell me a story about a magic backpack.",
);
console.log(result.response.text())
```

```
ctx := context.Background()
client, err := genai.NewClient(ctx, option.WithAPIKey("GOOGLE_API_KEY"))
if err != nil {
    log.Fatal(err)
}
defer client.Close()

model := client.GenerativeModel("gemini-1.5-flash")
model.SetTemperature(0.5)
model.SetTopP(0.5)
model.SetTopK(2.0)
model.SetMaxOutputTokens(100)
model.ResponseMIMEType = "application/json"
resp, err := model.GenerateContent(ctx, genai.Text("Tell me about New York"))
if err != nil {
    log.Fatal(err)
}
printResponse(resp) // utility for printing response
```

**之后**

对于新 SDK 中的所有方法，必需实参都以关键字实参的形式提供。所有可选输入都通过 `config` 实参提供。配置实参可以指定为 Python 字典或 `google.genai.types` 命名空间中的 `Config` 类。为了实现实用性和一致性，`types` 模块中的所有定义都是 `pydantic` 类。

```
from google import genai
from google.genai import types

client = genai.Client()

response = client.models.generate_content(
  model='gemini-2.0-flash',
  contents='Tell me a story in 100 words.',
  config=types.GenerateContentConfig(
      system_instruction='you are a story teller for kids under 5 years old',
      max_output_tokens= 400,
      top_k= 2,
      top_p= 0.5,
      temperature= 0.5,
      response_mime_type= 'application/json',
      stop_sequences= ['\n'],
      seed=42,
  ),
)
```

```
import {GoogleGenAI} from '@google/genai';

const ai = new GoogleGenAI({ apiKey: "GOOGLE_API_KEY" });

const response = await ai.models.generateContent({
  model: "gemini-2.0-flash",
  contents: "Tell me a story about a magic backpack.",
  config: {
    candidateCount: 1,
    stopSequences: ["x"],
    maxOutputTokens: 20,
    temperature: 1.0,
  },
});

console.log(response.text);
```

```
ctx := context.Background()
client, err := genai.NewClient(ctx, nil)
if err != nil {
    log.Fatal(err)
}

result, err := client.Models.GenerateContent(ctx,
    "gemini-2.0-flash",
    genai.Text("Tell me about New York"),
    &genai.GenerateContentConfig{
        Temperature:      genai.Ptr[float32](0.5),
        TopP:             genai.Ptr[float32](0.5),
        TopK:             genai.Ptr[float32](2.0),
        ResponseMIMEType: "application/json",
        StopSequences:    []string{"Yankees"},
        CandidateCount:   2,
        Seed:             genai.Ptr[int32](42),
        MaxOutputTokens:  128,
        PresencePenalty:  genai.Ptr[float32](0.5),
        FrequencyPenalty: genai.Ptr[float32](0.5),
    },
)
if err != nil {
    log.Fatal(err)
}
debugPrint(result) // utility for printing response
```

安全设置
----

生成包含安全设置的回答：

**之前**

```
import google.generativeai as genai

model = genai.GenerativeModel('gemini-1.5-flash')
response = model.generate_content(
    'say something bad',
    safety_settings={
        'HATE': 'BLOCK_ONLY_HIGH',
        'HARASSMENT': 'BLOCK_ONLY_HIGH',
  }
)
```

```
import { GoogleGenerativeAI, HarmCategory, HarmBlockThreshold } from "@google/generative-ai";

const genAI = new GoogleGenerativeAI("GOOGLE_API_KEY");
const model = genAI.getGenerativeModel({
  model: "gemini-1.5-flash",
  safetySettings: [
    {
      category: HarmCategory.HARM_CATEGORY_HARASSMENT,
      threshold: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    },
  ],
});

const unsafePrompt =
  "I support Martians Soccer Club and I think " +
  "Jupiterians Football Club sucks! Write an ironic phrase telling " +
  "them how I feel about them.";

const result = await model.generateContent(unsafePrompt);

try {
  result.response.text();
} catch (e) {
  console.error(e);
  console.log(result.response.candidates[0].safetyRatings);
}
```

**之后**

```
from google import genai
from google.genai import types

client = genai.Client()

response = client.models.generate_content(
  model='gemini-2.0-flash',
  contents='say something bad',
  config=types.GenerateContentConfig(
      safety_settings= [
          types.SafetySetting(
              category='HARM_CATEGORY_HATE_SPEECH',
              threshold='BLOCK_ONLY_HIGH'
          ),
      ]
  ),
)
```

```
import {GoogleGenAI} from '@google/genai';

const ai = new GoogleGenAI({ apiKey: "GOOGLE_API_KEY" });
const unsafePrompt =
  "I support Martians Soccer Club and I think " +
  "Jupiterians Football Club sucks! Write an ironic phrase telling " +
  "them how I feel about them.";

const response = await ai.models.generateContent({
  model: "gemini-2.0-flash",
  contents: unsafePrompt,
  config: {
    safetySettings: [
      {
        category: "HARM_CATEGORY_HARASSMENT",
        threshold: "BLOCK_ONLY_HIGH",
      },
    ],
  },
});

console.log("Finish reason:", response.candidates[0].finishReason);
console.log("Safety ratings:", response.candidates[0].safetyRatings);
```

异步
--

**之前**

```
import google.generativeai as genai

model = genai.GenerativeModel('gemini-1.5-flash')
response = model.generate_content_async(
    'tell me a story in 100 words'
)
```

**之后**

如需将新 SDK 与 `asyncio` 搭配使用，请在 `client.aio` 下单独实现每个方法 `async`。

```
from google import genai

client = genai.Client()

response = await client.aio.models.generate_content(
    model='gemini-2.0-flash',
    contents='Tell me a story in 300 words.'
)
```

聊天
--

开始聊天并向模型发送消息：

**之前**

```
import google.generativeai as genai

model = genai.GenerativeModel('gemini-1.5-flash')
chat = model.start_chat()

response = chat.send_message(
    "Tell me a story in 100 words")
response = chat.send_message(
    "What happened after that?")
```

```
import { GoogleGenerativeAI } from "@google/generative-ai";

const genAI = new GoogleGenerativeAI("GOOGLE_API_KEY");
const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });
const chat = model.startChat({
  history: [
    {
      role: "user",
      parts: [{ text: "Hello" }],
    },
    {
      role: "model",
      parts: [{ text: "Great to meet you. What would you like to know?" }],
    },
  ],
});
let result = await chat.sendMessage("I have 2 dogs in my house.");
console.log(result.response.text());
result = await chat.sendMessage("How many paws are in my house?");
console.log(result.response.text());
```

```
ctx := context.Background()
client, err := genai.NewClient(ctx, option.WithAPIKey("GOOGLE_API_KEY"))
if err != nil {
    log.Fatal(err)
}
defer client.Close()

model := client.GenerativeModel("gemini-1.5-flash")
cs := model.StartChat()

cs.History = []*genai.Content{
    {
        Parts: []genai.Part{
            genai.Text("Hello, I have 2 dogs in my house."),
        },
        Role: "user",
    },
    {
        Parts: []genai.Part{
            genai.Text("Great to meet you. What would you like to know?"),
        },
        Role: "model",
    },
}

res, err := cs.SendMessage(ctx, genai.Text("How many paws are in my house?"))
if err != nil {
    log.Fatal(err)
}
printResponse(res) // utility for printing the response
```

**之后**

```
from google import genai

client = genai.Client()

chat = client.chats.create(model='gemini-2.0-flash')

response = chat.send_message(
    message='Tell me a story in 100 words')
response = chat.send_message(
    message='What happened after that?')
```

```
import {GoogleGenAI} from '@google/genai';

const ai = new GoogleGenAI({ apiKey: "GOOGLE_API_KEY" });
const chat = ai.chats.create({
  model: "gemini-2.0-flash",
  history: [
    {
      role: "user",
      parts: [{ text: "Hello" }],
    },
    {
      role: "model",
      parts: [{ text: "Great to meet you. What would you like to know?" }],
    },
  ],
});

const response1 = await chat.sendMessage({
  message: "I have 2 dogs in my house.",
});
console.log("Chat response 1:", response1.text);

const response2 = await chat.sendMessage({
  message: "How many paws are in my house?",
});
console.log("Chat response 2:", response2.text);
```

```
ctx := context.Background()
client, err := genai.NewClient(ctx, nil)
if err != nil {
    log.Fatal(err)
}

chat, err := client.Chats.Create(ctx, "gemini-2.0-flash", nil, nil)
if err != nil {
    log.Fatal(err)
}

result, err := chat.SendMessage(ctx, genai.Part{Text: "Hello, I have 2 dogs in my house."})
if err != nil {
    log.Fatal(err)
}
debugPrint(result) // utility for printing result

result, err = chat.SendMessage(ctx, genai.Part{Text: "How many paws are in my house?"})
if err != nil {
    log.Fatal(err)
}
debugPrint(result) // utility for printing result
```

函数调用
----

**之前**

```
import google.generativeai as genai
from enum import Enum

def get_current_weather(location: str) -> str:
    """Get the current whether in a given location.

    Args:
        location: required, The city and state, e.g. San Franciso, CA
        unit: celsius or fahrenheit
    """
    print(f'Called with: {location=}')
    return "23C"

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    tools=[get_current_weather]
)

response = model.generate_content("What is the weather in San Francisco?")
function_call = response.candidates[0].parts[0].function_call
```

**之后**

在新 SDK 中，自动函数调用是默认设置。在此处，您可以停用该功能。

```
from google import genai
from google.genai import types

client = genai.Client()

def get_current_weather(location: str) -> str:
    """Get the current whether in a given location.

    Args:
        location: required, The city and state, e.g. San Franciso, CA
        unit: celsius or fahrenheit
    """
    print(f'Called with: {location=}')
    return "23C"

response = client.models.generate_content(
  model='gemini-2.0-flash',
  contents="What is the weather like in Boston?",
  config=types.GenerateContentConfig(
      tools=[get_current_weather],
      automatic_function_calling={'disable': True},
  ),
)

function_call = response.candidates[0].content.parts[0].function_call
```

### 自动函数调用

**之前**

旧版 SDK 仅支持在聊天中自动调用函数。在新版 SDK 中，这是 `generate_content` 中的默认行为。

```
import google.generativeai as genai

def get_current_weather(city: str) -> str:
    return "23C"

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    tools=[get_current_weather]
)

chat = model.start_chat(
    enable_automatic_function_calling=True)
result = chat.send_message("What is the weather in San Francisco?")
```

**之后**

```
from google import genai
from google.genai import types
client = genai.Client()

def get_current_weather(city: str) -> str:
    return "23C"

response = client.models.generate_content(
  model='gemini-2.0-flash',
  contents="What is the weather like in Boston?",
  config=types.GenerateContentConfig(
      tools=[get_current_weather]
  ),
)
```

代码执行
----

代码执行是一种工具，可让模型生成 Python 代码、运行代码并返回结果。

**之前**

```
import google.generativeai as genai

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    tools="code_execution"
)

result = model.generate_content(
  "What is the sum of the first 50 prime numbers? Generate and run code for "
  "the calculation, and make sure you get all 50.")
```

```
import { GoogleGenerativeAI } from "@google/generative-ai";

const genAI = new GoogleGenerativeAI("GOOGLE_API_KEY");
const model = genAI.getGenerativeModel({
  model: "gemini-1.5-flash",
  tools: [{ codeExecution: {} }],
});

const result = await model.generateContent(
  "What is the sum of the first 50 prime numbers? " +
    "Generate and run code for the calculation, and make sure you get " +
    "all 50.",
);

console.log(result.response.text());
```

**之后**

```
from google import genai
from google.genai import types

client = genai.Client()

response = client.models.generate_content(
    model='gemini-2.0-flash',
    contents='What is the sum of the first 50 prime numbers? Generate and run '
            'code for the calculation, and make sure you get all 50.',
    config=types.GenerateContentConfig(
        tools=[types.Tool(code_execution=types.ToolCodeExecution)],
    ),
)
```

```
import {GoogleGenAI} from '@google/genai';

const ai = new GoogleGenAI({ apiKey: "GOOGLE_API_KEY" });

const response = await ai.models.generateContent({
  model: "gemini-2.0-pro-exp-02-05",
  contents: `Write and execute code that calculates the sum of the first 50 prime numbers.
            Ensure that only the executable code and its resulting output are generated.`,
});

// Each part may contain text, executable code, or an execution result.
for (const part of response.candidates[0].content.parts) {
  console.log(part);
  console.log("\n");
}

console.log("-".repeat(80));
// The `.text` accessor concatenates the parts into a markdown-formatted text.
console.log("\n", response.text);
```

搜索接地
----

`GoogleSearch`（Gemini>=2.0）和 `GoogleSearchRetrieval`（Gemini < 2.0）是可让模型检索公开网络数据以进行接地（由 Google 提供支持）的工具。

**之前**

```
import google.generativeai as genai

model = genai.GenerativeModel('gemini-1.5-flash')
response = model.generate_content(
    contents="what is the Google stock price?",
    tools='google_search_retrieval'
)
```

**之后**

```
from google import genai
from google.genai import types

client = genai.Client()

response = client.models.generate_content(
    model='gemini-2.0-flash',
    contents='What is the Google stock price?',
    config=types.GenerateContentConfig(
        tools=[
            types.Tool(
                google_search=types.GoogleSearch()
            )
        ]
    )
)
```

JSON 响应
-------

以 JSON 格式生成答案。

**之前**

通过指定 `response_schema` 并设置 `response_mime_type="application/json"`，用户可以限制模型生成遵循给定结构的 `JSON` 回答。

```
import google.generativeai as genai
import typing_extensions as typing

class CountryInfo(typing.TypedDict):
    name: str
    population: int
    capital: str
    continent: str
    major_cities: list[str]
    gdp: int
    official_language: str
    total_area_sq_mi: int

model = genai.GenerativeModel(model_name="gemini-1.5-flash")
result = model.generate_content(
    "Give me information of the United States",
    generation_config=genai.GenerationConfig(
        response_mime_type="application/json",
        response_schema = CountryInfo
    ),
)
```

```
import { GoogleGenerativeAI, SchemaType } from "@google/generative-ai";

const genAI = new GoogleGenerativeAI("GOOGLE_API_KEY");

const schema = {
  description: "List of recipes",
  type: SchemaType.ARRAY,
  items: {
    type: SchemaType.OBJECT,
    properties: {
      recipeName: {
        type: SchemaType.STRING,
        description: "Name of the recipe",
        nullable: false,
      },
    },
    required: ["recipeName"],
  },
};

const model = genAI.getGenerativeModel({
  model: "gemini-1.5-pro",
  generationConfig: {
    responseMimeType: "application/json",
    responseSchema: schema,
  },
});

const result = await model.generateContent(
  "List a few popular cookie recipes.",
);
console.log(result.response.text());
```

**之后**

新版 SDK 使用 `pydantic` 类来提供架构（不过您可以传递 `genai.types.Schema` 或等效的 `dict`）。如果可能，SDK 会解析返回的 JSON，并以 `response.parsed` 形式返回结果。如果您提供 `pydantic` 类作为架构，SDK 会将该 `JSON` 转换为该类的实例。

```
from google import genai
from pydantic import BaseModel

client = genai.Client()

class CountryInfo(BaseModel):
    name: str
    population: int
    capital: str
    continent: str
    major_cities: list[str]
    gdp: int
    official_language: str
    total_area_sq_mi: int

response = client.models.generate_content(
    model='gemini-2.0-flash',
    contents='Give me information of the United States.',
    config={
        'response_mime_type': 'application/json',
        'response_schema': CountryInfo,
    },
)

response.parsed
```

```
import {GoogleGenAI} from '@google/genai';

const ai = new GoogleGenAI({ apiKey: "GOOGLE_API_KEY" });
const response = await ai.models.generateContent({
  model: "gemini-2.0-flash",
  contents: "List a few popular cookie recipes.",
  config: {
    responseMimeType: "application/json",
    responseSchema: {
      type: "array",
      items: {
        type: "object",
        properties: {
          recipeName: { type: "string" },
          ingredients: { type: "array", items: { type: "string" } },
        },
        required: ["recipeName", "ingredients"],
      },
    },
  },
});
console.log(response.text);
```

文件
--

### 上传

上传文件：

**之前**

```
import requests
import pathlib
import google.generativeai as genai

# Download file
response = requests.get(
    'https://storage.googleapis.com/generativeai-downloads/data/a11.txt')
pathlib.Path('a11.txt').write_text(response.text)

file = genai.upload_file(path='a11.txt')

model = genai.GenerativeModel('gemini-1.5-flash')
response = model.generate_content([
    'Can you summarize this file:',
    my_file
])
print(response.text)
```

**之后**

```
import requests
import pathlib
from google import genai

client = genai.Client()

# Download file
response = requests.get(
    'https://storage.googleapis.com/generativeai-downloads/data/a11.txt')
pathlib.Path('a11.txt').write_text(response.text)

my_file = client.files.upload(file='a11.txt')

response = client.models.generate_content(
    model='gemini-2.0-flash',
    contents=[
        'Can you summarize this file:',
        my_file
    ]
)
print(response.text)
```

### 列出和获取

列出已上传的文件并获取具有特定文件名的已上传文件：

**之前**

```
import google.generativeai as genai

for file in genai.list_files():
  print(file.name)

file = genai.get_file(name=file.name)
```

**之后**

```
from google import genai
client = genai.Client()

for file in client.files.list():
    print(file.name)

file = client.files.get(name=file.name)
```

### 删除

删除文件：

**之前**

```
import pathlib
import google.generativeai as genai

pathlib.Path('dummy.txt').write_text(dummy)
dummy_file = genai.upload_file(path='dummy.txt')

file = genai.delete_file(name=dummy_file.name)
```

**之后**

```
import pathlib
from google import genai

client = genai.Client()

pathlib.Path('dummy.txt').write_text(dummy)
dummy_file = client.files.upload(file='dummy.txt')

response = client.files.delete(name=dummy_file.name)
```

上下文缓存
-----

借助上下文缓存，用户只需将内容传递给模型一次，即可缓存输入 token，然后在后续调用中引用缓存的 token，从而降低费用。

**之前**

```
import requests
import pathlib
import google.generativeai as genai
from google.generativeai import caching

# Download file
response = requests.get(
    'https://storage.googleapis.com/generativeai-downloads/data/a11.txt')
pathlib.Path('a11.txt').write_text(response.text)

# Upload file
document = genai.upload_file(path="a11.txt")

# Create cache
apollo_cache = caching.CachedContent.create(
    model="gemini-1.5-flash-001",
    system_instruction="You are an expert at analyzing transcripts.",
    contents=[document],
)

# Generate response
apollo_model = genai.GenerativeModel.from_cached_content(
    cached_content=apollo_cache
)
response = apollo_model.generate_content("Find a lighthearted moment from this transcript")
```

```
import { GoogleAICacheManager, GoogleAIFileManager } from "@google/generative-ai/server";
import { GoogleGenerativeAI } from "@google/generative-ai";

const cacheManager = new GoogleAICacheManager("GOOGLE_API_KEY");
const fileManager = new GoogleAIFileManager("GOOGLE_API_KEY");

const uploadResult = await fileManager.uploadFile("path/to/a11.txt", {
  mimeType: "text/plain",
});

const cacheResult = await cacheManager.create({
  model: "models/gemini-1.5-flash",
  contents: [
    {
      role: "user",
      parts: [
        {
          fileData: {
            fileUri: uploadResult.file.uri,
            mimeType: uploadResult.file.mimeType,
          },
        },
      ],
    },
  ],
});

console.log(cacheResult);

const genAI = new GoogleGenerativeAI("GOOGLE_API_KEY");
const model = genAI.getGenerativeModelFromCachedContent(cacheResult);
const result = await model.generateContent(
  "Please summarize this transcript.",
);
console.log(result.response.text());
```

**之后**

```
import requests
import pathlib
from google import genai
from google.genai import types

client = genai.Client()

# Check which models support caching.
for m in client.models.list():
  for action in m.supported_actions:
    if action == "createCachedContent":
      print(m.name)
      break

# Download file
response = requests.get(
    'https://storage.googleapis.com/generativeai-downloads/data/a11.txt')
pathlib.Path('a11.txt').write_text(response.text)

# Upload file
document = client.files.upload(file='a11.txt')

# Create cache
model='gemini-1.5-flash-001'
apollo_cache = client.caches.create(
      model=model,
      config={
          'contents': [document],
          'system_instruction': 'You are an expert at analyzing transcripts.',
      },
  )

# Generate response
response = client.models.generate_content(
    model=model,
    contents='Find a lighthearted moment from this transcript',
    config=types.GenerateContentConfig(
        cached_content=apollo_cache.name,
    )
)
```

```
import {GoogleGenAI} from '@google/genai';

const ai = new GoogleGenAI({ apiKey: "GOOGLE_API_KEY" });
const filePath = path.join(media, "a11.txt");
const document = await ai.files.upload({
  file: filePath,
  config: { mimeType: "text/plain" },
});
console.log("Uploaded file name:", document.name);
const modelName = "gemini-1.5-flash";

const contents = [
  createUserContent(createPartFromUri(document.uri, document.mimeType)),
];

const cache = await ai.caches.create({
  model: modelName,
  config: {
    contents: contents,
    systemInstruction: "You are an expert analyzing transcripts.",
  },
});
console.log("Cache created:", cache);

const response = await ai.models.generateContent({
  model: modelName,
  contents: "Please summarize this transcript",
  config: { cachedContent: cache.name },
});
console.log("Response text:", response.text);
```

统计 token 数量
-----------

计算请求中的 token 数量。

**之前**

```
import google.generativeai as genai

model = genai.GenerativeModel('gemini-1.5-flash')
response = model.count_tokens(
    'The quick brown fox jumps over the lazy dog.')
```

```
import { GoogleGenerativeAI } from "@google/generative-ai";

 const genAI = new GoogleGenerativeAI("GOOGLE_API_KEY+);
 const model = genAI.getGenerativeModel({
   model: "gemini-1.5-flash",
 });

 // Count tokens in a prompt without calling text generation.
 const countResult = await model.countTokens(
   "The quick brown fox jumps over the lazy dog.",
 );

 console.log(countResult.totalTokens); // 11

 const generateResult = await model.generateContent(
   "The quick brown fox jumps over the lazy dog.",
 );

 // On the response for `generateContent`, use `usageMetadata`
 // to get separate input and output token counts
 // (`promptTokenCount` and `candidatesTokenCount`, respectively),
 // as well as the combined token count (`totalTokenCount`).
 console.log(generateResult.response.usageMetadata);
 // candidatesTokenCount and totalTokenCount depend on response, may vary
 // { promptTokenCount: 11, candidatesTokenCount: 124, totalTokenCount: 135 }
```

**之后**

```
from google import genai

client = genai.Client()

response = client.models.count_tokens(
    model='gemini-2.0-flash',
    contents='The quick brown fox jumps over the lazy dog.',
)
```

```
import {GoogleGenAI} from '@google/genai';

const ai = new GoogleGenAI({ apiKey: "GOOGLE_API_KEY" });
const prompt = "The quick brown fox jumps over the lazy dog.";
const countTokensResponse = await ai.models.countTokens({
  model: "gemini-2.0-flash",
  contents: prompt,
});
console.log(countTokensResponse.totalTokens);

const generateResponse = await ai.models.generateContent({
  model: "gemini-2.0-flash",
  contents: prompt,
});
console.log(generateResponse.usageMetadata);
```

生成图片
----

生成图片：

**之前**

```
#pip install https://github.com/google-gemini/generative-ai-python@imagen
import google.generativeai as genai

imagen = genai.ImageGenerationModel(
    "imagen-3.0-generate-001")
gen_images = imagen.generate_images(
    prompt="Robot holding a red skateboard",
    number_of_images=1,
    safety_filter_level="block_low_and_above",
    person_generation="allow_adult",
    aspect_ratio="3:4",
)
```

**之后**

```
from google import genai

client = genai.Client()

gen_images = client.models.generate_images(
    model='imagen-3.0-generate-001',
    prompt='Robot holding a red skateboard',
    config=types.GenerateImagesConfig(
        number_of_images= 1,
        safety_filter_level= "BLOCK_LOW_AND_ABOVE",
        person_generation= "ALLOW_ADULT",
        aspect_ratio= "3:4",
    )
)

for n, image in enumerate(gen_images.generated_images):
    pathlib.Path(f'{n}.png').write_bytes(
        image.image.image_bytes)
```

嵌入内容
----

生成内容嵌入。

**之前**

```
import google.generativeai as genai

response = genai.embed_content(
  model='models/gemini-embedding-001',
  content='Hello world'
)
```

```
import { GoogleGenerativeAI } from "@google/generative-ai";

const genAI = new GoogleGenerativeAI("GOOGLE_API_KEY");
const model = genAI.getGenerativeModel({
  model: "gemini-embedding-001",
});

const result = await model.embedContent("Hello world!");

console.log(result.embedding);
```

**之后**

```
from google import genai

client = genai.Client()

response = client.models.embed_content(
  model='gemini-embedding-001',
  contents='Hello world',
)
```

```
import {GoogleGenAI} from '@google/genai';

const ai = new GoogleGenAI({ apiKey: "GOOGLE_API_KEY" });
const text = "Hello World!";
const result = await ai.models.embedContent({
  model: "gemini-embedding-001",
  contents: text,
  config: { outputDimensionality: 10 },
});
console.log(result.embeddings);
```

调整模型
----

创建和使用已调参模型。

新版 SDK 通过 `client.tunings.tune` 简化了调优流程，该方法会启动调优作业并轮询，直到作业完成。

**之前**

```
import google.generativeai as genai
import random

# create tuning model
train_data = {}
for i in range(1, 6):
  key = f'input {i}'
  value = f'output {i}'
  train_data[key] = value

name = f'generate-num-{random.randint(0,10000)}'
operation = genai.create_tuned_model(
    source_model='models/gemini-1.5-flash-001-tuning',
    training_data=train_data,
    id = name,
    epoch_count = 5,
    batch_size=4,
    learning_rate=0.001,
)
# wait for tuning complete
tuningProgress = operation.result()

# generate content with the tuned model
model = genai.GenerativeModel(model_name=f'tunedModels/{name}')
response = model.generate_content('55')
```

**之后**

```
from google import genai
from google.genai import types

client = genai.Client()

# Check which models are available for tuning.
for m in client.models.list():
  for action in m.supported_actions:
    if action == "createTunedModel":
      print(m.name)
      break

# create tuning model
training_dataset=types.TuningDataset(
        examples=[
            types.TuningExample(
                text_input=f'input {i}',
                output=f'output {i}',
            )
            for i in range(5)
        ],
    )
tuning_job = client.tunings.tune(
    base_model='models/gemini-1.5-flash-001-tuning',
    training_dataset=training_dataset,
    config=types.CreateTuningJobConfig(
        epoch_count= 5,
        batch_size=4,
        learning_rate=0.001,
        tuned_model_display_name="test tuned model"
    )
)

# generate content with the tuned model
response = client.models.generate_content(
    model=tuning_job.tuned_model.model,
    contents='55',
)
```

如未另行说明，那么本页面中的内容已根据[知识共享署名 4.0 许可](https://creativecommons.org/licenses/by/4.0/)获得了许可，并且代码示例已根据 [Apache 2.0 许可](https://www.apache.org/licenses/LICENSE-2.0)获得了许可。有关详情，请参阅 [Google 开发者网站政策](https://developers.google.com/site-policies?hl=zh-cn)。Java 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2025-08-01。
a