### 퀴즈생성 테스트

import pytest
import time
import json
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# --- 선택자 설정 (기존 코드 유지) ---
QUIZ_TOOL_URL = "https://qaproject.elice.io/ai-helpy-chat/tools/98b00265-c2fb-43cc-8785-5330e18f8c28"
OPTION_TYPE_DROPDOWN = (By.ID, "mui-component-select-quiz_configs.0.option_type")
DIFFICULTY_DROPDOWN = (By.ID, "mui-component-select-quiz_configs.0.difficulty")
QUIZ_TEXTAREA = (By.NAME, "content")
FIRST_SUBMIT_BTN = (By.CSS_SELECTOR, "button[type='submit'].MuiButton-sizeLarge")
SECOND_SUBMIT_BTN = (By.CSS_SELECTOR, "button[type='submit'].MuiButton-sizeMedium")
QUIZ_RESULT_CONTAINER = (By.CSS_SELECTOR, "div.MuiStack-root.css-1id3s5p")

def select_dropdown_option(driver, dropdown_locator, option_text):
    wait = WebDriverWait(driver, 10)
    dropdown = wait.until(EC.element_to_be_clickable(dropdown_locator))
    dropdown.click()
    time.sleep(0.5) 
    option_xpath = f"//li[@role='option' and contains(text(), '{option_text}')]"
    option = wait.until(EC.element_to_be_clickable((By.XPATH, option_xpath)))
    option.click()
    time.sleep(0.5)

def test_ai_quiz_generation(driver):
    """AI 퀴즈 생성 도구 테스트 (ISTQB 주제)"""
    # 1. 퀴즈 도구 페이지로 이동
    driver.get(QUIZ_TOOL_URL)
    wait = WebDriverWait(driver, 20)
    print(f"\n[INFO] 퀴즈 페이지 이동 완료")

    # 2. 옵션 설정
    select_dropdown_option(driver, OPTION_TYPE_DROPDOWN, "객관식 (단일 선택)")
    select_dropdown_option(driver, DIFFICULTY_DROPDOWN, "하")
    
    # 3. 주제 입력 (기존 내용 삭제 후 ISTQB 입력)
    textarea = wait.until(EC.element_to_be_clickable(QUIZ_TEXTAREA))
    textarea.click()
    textarea.send_keys(Keys.CONTROL + "a")
    textarea.send_keys(Keys.BACKSPACE)
    textarea.send_keys("ISTQB")
    print("[SUCCESS] 주제 입력 완료: 'ISTQB'")
    
    # 4. 1차 생성 클릭
    first_btn = wait.until(EC.element_to_be_clickable(FIRST_SUBMIT_BTN))
    driver.execute_script("arguments[0].click();", first_btn)
    print("[SUCCESS] 1차 생성 버튼 클릭")

    # 이전 텍스트 저장을 위해 1차 응답 대기
    time.sleep(5) 
    old_result_text = driver.find_element(*QUIZ_RESULT_CONTAINER).text
    
    # 5. 2차 '다시 생성' 클릭
    second_btn = wait.until(EC.presence_of_element_located(SECOND_SUBMIT_BTN))
    driver.execute_script("arguments[0].click();", second_btn)
    print("[SUCCESS] 2차 '다시 생성' 클릭 완료")

    # 6. 데이터 갱신 및 최종 수집 대기
    print("새로운 퀴즈 데이터 생성 대기 중 (최대 60초)...")
    WebDriverWait(driver, 60).until(
        lambda d: d.find_element(*QUIZ_RESULT_CONTAINER).text != old_result_text 
        and len(d.find_element(*QUIZ_RESULT_CONTAINER).text) > 100
    )
    
    # AI가 텍스트를 끝까지 타이핑할 시간을 줌
    time.sleep(10)
    final_quiz_result = driver.find_element(*QUIZ_RESULT_CONTAINER).text
    
    # --- [검증 단계] ---
    assert "ISTQB" in final_quiz_result, "퀴즈 내용에 'ISTQB'가 포함되어 있지 않습니다."
    assert len(final_quiz_result) > 100, "퀴즈 내용이 너무 짧습니다."
    print("[PASS] 퀴즈 생성 및 데이터 검증 성공")

    # --- [데이터 저장 단계] ---
    save_quiz_to_json(final_quiz_result)

def save_quiz_to_json(content):
    """결과 데이터를 JSON 파일로 저장"""
    results_dir = os.path.join(os.getcwd(), "dongbin", "results")
    os.makedirs(results_dir, exist_ok=True)
    file_path = os.path.join(results_dir, "quiz_gen_log.json")

    new_data = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "user_input": "ISTQB 퀴즈 생성",
        "quiz_content": content,
        "config": {"type": "객관식", "difficulty": "하"}
    }

    data = []
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                if not isinstance(data, list): data = [data]
            except: data = []

    data.append(new_data)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"[INFO] 결과 저장 완료: {file_path}")