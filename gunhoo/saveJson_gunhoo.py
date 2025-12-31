import json
import os

SAVE_DIR = "TC-CHAT-JSON"

def save_json(filename, data):
    """
    JSON 데이터를 TC-CHAT-JSON 폴더에 저장
    """

    # 📁 폴더가 없으면 생성
    os.makedirs(SAVE_DIR, exist_ok=True)

    # 📄 전체 파일 경로 생성
    file_path = os.path.join(SAVE_DIR, filename)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"JSON 저장 완료 → {file_path}")