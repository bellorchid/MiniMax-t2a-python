import os
import time
import requests
import json
from typing import List, Dict
import subprocess
from pydub import AudioSegment


def generate_audio(dialogues: List[Dict], config: Dict) -> List[str]:
    """
    为每条对话生成音频
    
    Args:
        dialogues: 对话列表
        config: 配置信息，包含API密钥等
        
    Returns:
        生成的音频文件路径列表
    """
    api_key = config.get('api_key')
    group_id = config.get('group_id')
    base_url = config.get('base_url', 'https://api.minimaxi.com/v1/t2a_v2')
    voice_map = config.get('voice_map', {})
    output_dir = config.get('temp_dir', 'temp_audio')
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    audio_files = []
    
    for i, dialogue in enumerate(dialogues):
        speaker = dialogue['speaker']
        text = dialogue['text']
        
        # 获取说话人对应的声音ID，如果没有配置则使用默认声音
        voice_id = voice_map.get(speaker, config.get('default_voice', 'male-qn-qingse'))
        
        # 构建请求参数
        payload = {
            "text": text,
            "model": config.get('model', 'speech-02-hd'),  # 使用最新的模型
            "stream": False,
            "output_format": "hex",
            "language_boost": "auto",
            "voice_setting": {
                "voice_id": voice_id,
                "speed": config.get('speed', 1),
                "vol": config.get('vol', 1),
                "pitch": config.get('pitch', 0)
            },
            "audio_setting": {
                "sample_rate": config.get('sample_rate', 32000),
                "bitrate": config.get('bitrate', 128000),
                "format": "mp3"
            }
        }
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
            "Groupid": group_id
        }
        
        # 发送请求
        try:
            response = requests.post(base_url, json=payload, headers=headers)
            response.raise_for_status()
            
            # 解析响应
            result = response.json()
            
            # 检查是否有错误
            if 'base_resp' in result and result['base_resp'].get('status_code', 0) != 0:
                print(f"警告: 对话 {i+1} 生成失败: {result['base_resp'].get('status_msg')}")
                continue
                
            # 获取音频数据
            audio_data = result.get('data', {}).get('audio')
            
            if not audio_data:
                print(f"警告: 对话 {i+1} 未能获取音频数据")
                continue
                
            # 保存音频
            file_path = os.path.join(output_dir, f"dialogue_{i:04d}.mp3")
            with open(file_path, 'wb') as f:
                # 如果是hex格式，需要转换为二进制
                if payload['output_format'] == 'hex':
                    import binascii
                    audio_binary = binascii.unhexlify(audio_data)
                    f.write(audio_binary)
                # 如果是url格式，需要下载
                elif payload['output_format'] == 'url':
                    audio_response = requests.get(audio_data)
                    audio_response.raise_for_status()
                    f.write(audio_response.content)
                
            audio_files.append(file_path)
            print(f"已生成音频 {i+1}/{len(dialogues)}: {speaker} - {text[:30]}...")
            
            # 避免API限流
            time.sleep(0.5)
            
        except Exception as e:
            print(f"生成音频时出错 (对话 {i+1}): {str(e)}")
    
    return audio_files


def merge_audios(audio_files: List[str], output_path: str) -> str:
    """
    合并多个音频文件
    
    Args:
        audio_files: 音频文件路径列表
        output_path: 输出文件路径
        
    Returns:
        合并后的音频文件路径
    """
    if not audio_files:
        raise ValueError("没有音频文件可合并")
    
    # 确保输出目录存在
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    
    # 使用pydub合并音频
    combined = AudioSegment.empty()
    
    for file_path in audio_files:
        audio = AudioSegment.from_file(file_path)
        combined += audio
        # 在每个音频之间添加短暂的停顿
        combined += AudioSegment.silent(duration=300)  # 300毫秒的停顿
    
    # 导出合并后的音频
    combined.export(output_path, format="mp3")
    
    return output_path