#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from config import load_config, create_default_config


def main():
    config_path = 'test_config.json'
    
    # 如果测试配置文件不存在，创建一个
    if not os.path.exists(config_path):
        print(f"创建测试配置文件: {config_path}")
        create_default_config(config_path)
    
    # 加载配置
    try:
        config = load_config(config_path)
        print("成功加载配置:")
        print(json.dumps(config, ensure_ascii=False, indent=4))
        
        # 检查必要字段
        print("\n检查配置字段:")
        print(f"API密钥: {'已设置' if config['api_key'] != 'your_api_key_here' else '未设置 - 请更新配置'}")
        print(f"组ID: {'已设置' if config['group_id'] != 'your_group_id_here' else '未设置 - 请更新配置'}")
        print(f"API基础URL: {config['base_url']}")
        print(f"模型: {config['model']}")
        print(f"临时目录: {config['temp_dir']}")
        print(f"默认声音: {config['default_voice']}")
        print(f"语速: {config['speed']}")
        print(f"音量: {config['vol']}")
        print(f"音调: {config['pitch']}")
        print(f"采样率: {config['sample_rate']}")
        print(f"比特率: {config['bitrate']}")
        print(f"声音映射: {len(config['voice_map'])} 个说话人已配置")
        
    except Exception as e:
        print(f"加载配置时出错: {str(e)}")


if __name__ == '__main__':
    main()