import os
import json
import binascii
import requests
import time
import uuid
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import tempfile
from pydub import AudioSegment

app = Flask(__name__)

# 加载音色数据
def load_voices():
    try:
        with open('voices_data.json', 'r', encoding='utf-8') as f:
            voices_data = json.load(f)
        return voices_data
    except Exception as e:
        print(f"加载音色数据失败: {e}")
        return {"system_voice": []}

# 加载配置
def load_config():
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        # 尝试加载示例配置
        try:
            with open('config.json.example', 'r', encoding='utf-8') as f:
                config = json.load(f)
            print("警告: 使用示例配置文件，请确保填写了正确的API密钥和群组ID")
            return config
        except Exception as e:
            print(f"加载配置失败: {e}")
            return {}

# 生成语音
def generate_audio(text, voice_id, config):
    api_key = config.get('api_key')
    group_id = config.get('group_id')
    base_url = config.get('base_url', 'https://api.minimaxi.com/v1/t2a_v2')
    
    # 构建请求参数
    payload = {
        "text": text,
        "model": config.get('model', 'speech-02-hd'),
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
    
    try:
        response = requests.post(base_url, json=payload, headers=headers)
        response.raise_for_status()
        
        # 解析响应
        result = response.json()
        
        # 检查是否有错误
        if 'base_resp' in result and result['base_resp'].get('status_code', 0) != 0:
            return None, f"生成失败: {result['base_resp'].get('status_msg')}"
            
        # 获取音频数据
        audio_data = result.get('data', {}).get('audio')
        
        if not audio_data:
            return None, "未能获取音频数据"
            
        # 如果是hex格式，需要转换为二进制
        if payload['output_format'] == 'hex':
            audio_binary = binascii.unhexlify(audio_data)
            return audio_binary, None
        # 如果是url格式，需要下载
        elif payload['output_format'] == 'url':
            audio_response = requests.get(audio_data)
            audio_response.raise_for_status()
            return audio_response.content, None
            
    except Exception as e:
        return None, f"请求失败: {str(e)}"

@app.route('/')
def index():
    voices_data = load_voices()
    system_voices = voices_data.get('system_voice', [])
    voice_cloning = voices_data.get('voice_cloning', [])
    
    # 合并系统音色和克隆音色
    all_voices = system_voices + voice_cloning
    
    # 按音色名称排序
    all_voices.sort(key=lambda x: x.get('voice_name', ''))
    
    return render_template('voice_preview.html', voices=all_voices)

@app.route('/speech_editor')
def speech_editor():
    voices_data = load_voices()
    system_voices = voices_data.get('system_voice', [])
    voice_cloning = voices_data.get('voice_cloning', [])
    
    # 合并系统音色和克隆音色
    all_voices = system_voices + voice_cloning
    
    # 按音色名称排序
    all_voices.sort(key=lambda x: x.get('voice_name', ''))
    
    return render_template('speech_editor.html', voices=all_voices)

@app.route('/preview', methods=['POST'])
def preview():
    text = request.form.get('text', '')
    voice_id = request.form.get('voice_id', '')
    
    if not text:
        return jsonify({"error": "请输入文本"}), 400
        
    if not voice_id:
        return jsonify({"error": "请选择音色"}), 400
    
    config = load_config()
    if not config.get('api_key') or not config.get('group_id'):
        return jsonify({"error": "配置文件中缺少API密钥或群组ID"}), 500
    
    audio_data, error = generate_audio(text, voice_id, config)
    
    if error:
        return jsonify({"error": error}), 500
    
    # 创建临时文件保存音频
    temp_dir = os.path.join(tempfile.gettempdir(), 'minimax_preview')
    os.makedirs(temp_dir, exist_ok=True)
    
    # 生成随机文件名，添加前缀以便路由识别
    filename = f"preview_{int(time.time())}_{binascii.hexlify(os.urandom(4)).decode()}.mp3"
    file_path = os.path.join(temp_dir, filename)
    
    with open(file_path, 'wb') as f:
        f.write(audio_data)
    
    return jsonify({"success": True, "audio_url": f"/audio/{filename}"})

@app.route('/generate_segment', methods=['POST'])
def generate_segment():
    text = request.form.get('text', '')
    voice_id = request.form.get('voice_id', '')
    segment_id = request.form.get('segment_id', '')
    
    if not text:
        return jsonify({"error": "请输入文本"}), 400
        
    if not voice_id:
        return jsonify({"error": "请选择音色"}), 400
    
    config = load_config()
    if not config.get('api_key') or not config.get('group_id'):
        return jsonify({"error": "配置文件中缺少API密钥或群组ID"}), 500
    
    audio_data, error = generate_audio(text, voice_id, config)
    
    if error:
        return jsonify({"error": error}), 500
    
    # 创建临时文件保存音频
    temp_dir = os.path.join(tempfile.gettempdir(), 'minimax_speech')
    os.makedirs(temp_dir, exist_ok=True)
    
    # 使用分段ID作为文件名的一部分，确保唯一性
    filename = f"segment_{segment_id}_{int(time.time())}.mp3"
    file_path = os.path.join(temp_dir, filename)
    
    with open(file_path, 'wb') as f:
        f.write(audio_data)
    
    return jsonify({
        "success": True, 
        "audio_url": f"/audio/{filename}",
        "filename": filename
    })

@app.route('/merge_segments', methods=['POST'])
def merge_segments():
    data = request.json
    segments = data.get('segments', [])
    
    if not segments:
        return jsonify({"error": "没有可合并的分段"}), 400
    
    try:
        # 创建临时目录
        temp_dir = os.path.join(tempfile.gettempdir(), 'minimax_speech')
        os.makedirs(temp_dir, exist_ok=True)
        
        # 合并音频
        combined = AudioSegment.empty()
        
        for segment in segments:
            filename = segment.get('filename')
            if not filename:
                continue
                
            file_path = os.path.join(temp_dir, filename)
            if not os.path.exists(file_path):
                return jsonify({"error": f"找不到音频文件: {filename}"}), 404
                
            audio = AudioSegment.from_file(file_path)
            combined += audio
            # 在每个音频之间添加短暂的停顿
            combined += AudioSegment.silent(duration=300)  # 300毫秒的停顿
        
        # 生成合并后的文件名
        merged_filename = f"merged_{uuid.uuid4().hex[:8]}_{int(time.time())}.mp3"
        merged_path = os.path.join(temp_dir, merged_filename)
        
        # 导出合并后的音频
        combined.export(merged_path, format="mp3")
        
        return jsonify({
            "success": True,
            "audio_url": f"/audio/{merged_filename}",
            "filename": merged_filename
        })
    except Exception as e:
        return jsonify({"error": f"合并音频失败: {str(e)}"}), 500

@app.route('/audio/<filename>')
def get_audio(filename):
    # 支持两个临时目录
    if filename.startswith('preview_'):
        temp_dir = os.path.join(tempfile.gettempdir(), 'minimax_preview')
    else:
        temp_dir = os.path.join(tempfile.gettempdir(), 'minimax_speech')
        
    return send_file(os.path.join(temp_dir, filename), mimetype='audio/mpeg')

if __name__ == '__main__':
    # 确保templates目录存在
    os.makedirs('templates', exist_ok=True)
    
    # 如果配置文件不存在，提示用户
    if not os.path.exists('config.json') and not os.path.exists('config.json.example'):
        print("警告: 未找到配置文件，请确保config.json或config.json.example文件存在")
    
    # 使用host='0.0.0.0'允许局域网访问
    app.run(debug=True, host='0.0.0.0', port=5000)