#초안 삭제 스크립트

import sys
import os
import time

current_dir = os.path.dirname(os.path.abspath(__file__))
dongbin_dir = os.path.join(current_dir, 'dongbin')
if dongbin_dir not in sys.path:
    sys.path.append(dongbin_dir)

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (TimeoutException, StaleElementReferenceException, NoSuchElementException, ElementClickInterceptedException)
from selenium.webdriver.common.keys import Keys

from utils.credentials import USER_EMAIL, USER_PASSWORD
from utils.driver_setup import login_driver
from utils.login_module import perform_login


LOGIN_URL = "https://accounts.elice.io/accounts/signin/me?continue_to=https%3A%2F%2Fqaproject.elice.io%2Fai-helpy-chat%2Fagents&lang=en-US&org=qaproject"
MY_AGENTS_BUTTON = (By.XPATH, "//a[@href='/ai-helpy-chat/agents/mine']")


AGENT_CARDS = (By.XPATH, "//a[contains(@class, 'MuiCard-root')]")
DRAFT_STATUS = (By.XPATH, ".//span[normalize-space()='초안'or normalize-space()='나만보기'or normalize-space()='기관 공개']") #나만보기, 초안 중 삭제하고 싶으면 수정
DELETE_BUTTON_IN_CARD = (By.XPATH, ".//*[@data-testid='trashIcon'] | .//*[contains(@data-icon, 'trash')]")
CONFIRM_DELETE_BUTTON = (By.XPATH, "//button[normalize-space()='삭제' or contains(text(), '삭제')]")

driver = login_driver(LOGIN_URL) 
driver.maximize_window()



  
perform_login(driver, USER_EMAIL, USER_PASSWORD)
print(f"로그인 후 현재 URL: {driver.current_url}") 


wait = WebDriverWait(driver, 10)
agent_btn = wait.until(EC.element_to_be_clickable(MY_AGENTS_BUTTON))
agent_btn.click()
wait.until(EC.url_to_be("https://qaproject.elice.io/ai-helpy-chat/agents/mine"))
print("\n--- 초안 에이전트 삭제 프로세스 시작 ---")
print("[INFO] '/mine' 페이지로 이동 완료.")


wait.until(EC.presence_of_all_elements_located(AGENT_CARDS)) 
print("[INFO] 에이전트 카드 목록 로딩 확인.")

deleted_count = 0
wait_short = WebDriverWait(driver, 5)


try:
        all_cards = driver.find_elements(*AGENT_CARDS) 
        
        print(f"[INFO] 현재 페이지에서 총 {len(all_cards)}개의 카드를 발견했습니다.")

        for card in all_cards:
            try:
                # 초안 상태 태그가 있는지 확인
                if card.find_elements(*DRAFT_STATUS): 
                    
                    # 삭제 버튼 클릭
                    delete_btn = card.find_element(*DELETE_BUTTON_IN_CARD)
                    delete_btn.click()
                    
                    # 확인 버튼 클릭
                    confirm_btn = wait_short.until(EC.element_to_be_clickable(CONFIRM_DELETE_BUTTON))
                    confirm_btn.click()
                    
                    deleted_count += 1
                    print(f"[SUCCESS] 초안 삭제 완료 ({deleted_count}번째)")
                    
                    time.sleep(1) 
                    
            except StaleElementReferenceException:
          
                print("[WARNING] 삭제 중 DOM 변경 발생 (Stale Element). 다음 카드로 스킵.")
                continue
            except TimeoutException:
                print("[FAILURE] 삭제 확인 팝업이 나타나지 않아 삭제를 완료하지 못했습니다.")
                continue
        
        print(f"\n[PASS] 총 {deleted_count}개의  에이전트를 성공적으로 삭제했습니다.")
        
except Exception as e:
  
        print(f"\n[CRITICAL ERROR] 자동화 프로세스 중 예상치 못한 오류 발생.")
        print(f"오류 클래스: {e.__class__.__name__}")
        print(f"오류 메시지: {e}")



finally:
        if 'driver' in locals() and driver:
         time.sleep(3) 
         driver.quit()
         print("\n[INFO] 드라이버 종료.")