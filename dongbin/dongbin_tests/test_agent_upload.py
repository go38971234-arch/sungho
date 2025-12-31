### 나만보기, 기관내 공유 체크 테스트

import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# 기존 유틸리티 임포트
from utils.common_actions import click_make_button

# --- 선택자 설정 ---
AGENT_MINE_URL = "https://qaproject.elice.io/ai-helpy-chat/agents/mine"
NAME_INPUT = (By.NAME, "name")
SUMMARY_INPUT = (By.XPATH, "//input[@placeholder='에이전트의 짧은 설명을 입력해보세요']")
SYSTEM_PROMPT_SELECTOR = (By.NAME, 'systemPrompt')
CREATE_BUTTON = (By.XPATH, "//button[normalize-space()='만들기']")
CREATE_SAVE_BUTTON = (By.XPATH, "//button[@type='submit' and normalize-space()='저장']")
MY_AGENTS_BUTTON = (By.XPATH, "//a[@href='/ai-helpy-chat/agents/mine']")

# 라디오 버튼 선택자
PRIVATE_RADIO = (By.XPATH, "//input[@type='radio' and @value='private']")
ORG_RADIO = (By.XPATH, "//input[@type='radio' and @value='organization']")

@pytest.mark.parametrize("target", ["private", "organization"])
def test_create_agent_visibility(driver, target):
    """에이전트 생성 시 공개 범위(나만보기/기관) 설정 및 검증 테스트"""
    wait = WebDriverWait(driver, 15)
    agent_name = f"test_{target}_{int(time.time())}"
    agent_rule = "길 찾기용 에이전트 입니다. 서울 위주 대중교통을 안내합니다."

    # 1. 내 에이전트 페이지 이동
    driver.get(AGENT_MINE_URL)
    wait.until(EC.url_contains("/agents/mine"))

    # 2. 만들기 시작 (공통 액션 함수 사용)
    click_make_button(driver, wait_time=10)
    print(f"\n--- 에이전트 생성 시작 ({target}) ---")

    # 3. 정보 입력
    wait.until(EC.visibility_of_element_located(NAME_INPUT)).send_keys(agent_name)
    wait.until(EC.visibility_of_element_located(SUMMARY_INPUT)).send_keys("길 찾기 에이전트")
    time.sleep(2)
    wait.until(EC.visibility_of_element_located(SYSTEM_PROMPT_SELECTOR)).send_keys(agent_rule)

    # 4. 1차 '만들기' 버튼 클릭
    upload_btn = wait.until(EC.element_to_be_clickable(CREATE_BUTTON))
    upload_btn.click()

    # 5. 공개 범위 라디오 버튼 선택
    target_locator = PRIVATE_RADIO if target == "private" else ORG_RADIO
    radio_element = wait.until(EC.presence_of_element_located(target_locator))
    
    # 레이어 간섭 방지를 위해 JS 클릭 사용
    driver.execute_script("arguments[0].click();", radio_element)
    print(f"[SUCCESS] {target} 라디오 버튼 선택 완료")

    # 6. 최종 저장
    final_save_btn = wait.until(EC.element_to_be_clickable(CREATE_SAVE_BUTTON))
    driver.execute_script("arguments[0].click();", final_save_btn)
    print(f"[ACTION] 최종 저장 클릭 완료")
    
    time.sleep(3)
    
    # 7. 목록으로 돌아가서 검증
    try:
        wait.until(EC.url_contains("/agents/mine"))
    except TimeoutException:
        print("[WARNING] URL 전환이 느려 강제 이동합니다.")
        driver.get(AGENT_MINE_URL)
    
    

    status_text = "나만보기" if target == "private" else "기관 공개"
    AGENT_CARD_XPATH = f"//p[text()='{agent_name}']/ancestor::a[contains(@class, 'MuiCard-root')]"
    
    try:
        card = wait.until(EC.presence_of_element_located((By.XPATH, AGENT_CARD_XPATH)))

        assert status_text in card.text
        print(f"[PASS] {agent_name} 생성 및 '{status_text}' 상태 확인 완료")
    except TimeoutException:
        pytest.fail(f"[FAIL] 목록에서 '{agent_name}'의 '{status_text}' 라벨을 찾을 수 없습니다.")