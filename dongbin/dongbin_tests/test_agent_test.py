### 에이전트 한줄소개 텍스트 

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from utils.common_actions import click_make_button

# --- 설정 및 상수 ---
AGENT_MINE_URL = "https://qaproject.elice.io/ai-helpy-chat/agents/mine"
SUMMARY_INPUT = (By.XPATH, "//input[@placeholder='에이전트의 짧은 설명을 입력해보세요']")
LONG_TEXT = "0" * 301  # 301자 (제한 초과)
VALID_TEXT = "길 찾기 에이전트 입니다"
VALIDATION_TEXT = "한줄 소개는 최대 300자입니다"
VALIDATION_XPATH = (By.XPATH, f"//*[contains(text(), '{VALIDATION_TEXT}')]")

def test_agent_summary_length_validation(driver):
    """에이전트 한 줄 소개 300자 초과 시 유효성 메시지 노출 및 수정 테스트"""
    wait = WebDriverWait(driver, 15)
    
    # 1. 내 에이전트 페이지 이동 및 만들기 진입
    driver.get(AGENT_MINE_URL)
    click_make_button(driver, wait_time=10)
    print("\n[INFO] 한 줄 소개 유효성 테스트 시작")

    # 2. 비정상 입력 (301자)
    summary_field = wait.until(EC.visibility_of_element_located(SUMMARY_INPUT))
    summary_field.send_keys(LONG_TEXT)
    print(f"[ACTION] 301자 입력 완료")

    # 3. 경고 메시지 노출 확인 (Assertion)
    validation_msg = wait.until(EC.presence_of_element_located(VALIDATION_XPATH))
    assert validation_msg.is_displayed(), "300자 초과 시 경고 메시지가 노출되지 않았습니다."
    print(f"[SUCCESS] 유효성 검사 메시지 확인: '{VALIDATION_TEXT}'")

    # 4. 입력 내용 삭제
    summary_field.send_keys(Keys.CONTROL, "a")
    summary_field.send_keys(Keys.DELETE)
    
    # 메시지가 사라지는지 중간 확인
    wait.until(EC.invisibility_of_element_located(VALIDATION_XPATH))
    print("[INFO] 텍스트 삭제 후 메시지 사라짐 확인")

    # 5. 정상 내용 입력
    summary_field.send_keys(VALID_TEXT)
    print(f"[ACTION] 정상 내용('{VALID_TEXT}')으로 수정 완료")

    # 6. 경고 메시지가 여전히 없는지 최종 확인
    is_msg_gone = wait.until(EC.invisibility_of_element_located(VALIDATION_XPATH))
    assert is_msg_gone, "정상 입력 후에도 경고 메시지가 남아있습니다."
    print("[PASS] 한 줄 소개 유효성 검사 테스트 최종 성공")