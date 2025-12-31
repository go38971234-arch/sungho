#ai 비정상 질문

import time
import json
import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from utils.chat_utils import get_latest_ai_answer,wait_for_AI_complete #chat_utils 모듈
from utils.credentials import USER_EMAIL, USER_PASSWORD
from utils.driver_setup import login_driver
from utils.login_module import perform_login

LOGIN_URL = "https://accounts.elice.io/accounts/signin/me?continue_to=https%3A%2F%2Fqaproject.elice.io%2Fai-helpy-chat%2Fagents&lang=en-US&org=qaproject"
MAKE_BUTTON = (By.XPATH, "//a[normalize-space()='만들기']")

CHAT_CREATE_BUTTON = (By.CSS_SELECTOR, "button[value='chat']") #대화로 버튼
MESSAGE_TEXTAREA = (By.NAME, "input") #ai챗 입력
AI_CHAT_BUBBLE = (By.CSS_SELECTOR, "div.elice-aichat__markdown")

current_dir = os.path.dirname(os.path.abspath(__file__))
results_dir = os.path.join(current_dir, "results")
file_path = os.path.join(results_dir, "abnormal_test_log.json")

scenario_questions = ["ㅁㄴㅇ123"] * 4
conversation_history = []

driver = login_driver(LOGIN_URL) 
driver.maximize_window()

try:
    #로그인 실행
    perform_login(driver, USER_EMAIL, USER_PASSWORD)
    print(f"로그인 후 현재 URL: {driver.current_url}") 

    wait = WebDriverWait(driver, 10)

    print("--- 에이전트 생성 프로세스 시작 ---")

    #만들기 버튼 클릭
    make_btn = wait.until(EC.element_to_be_clickable(MAKE_BUTTON))
    make_btn.click()
    print("[SUCCESS] 내 에이전트 클릭 완료")
    
    print("\n--- AI 에이전트 대화 생성 시작 ---")
    
    #대화로 만들기 클릭
    
    ai_chat_make = wait.until(EC.element_to_be_clickable(CHAT_CREATE_BUTTON))
    ai_chat_make.click()
    print("[SUCCESS] 대화로 만들기 클릭 완료")
    
    for i, question in enumerate(scenario_questions, 1):
        # 질문 전송 전 현재 말풍선 개수 파악
        current_bubbles = driver.find_elements(*AI_CHAT_BUBBLE)
        before_count = len(current_bubbles)
        
        print(f"\n[Abnormal Step {i}] 나: {question}")
        
        input_box = wait.until(EC.element_to_be_clickable(MESSAGE_TEXTAREA))
        input_box.send_keys(question)
        input_box.send_keys(Keys.ENTER)
        
        print("AI가 비정상 입력에 반응 중입니다...", end="", flush=True)
        
        # 새로운 답변이 완료될 때까지 대기
        final_answer = wait_for_AI_complete(driver, before_count, timeout=60)
        print(f"\n[AI 반응]: {final_answer[:100]}...")
        
        conversation_history.append({
            "order": i,
            "user_input": question,
            "ai_response": final_answer
        })

except Exception as e:
    print(f"\n[FAIL] 테스트 중 오류 발생: {e}")

finally:
    if conversation_history:
        os.makedirs(results_dir, exist_ok=True)
        
        # 결과 데이터 구조
        new_entry = {
            "test_type": "비정상 입력 테스트 (의미 없는 문자열)",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "full_chat": conversation_history
        }

        if os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    existing_data = json.load(f)
                if isinstance(existing_data, list):
                    existing_data.append(new_entry)
                else:
                    existing_data = [existing_data, new_entry]
            except:
                existing_data = [new_entry]
        else:
            existing_data = [new_entry]

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(existing_data, f, ensure_ascii=False, indent=4)

        print(f"\n[SUCCESS] 비정상 테스트 로그 저장 완료: {file_path}")
        
        
        if 'driver' in locals() and driver:
            time.sleep(3) 
            driver.quit()
            print("\n[INFO] 드라이버 종료.")