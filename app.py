from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# 所有的資料都統一存在這裡
db_data = {
    "classes": [], # 格式: {"id": 1, "name": "101", "subjects": {"國語": 6}}
    "subjects": ["國語", "英語", "本土語", "數學", "社會", "自然", "體育", "健康", "美勞", "音樂", "生活", "綜合", "閱讀", "本位", "資訊"]
}

@app.route('/')
def index():
    return render_template('index.html')

# 取得目前所有資料
@app.route('/get_data', methods=['GET'])
def get_data():
    return jsonify(db_data)

# 儲存所有資料 (當前端按下儲存或變動時呼叫)
@app.route('/save_data', methods=['POST'])
def save_data():
    global db_data
    incoming_data = request.json
    db_data["classes"] = incoming_data.get('classes', [])
    db_data["subjects"] = incoming_data.get('subjects', db_data["subjects"])
    return jsonify({"status": "success", "message": "伺服器已同步"})

if __name__ == '__main__':
    print("排課系統已啟動：http://127.0.0.1:5000")
    app.run(debug=True, port=5000)