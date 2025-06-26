import os
import requests
import json
import sys

def load_config():
    """
    从config.json加载配置
    """
    config_path = 'config.json'
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            
        # 检查必要的配置项
        if not config.get('api_key'):
            print("错误: 配置文件中缺少API密钥")
            sys.exit(1)
            
        if not config.get('group_id'):
            print("错误: 配置文件中缺少群组ID")
            sys.exit(1)
            
        return config
    except FileNotFoundError:
        print(f"错误: 配置文件 {config_path} 不存在")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"错误: 配置文件 {config_path} 格式不正确")
        sys.exit(1)

def get_all_voices(config):
    """
    获取所有可用的音色
    
    Args:
        config: 配置信息，包含API密钥等
        
    Returns:
        所有可用的音色信息
    """
    api_key = config.get('api_key')
    group_id = config.get('group_id')
    base_url = f"https://api.minimaxi.com/v1/get_voice"
    
    headers = {
        'authority': 'api.minimaxi.com',
        "Authorization": f"Bearer {api_key}",
    }
    
    # 构建请求数据
    data = {
        'voice_type': 'all'
    }
    
    # 发送请求
    try:
        response = requests.post(base_url, headers=headers, data=data)
        response.raise_for_status()
        
        # 解析响应
        result = response.json()
        
        # 检查是否有错误
        if 'base_resp' in result and result['base_resp'].get('status_code', 0) != 0:
            print(f"错误: 获取音色失败: {result['base_resp'].get('status_msg')}")
            return None
            
        return result
    except requests.exceptions.RequestException as e:
        print(f"错误: 请求失败: {e}")
        return None

def print_voices(voices_data):
    """
    打印所有可用的音色信息
    
    Args:
        voices_data: 音色数据
    """
    if not voices_data:
        print("没有获取到音色数据")
        return
    
    # 打印系统音色
    if 'system_voice' in voices_data and voices_data['system_voice']:
        print("\n=== 系统音色 ===")
        for voice in voices_data['system_voice']:
            print(f"音色ID: {voice.get('voice_id', 'N/A')}")
            print(f"音色名称: {voice.get('voice_name', 'N/A')}")
            if 'description' in voice and voice['description']:
                print(f"描述: {', '.join(voice['description'])}")
            print("---")
    
    # 打印克隆音色
    if 'voice_cloning' in voices_data and voices_data['voice_cloning']:
        print("\n=== 克隆音色 ===")
        for voice in voices_data['voice_cloning']:
            print(f"音色ID: {voice.get('voice_id', 'N/A')}")
            if 'description' in voice and voice['description']:
                print(f"描述: {', '.join(voice['description'])}")
            print(f"创建时间: {voice.get('created_time', 'N/A')}")
            print("---")
    
    # 打印生成音色
    if 'voice_generation' in voices_data and voices_data['voice_generation']:
        print("\n=== 生成音色 ===")
        for voice in voices_data['voice_generation']:
            print(f"音色ID: {voice.get('voice_id', 'N/A')}")
            if 'description' in voice and voice['description']:
                print(f"描述: {', '.join(voice['description'])}")
            print(f"创建时间: {voice.get('created_time', 'N/A')}")
            print("---")
    
    # 打印音乐生成
    if 'music_generation' in voices_data and voices_data['music_generation']:
        print("\n=== 音乐生成 ===")
        for voice in voices_data['music_generation']:
            print(f"音色ID: {voice.get('voice_id', 'N/A')}")
            print(f"乐器ID: {voice.get('instrumental_id', 'N/A')}")
            print(f"创建时间: {voice.get('created_time', 'N/A')}")
            print("---")

def main():
    # 加载配置
    config = load_config()
    
    # 获取所有音色
    print("正在获取所有可用音色...")
    voices_data = get_all_voices(config)
    
    # 打印音色信息
    print_voices(voices_data)
    
    # 保存音色数据到文件
    if voices_data:
        with open('voices_data.json', 'w', encoding='utf-8') as f:
            json.dump(voices_data, f, ensure_ascii=False, indent=2)
        print(f"\n音色数据已保存到 voices_data.json")

if __name__ == "__main__":
    main()