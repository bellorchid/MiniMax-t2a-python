import os
import json
from typing import Dict


def load_config(config_path: str) -> Dict:
    """
    加载配置文件
    
    Args:
        config_path: 配置文件路径
        
    Returns:
        配置信息字典
    """
    # 检查配置文件是否存在
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"配置文件不存在: {config_path}")
    
    # 读取配置文件
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # 验证必要的配置项
    required_fields = ['api_key', 'group_id']
    for field in required_fields:
        if field not in config:
            raise ValueError(f"配置文件缺少必要的字段: {field}")
    
    # 设置默认值
    if 'temp_dir' not in config:
        config['temp_dir'] = 'temp_audio'
    
    if 'model' not in config:
        config['model'] = 'speech-02-hd'
        
    if 'default_voice' not in config:
        config['default_voice'] = 'male-qn-qingse'
    
    if 'speed' not in config:
        config['speed'] = 1.0
        
    if 'vol' not in config:
        config['vol'] = 1.0
        
    if 'pitch' not in config:
        config['pitch'] = 0.0
        
    if 'sample_rate' not in config:
        config['sample_rate'] = 32000
        
    if 'bitrate' not in config:
        config['bitrate'] = 128000
    
    # 如果没有配置voice_map，创建一个空字典
    if 'voice_map' not in config:
        config['voice_map'] = {}
    
    return config


def create_default_config(config_path: str) -> None:
    """
    创建默认配置文件
    
    Args:
        config_path: 配置文件路径
    """
    default_config = {
        "api_key": "your_api_key_here",
        "group_id": "your_group_id_here",
        "base_url": "https://api.minimaxi.com/v1/t2a_v2",
        "temp_dir": "temp_audio",
        "model": "speech-02-hd",
        "default_voice": "male-qn-qingse",
        "speed": 1.0,
        "vol": 1.0,
        "pitch": 0.0,
        "sample_rate": 32000,
        "bitrate": 128000,
        "voice_map": {
            "主持人": "female-shaonv",
            "嘉宾A": "male-qn-qingse",
            "嘉宾B": "male-zh-yinse"
        }
    }
    
    # 确保目录存在
    os.makedirs(os.path.dirname(os.path.abspath(config_path)), exist_ok=True)
    
    # 写入配置文件
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(default_config, f, ensure_ascii=False, indent=4)
    
    print(f"已创建默认配置文件: {config_path}")
    print("请编辑配置文件，填入您的API密钥和其他必要信息。")