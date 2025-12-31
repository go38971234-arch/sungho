###내 에이전트 초안 작성 확인 테스트

import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# --- 선택자 설정 ---
MINE_URL = "https://qaproject.elice.io/ai-helpy-chat/agents/mine"
MY_AGENTS_BUTTON = (By.XPATH, "//a[@href='/ai-helpy-chat/agents/mine']")
MAKE_BUTTON = (By.XPATH, "//a[normalize-space()='만들기']")
NAME_INPUT = (By.NAME, "name")
SUMMARY_INPUT = (By.XPATH, "//input[@placeholder='에이전트의 짧은 설명을 입력해보세요']")
RULE_TEXTAREA = (By.NAME, 'systemPrompt')
BACK_BUTTON = (By.XPATH, "//button[@aria-label='뒤로가기']")

def test_agent_auto_draft_on_back(driver):
    """에이전트 작성 중 뒤로가기 시 '초안' 저장 여부 테스트"""
    wait = WebDriverWait(driver, 15)
    
    # 1. 고유한 에이전트 정보 생성
    unique_id = int(time.time())
    agent_name = f"draft_test_{unique_id}"
    
    # 2. 내 에이전트 페이지 이동
    driver.get(MINE_URL)
    print(f"\n[INFO] 에이전트 목록 페이지 접속")

    # 3. 만들기 진입
    make_btn = wait.until(EC.element_to_be_clickable(MAKE_BUTTON))
    make_btn.click() 
    
    # 4. 필드 입력 (이름, 한 줄 소개, 규칙)
    wait.until(EC.visibility_of_element_located(NAME_INPUT)).send_keys(agent_name)
    wait.until(EC.visibility_of_element_located(SUMMARY_INPUT)).send_keys("자동 저장 테스트 중")
    wait.until(EC.visibility_of_element_located(RULE_TEXTAREA)).send_keys("이것은 초안 저장 테스트 규칙입니다.")
    print(f"[SUCCESS] 에이전트 정보 입력 완료: {agent_name}")
    

    time.sleep(2)
    
    # 5. '뒤로가기' 클릭 (저장 버튼 안 누름)
    back_btn = wait.until(EC.element_to_be_clickable(BACK_BUTTON))
    back_btn.click()
    print("[ACTION] 저장 없이 '뒤로가기' 클릭")
    
    # 6. 목록 복귀 확인
    wait.until(EC.url_to_be(MINE_URL))
 
    DRAFT_CARD_XPATH = f"//a[contains(@class, 'MuiCard-root')]//p[text()='{agent_name}']/ancestor::a//span[normalize-space()='초안']"
    
    try:
        draft_label = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, DRAFT_CARD_XPATH))
        )
        assert draft_label.is_displayed(), "초안 라벨이 화면에 표시되지 않습니다."
        print(f"[PASS] 검증 완료: '{agent_name}'이(가) '초안' 상태로 저장되었습니다.")
        
    except TimeoutException:
        pytest.fail(f"[FAIL] '{agent_name}' 에이전트의 '초안' 상태를 찾을 수 없습니다. (자동 저장 실패)")