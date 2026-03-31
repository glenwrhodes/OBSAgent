"""
OBSAgent - AI agent backend server
Serves the chat UI and handles agent requests
"""

import json
import os
import sys
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from agent import OBSAgent

app = Flask(__name__, template_folder='../ui/templates', static_folder='../ui/static')
CORS(app)

# Load config
CONFIG_PATH = os.path.join(os.path.dirname(__file__), '..', 'config.json')
with open(CONFIG_PATH) as f:
    config = json.load(f)

agent = OBSAgent(config)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get('message', '').strip()
    history = data.get('history', [])

    if not message:
        return jsonify({'error': 'No message provided'}), 400

    try:
        response = agent.run(message, history)
        return jsonify({
            'response': response['text'],
            'tool_calls': response.get('tool_calls', []),
            'success': True
        })
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500


@app.route('/api/status')
def status():
    """Check OBS connection status"""
    connected = agent.obs_client.is_connected()
    obs_version = None
    if connected:
        try:
            info = agent.obs_client.get_version()
            obs_version = info.get('obsVersion')
        except Exception:
            pass
    return jsonify({
        'connected': connected,
        'obs_version': obs_version
    })


@app.route('/api/scenes')
def get_scenes():
    """Get current scene list for UI display"""
    try:
        scenes = agent.obs_client.get_scene_list()
        return jsonify(scenes)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    host = config.get('server', {}).get('host', '127.0.0.1')
    port = config.get('server', {}).get('port', 5050)
    print(f"OBSAgent server starting on http://{host}:{port}")
    print("Dock this URL in OBS: Docks → Custom Browser Docks → Add")
    app.run(host=host, port=port, debug=False)
