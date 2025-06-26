# MiniMax Flow - 播客文章转音频工具

这是一个Python脚本项目，用于将包含对话的播客文章转换为音频。该工具会自动提取文章中的对话，调用MiniMax的T2A V2接口生成每句对话的音频，然后将所有音频合并成一个完整的音频文件。

代码由Cursor生成，感谢AI提高效率

## 功能特点

- 自动提取播客文章中的对话内容
- 支持为不同说话人配置不同的声音
- 调用MiniMax的T2A V2接口生成高质量音频
- 自动合并所有对话音频为一个完整的音频文件

## 安装依赖

```bash
pip install requests pydub
```

## 配置

在使用前，请编辑`config.json`文件，填入您的MiniMax API密钥和其他必要信息：

```json
{
    "api_key": "your_api_key_here",
    "group_id": "your_group_id_here",
    "base_url": "https://api.minimaxi.com/v1/t2a_v2",
    "temp_dir": "temp_audio",
    "model": "speech-02-hd",
    "default_voice": "male-qn-qingse",
    "speed": 1,
    "vol": 1,
    "pitch": 0,
    "sample_rate": 32000,
    "bitrate": 128000,
    "voice_map": {
        "主持人": "female-shaonv",
        "嘉宾A": "male-qn-qingse",
        "嘉宾B": "male-zh-yinse"
    }
}
```

### 配置说明

- `api_key`: MiniMax API密钥
- `group_id`: MiniMax组ID
- `base_url`: MiniMax T2A V2 API的基础URL
- `temp_dir`: 临时音频文件存储目录
- `model`: 使用的模型，推荐使用最新的`speech-02-hd`或`speech-02-turbo`
- `default_voice`: 默认声音ID
- `speed`: 语速，默认为1.0
- `vol`: 音量，默认为1.0
- `pitch`: 音调，默认为0.0
- `sample_rate`: 采样率，默认为32000
- `bitrate`: 比特率，默认为128000
- `voice_map`: 说话人到声音ID的映射

## 使用方法

```bash
python main.py --input 示例.txt --output 输出音频.mp3 --config config.json
```

### 参数说明

- `--input`, `-i`: 输入的播客文章文件路径（必需）
- `--output`, `-o`: 输出的音频文件路径（必需）
- `--config`, `-c`: 配置文件路径（可选，默认为`config.json`）

## 播客文章格式要求

播客文章中的对话应该遵循以下格式：

```
说话人A：这是说话人A的对话内容。
说话人B：这是说话人B的对话内容。
说话人A：这是说话人A的另一段对话。
```

工具会自动提取格式为"说话人：对话内容"的内容。

## 声音ID参考

MiniMax T2A V2接口支持多种声音，以下是一些常用的声音ID：

- `female-shaonv`: 少女音色
- `male-qn-qingse`: 男声-青涩
- `male-zh-yinse`: 男声-阴色
- `female-zh-wenzhong`: 女声-温中

最新的speech-02-hd和speech-02-turbo模型支持更多的声音选项和更高质量的音频输出。更多声音ID请参考MiniMax官方文档：https://platform.minimaxi.com/document/

## 注意事项

- 请确保您有足够的MiniMax API调用额度
- 生成的临时音频文件会在处理完成后自动删除
- 对于较长的播客文章，处理时间可能较长