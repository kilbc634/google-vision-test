from flask import Flask, request, jsonify
import os
from vision_context import extract_text

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_image():
    # 確認有附檔
    if 'file' not in request.files:
        return jsonify({"error": "Missing file field"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400

    try:
        os.remove("pending.png")
    except FileNotFoundError:
        pass

    # if os.path.exists("pending.png"):
    #     return jsonify({"error": "pending.png already exists"}), 409

    # 儲存圖片
    file.save("pending.png")

    # 呼叫 Vision 處理函式
    try:
        result = extract_text("pending.png")
    except Exception as e:
        return jsonify({"error": f"extract_text failed: {str(e)}"}), 500

    print(f"[✓] Extracted Text:\n{result}")
    return jsonify({"text": result})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=19862)