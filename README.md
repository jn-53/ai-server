# Ollama API 服务

这是一个简单的Flask应用，用于与本地运行的Ollama模型进行交互。它提供了一个Web界面和API端点，使您可以轻松地使用Ollama模型进行文本生成和对话。

## 前提条件

1. 已安装Python 3.7+
2. 已安装并运行Ollama（默认在http://localhost:11434）
3. 已在Ollama中下载至少一个模型（例如：`ollama pull llama2`）

## 安装

1. 克隆或下载此仓库
2. 安装依赖：

```bash
pip install -r requirements.txt
```

## 运行服务

```bash
python app.py
```

服务将在 http://localhost:5311 上启动。

## 使用方法

### Web界面

访问 http://localhost:5311 在浏览器中使用Web界面：

1. 页面加载时会自动获取可用的Ollama模型列表
2. 从下拉菜单中选择一个模型
3. 在文本框中输入您的消息
4. 点击"发送"按钮
5. 您的消息将显示在对话区域中，模型的回复会以流式方式实时显示
6. 您可以继续发送消息，进行连续对话
7. 点击"清除对话"按钮可以重新开始新的对话

### API端点

#### 获取模型列表

```
GET /api/models
```

响应示例：

```json
{
  "models": [
    {
      "name": "llama2",
      "size": 3791730298
    },
    {
      "name": "mistral",
      "size": 4126541330
    }
  ]
}
```

#### 流式对话

```
GET /api/chat/stream
POST /api/chat/stream
```

这是一个使用Server-Sent Events (SSE)实现的流式对话API。

请求体：

```json
{
  "model": "llama2",
  "messages": [
    {"role": "user", "content": "你好，请介绍一下自己"},
    {"role": "assistant", "content": "你好！我是一个AI助手，由Ollama提供支持。"},
    {"role": "user", "content": "你能做什么？"}
  ]
}
```

响应是一个SSE流，每个事件包含模型生成的部分内容：

```
data: {"content":"我"}
data: {"content":"可以"}
data: {"content":"帮助"}
...
data: [DONE]
```

客户端可以实时接收和显示这些内容，实现打字机效果的流式输出。

#### 对话模式

```
POST /api/chat
```

请求体：

```json
{
  "model": "llama2",
  "messages": [
    {"role": "user", "content": "你好，请介绍一下自己"},
    {"role": "assistant", "content": "你好！我是一个AI助手，由Ollama提供支持。"},
    {"role": "user", "content": "你能做什么？"}
  ]
}
```

响应示例：

```json
{
  "message": {
    "role": "assistant",
    "content": "我可以帮助你回答问题、提供信息、进行对话、创作内容等。我的能力取决于我的训练数据和你使用的具体模型。有什么我可以帮助你的吗？"
  }
}
```

## 环境变量

- `OLLAMA_API_URL`: Ollama API的URL（默认为 http://localhost:11434）

例如，如果Ollama运行在不同的主机或端口上：

```bash
export OLLAMA_API_URL="http://192.168.1.100:11434"
python app.py
```

## 注意事项

- 确保Ollama服务正在运行，否则API请求将失败
- 响应时间取决于所选模型的大小和复杂性
- 对于大型模型，生成响应可能需要一些时间
