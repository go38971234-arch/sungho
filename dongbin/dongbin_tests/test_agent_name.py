### 에이전트 이름 비정상 테스트

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from utils.common_actions import click_make_button

# --- 설정 및 상수 ---
AGENT_MINE_URL = "https://qaproject.elice.io/ai-helpy-chat/agents/mine"
NAME_INPUT = (By.NAME, "name")
VALID_NAME = "동빈"
LONG_NAME = "0" * 101  # 101자 (제한 초과)
VALIDATION_TEXT = "이름은 최대 100자입니다"
VALIDATION_XPATH = (By.XPATH, f"//*[contains(text(), '{VALIDATION_TEXT}')]")

def test_agent_name_length_validation(driver):
    """에이전트 이름 100자 초과 시 유효성 메시지 노출 및 수정 테스트"""
    wait = WebDriverWait(driver, 15)
    
    # 1. 내 에이전트 페이지 이동 및 만들기 진입
    driver.get(AGENT_MINE_URL)
    click_make_button(driver, wait_time=10)
    print("\n[INFO] 에이전트 이름 유효성 테스트 시작")

    # 2. 비정상 입력 (101자)
    name_field = wait.until(EC.visibility_of_element_located(NAME_INPUT))
    name_field.send_keys(LONG_NAME)
    print(f"[ACTION] 101자 입력 완료")

    # 3. 경고 메시지 노출 확인 (Assertion)
    validation_msg = wait.until(EC.presence_of_element_located(VALIDATION_XPATH))
    assert validation_msg.is_displayed(), "100자 초과 시 경고 메시지가 노출되지 않았습니다."
    print(f"[SUCCESS] 유효성 검사 메시지 확인: '{VALIDATION_TEXT}'")

    # 4. 입력 내용 삭제 후 정상 이름 입력
    name_field.send_keys(Keys.CONTROL, "a")
    name_field.send_keys(Keys.DELETE)
    name_field.send_keys(VALID_NAME)
    print(f"[ACTION] 정상 이름('{VALID_NAME}')으로 수정 완료")

    # 5. 경고 메시지가 사라졌는지 확인
    is_msg_gone = wait.until(EC.invisibility_of_element_located(VALIDATION_XPATH))
    assert is_msg_gone, "정상 입력 후에도 경고 메시지가 사라지지 않았습니다."
    print("[PASS] 유효성 검사 메시지 사라짐 확인 완료")