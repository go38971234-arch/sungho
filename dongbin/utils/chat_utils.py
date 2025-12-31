#AI가 말하는 거 가져오는 모듈

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

AI_CHAT_BUBBLE = (By.CSS_SELECTOR, "div.elice-aichat__markdown")
AI_COMPLETE_BUBBLE = (By.CSS_SELECTOR, "div.elice-aichat__markdown[data-status='complete']") # 수정된 로케이터 (완료된 것만 찾기)

def get_latest_ai_answer(driver, wait, timeout=10):
    """화면에 표시된 답변들 중 가장 마지막 답변을 가져옴"""
    try:
        # 답변 요소가 나타날 때까지 대기
        wait.until(EC.presence_of_element_located(AI_CHAT_BUBBLE))
   
        time.sleep(2) 
        
        all_responses = driver.find_elements(*AI_CHAT_BUBBLE)
        
        if all_responses:
            #가장 마지막 요소의 텍스트 반환
            return all_responses[-1].text
        return "답변 요소를 찾을 수 없음"
    except Exception as e:
        return f"답변 추출 중 오류 발생: {e}"

def wait_for_AI_complete(driver, previous_count, timeout=30):
    wait = WebDriverWait(driver, timeout)
    
    try:
        # 1. 말풍선 개수가 이전보다 늘어날 때까지 대기
        wait.until(lambda d: len(d.find_elements(*AI_CHAT_BUBBLE)) > previous_count)
        
        # 2. 늘어난 말풍선들 중 가장 마지막 요소가 'complete'가 될 때까지 대기
        wait.until(lambda d: d.find_elements(*AI_CHAT_BUBBLE)[-1].get_attribute("data-status") == "complete")
        
        # 3. 완료된 마지막 답변의 텍스트 반환
        all_responses = driver.find_elements(*AI_CHAT_BUBBLE)
        return all_responses[-1].text
        
    except Exception as e:
        print(f"\n[대기 오류] 답변 대기 중 문제 발생: {e}")
        return "답변 추출 실패 또는 페이지 전환됨"