from flask import render_template, jsonify, current_app
from app.blueprints.mqtt import bp
import paho.mqtt.client as mqtt
import threading
import time
import binascii
import logging

# 设置日志记录器
logger = logging.getLogger('mqtt_client')
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# MQTT配置
MQTT_BROKER = "192.168.1.59"
MQTT_PORT = 1883
MQTT_TOPIC = "voltage"

# 存储最新的电压数据
voltage_data = {
    'timestamp': 0,
    'values': [0] * 12  # 12个字节的数据
}

# MQTT客户端回调函数
def on_connect(client, userdata, flags, rc):
    logger.info(f"MQTT已连接，返回码: {rc}")
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    try:
        # 解析接收到的16进制数据
        payload = msg.payload
        
        # 将字节数据转换为字符串，并去掉前缀"b'"
        r_json = str(payload)[2:-1]
        
        # 确保字符串长度足够
        if len(r_json) >= 24:
            # 每2个字符提取一个值
            voltage_str = [r_json[i:i+2] for i in range(0, 24, 2)]
            values = []
            
            # 将十六进制字符串转换为整数
            for i in range(min(12, len(voltage_str))):
                try:
                    values.append(int(voltage_str[i], 16))
                except ValueError:
                    # 如果转换失败，添加0
                    values.append(0)
            
            # 确保有12个值
            while len(values) < 12:
                values.append(0)
            
            # 更新全局数据
            voltage_data['timestamp'] = time.time()
            voltage_data['values'] = values
        else:
            logger.warning(f"数据长度不足: {len(r_json)}字符，需要至少24字符")
            
    except Exception as e:
        logger.error(f"处理MQTT消息时出错: {str(e)}")
        logger.exception(e)  # 记录完整的异常堆栈

# 初始化MQTT客户端
mqtt_client = None

def start_mqtt_client(app):
    global mqtt_client
    
    try:
        # 创建MQTT客户端
        mqtt_client = mqtt.Client()
        mqtt_client.on_connect = on_connect
        mqtt_client.on_message = on_message
        
        # 连接到MQTT代理
        mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
        
        # 在后台线程中启动MQTT循环
        mqtt_client.loop_start()
        
        # 记录日志（使用应用上下文）
        with app.app_context():
            current_app.logger.info(f"MQTT客户端已启动，连接到 {MQTT_BROKER}:{MQTT_PORT}")
    except Exception as e:
        # 记录日志（使用应用上下文）
        with app.app_context():
            current_app.logger.error(f"启动MQTT客户端时出错: {str(e)}")

@bp.route('/voltage')
def voltage():
    """显示电压数据页面"""
    return render_template('mqtt/voltage.html', title='电压监控')

@bp.route('/voltage/data')
def voltage_data_api():
    """返回最新的电压数据"""
    global voltage_data
    
    # 检查数据是否过期（超过5秒）
    current_time = time.time()
    if current_time - voltage_data['timestamp'] > 5:
        # 数据过期，返回全零数据
        return jsonify({
            'timestamp': current_time,
            'values': [0] * 12,
            'status': 'stale'
        })
    
    # 返回最新数据
    return jsonify({
        'timestamp': voltage_data['timestamp'],
        'values': voltage_data['values'],
        'status': 'ok'
    }) 