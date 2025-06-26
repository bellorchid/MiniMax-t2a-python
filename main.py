import argparse
import json
import os
from typing import List, Dict

from podcast_parser import extract_dialogues
from audio_generator import generate_audio, merge_audios
from config import load_config


def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='将播客文章转换为音频')
    parser.add_argument('--input', '-i', type=str, required=True, help='输入的播客文章文件路径')
    parser.add_argument('--output', '-o', type=str, required=True, help='输出的音频文件路径')
    parser.add_argument('--config', '-c', type=str, default='config.json', help='配置文件路径')
    args = parser.parse_args()
    
    # 加载配置
    config = load_config(args.config)
    
    # 读取输入文件
    with open(args.input, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取对话
    dialogues = extract_dialogues(content)
    print(f"提取到 {len(dialogues)} 条对话")
    
    # 生成音频
    audio_files = generate_audio(dialogues, config)
    print(f"生成了 {len(audio_files)} 个音频文件")
    
    # 合并音频
    output_path = merge_audios(audio_files, args.output)
    print(f"已将音频合并到: {output_path}")
    
    # 清理临时文件
    for file in audio_files:
        if os.path.exists(file):
            os.remove(file)
    

if __name__ == '__main__':
    main()