#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from podcast_parser import extract_dialogues


def main():
    # 测试文件路径
    test_file = 'example_podcast.txt'
    
    # 读取测试文件
    with open(test_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取对话
    dialogues = extract_dialogues(content)
    
    # 打印结果
    print(f"共提取到 {len(dialogues)} 条对话")
    print("\n对话内容预览:")
    for i, dialogue in enumerate(dialogues[:5]):
        print(f"\n[{i+1}] {dialogue['speaker']}: {dialogue['text'][:50]}...")
    
    # 保存提取结果到JSON文件
    with open('extracted_dialogues.json', 'w', encoding='utf-8') as f:
        json.dump(dialogues, f, ensure_ascii=False, indent=4)
    
    print("\n完整对话已保存到 extracted_dialogues.json")


if __name__ == '__main__':
    main()