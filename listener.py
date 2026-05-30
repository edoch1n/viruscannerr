from flask import Flask, request, jsonify
import json
from datetime import datetime

app = Flask(__name__)

@app.route('/capture', methods=['POST'])
def capture():
    data = request.json
    with open("gelen_veriler.txt", "a", encoding="utf-8") as f:
        f.write(f"\n[{datetime.now()}]\n{json.dumps(data, indent=2, ensure_ascii=False)}\n")
    print(f"\n🔴 YENİ VERİ GELDİ:\n{json.dumps(data, indent=2, ensure_ascii=False)}")
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
