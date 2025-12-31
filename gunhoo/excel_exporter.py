import json
import os
from openpyxl import Workbook

JSON_DIR = "TC-CHAT-JSON"
EXCEL_DIR = "TC-CHAT-EXCEL"
OUTPUT_FILE = "chatbot_test_results.xlsx"

def export_json_to_excel():
    # 엑셀 저장 폴더 생성
    os.makedirs(EXCEL_DIR, exist_ok=True) # 폴더 확인, 없으면 생성

    wb = Workbook()
    ws = wb.active
    ws.title = "Chatbot Test Results"

    # 헤더
    ws.append(["TC ID", "Question", "Answer"])

    for filename in os.listdir(JSON_DIR):  # 모든 파일 순회, 가져옴
        if not filename.endswith(".json"): # 그중 .json이 아닌 파일 무시, 필터링. 즉 다른 파일있어도 충돌안남
            continue

        filepath = os.path.join(JSON_DIR, filename) # 알맞은 경로 생성

        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        tc_id = data["tc_id"]

        for item in data["results"]: # 연속 질문 형태 저장
            ws.append([
                tc_id,
                item["question"],
                item["answer"]
            ])

    output_path = os.path.join(EXCEL_DIR, OUTPUT_FILE)
    wb.save(output_path)

    print(f"엑셀 저장 완료 → {output_path}")


if __name__ == "__main__": # 엑셀 저장 코드 실행은 직접 실행으로만 실행, 다른 파일에서 import 금지 
    export_json_to_excel()
