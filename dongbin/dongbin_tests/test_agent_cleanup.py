### 내 에이전트 자동 삭제 스크립트

import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (TimeoutException, StaleElementReferenceException, NoSuchElementException)

# --- 선택자 설정 ---
MINE_URL = "https://qaproject.elice.io/ai-helpy-chat/agents/mine"
AGENT_CARDS = (By.XPATH, "//a[contains(@class, 'MuiCard-root')]")
# 삭제 대상 상태 정의 (초안, 나만보기, 기관 공개)
DRAFT_STATUS = (By.XPATH, ".//span[normalize-space()='초안' or normalize-space()='나만보기' or normalize-space()='기관 공개']")
DELETE_ICON = (By.XPATH, ".//*[@data-testid='trashIcon'] | .//*[contains(@data-icon, 'trash')]")
CONFIRM_DELETE_BUTTON = (By.XPATH, "//button[normalize-space()='삭제' or contains(text(), '삭제')]")

def test_cleanup_test_agents(driver):
    """생성된 테스트용 에이전트들을 상태별로 필터링하여 일괄 삭제"""
    wait = WebDriverWait(driver, 10)
    while True:
        # 1. 매번 목록을 새로 읽어옵니다
        driver.get(MINE_URL)
     
        
        # 2. 삭제 대상 찾기
        cards = driver.find_elements(By.CSS_SELECTOR, "a[class*='MuiCard-root']")
        
        if not cards:
            print("[INFO] 모든 에이전트가 삭제되었습니다. 목록이 비어있습니다.")
            break
        

        try:
            target_card = cards[0]
            delete_btn = target_card.find_element(By.CSS_SELECTOR, "button:has([data-testid='trashIcon'])")
            
      
            driver.execute_script("arguments[0].click();", delete_btn)
            print(f"[ACTION] 카드 삭제 버튼 클릭 완료")


            confirm_xpath = "//div[@role='dialog']//button[contains(., '삭제') or contains(., '확인')]"
            confirm_btn = wait.until(EC.element_to_be_clickable((By.XPATH, confirm_xpath)))
            confirm_btn.click()
            
            wait.until(EC.invisibility_of_element_located((By.XPATH, "//div[@role='dialog']")))
            
            print("[SUCCESS] 1개 삭제 완료. 다음 카드로 이동합니다.")
            
        except Exception as e:
            print(f"[ERROR] 삭제 중 오류 발생: {e}")
            break 