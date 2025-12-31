### 에이전트 작성 시작 바 자동생성

import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.common_actions import click_make_button

# --- 설정 및 선택자 ---
MINE_URL = "https://qaproject.elice.io/ai-helpy-chat/agents/mine"
STARTER_FIELD = (By.XPATH, '//input[@placeholder="이 에이전트의 시작 대화를 입력하세요"]')
MAX_STARTERS = 4
STARTER_TEXTS = ["대중교통", "서울", "맛집", "길 찾기"]

def test_dynamic_starter_fields_creation(driver):
    """시작 대화 입력 시 필드가 동적으로 추가되어 최대 4개까지 생성되는지 테스트"""
    wait = WebDriverWait(driver, 10)
    
    # 1. 페이지 이동 및 만들기 진입
    driver.get(MINE_URL)
    click_make_button(driver, wait_time=10)
    print("\n[INFO] 시작 대화 동적 생성 테스트 시작")

    # 2. 필드 생성 반복문 (최대 4개)
    for i in range(MAX_STARTERS):
        expected_count = i + 1
        
        # 필드가 나타날 때까지 대기 (elements 리스트의 길이를 체크)
        wait.until(
            lambda d: len(d.find_elements(*STARTER_FIELD)) >= expected_count,
            message=f"{expected_count}번째 필드가 나타나지 않았습니다."
        )
        
        # 현재 타겟 필드 가져오기
        fields = driver.find_elements(*STARTER_FIELD)
        current_field = fields[i]
        
        # 텍스트 입력 (입력 시 다음 필드가 트리거됨)
        current_field.send_keys(STARTER_TEXTS[i])
        print(f"[SUCCESS] {expected_count}번째 필드 입력 완료: '{STARTER_TEXTS[i]}'")
        
        # 마지막 필드가 아닐 경우에만 잠시 대기하여 다음 필드 출현 유도
        if expected_count < MAX_STARTERS:
            time.sleep(0.5)

    # 3. 최종 필드 개수 검증
    final_fields = driver.find_elements(*STARTER_FIELD)
    assert len(final_fields) == MAX_STARTERS, f"최종 필드 개수 오류: 예상 {MAX_STARTERS}, 실제 {len(final_fields)}"
    print(f"[PASS] 총 {MAX_STARTERS}개 필드 생성 및 입력 확인 완료")

    # 4. 최대 개수 초과 제한 확인

    time.sleep(1.5)
    extra_fields = driver.find_elements(*STARTER_FIELD)
    assert len(extra_fields) == MAX_STARTERS, "최대 개수를 초과하여 필드가 생성되었습니다."
    print("[PASS] 4개 초과 생성 제한 확인 완료")