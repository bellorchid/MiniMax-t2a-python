import re
from typing import List, Dict, Tuple


def extract_dialogues(content: str) -> List[Dict]:
    """
    从播客文章中提取对话
    
    Args:
        content: 播客文章内容
        
    Returns:
        对话列表，每个对话包含说话人和内容
    """
    # 正则表达式匹配对话模式
    # 假设对话格式为："人名：对话内容"
    dialogue_pattern = re.compile(r'([^：:]+)[：:]([^\n]+)')
    
    # 查找所有匹配项
    matches = dialogue_pattern.findall(content)
    
    # 转换为所需格式
    dialogues = []
    for speaker, text in matches:
        # 清理说话人和文本
        speaker = speaker.strip()
        text = text.strip()
        
        # 跳过空文本
        if not text:
            continue
            
        dialogues.append({
            'speaker': speaker,
            'text': text
        })
    
    return dialogues


def identify_speakers(dialogues: List[Dict]) -> Dict[str, str]:
    """
    识别对话中的说话人，并为每个说话人分配一个角色ID
    
    Args:
        dialogues: 对话列表
        
    Returns:
        说话人到角色ID的映射
    """
    speakers = set(dialogue['speaker'] for dialogue in dialogues)
    speaker_roles = {}
    
    # 为每个说话人分配一个角色ID
    for i, speaker in enumerate(speakers):
        speaker_roles[speaker] = f"role_{i+1}"
    
    return speaker_roles