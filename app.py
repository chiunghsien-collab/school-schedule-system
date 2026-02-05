from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)
DATA_FILE = 'data.json'

# --- 核心設定：禁用瀏覽器快取 ---
# 這樣你修改 index.html 後，重新整理網頁才會立刻看到 v6.8
@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

@app.route('/')
def index():
    # 確保你的 HTML 檔案放在 templates 資料夾內
    return render_template('index.html')

@app.route('/get_data', methods=['GET'])
def get_data():
    """讀取現有的排課資料"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return jsonify(json.load(f))
        except Exception as e:
            print(f"讀取 JSON 出錯: {e}")
            return jsonify({"classes": [], "teachers": [], "schedules": {}})
    return jsonify({"classes": [], "teachers": [], "schedules": {}})

@app.route('/save_data', methods=['POST'])
def save_data():
    """儲存排課資料至 data.json"""
    try:
        data = request.json
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return jsonify({"status": "success"})
    except Exception as e:
        print(f"儲存失敗: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # host='0.0.0.0' 允許同區域網路的其他裝置連線
    # port=5000 是預設埠位
    print("-----------------------------------------")
    print(" 國小排課系統後端已啟動！")
    print(" 請在瀏覽器輸入: http://127.0.0.1:5000")
    print("-----------------------------------------")
    app.run(host='0.0.0.0', port=5000, debug=True)
