## agent_upload.py는 내 에이전트에서 만들기 -> 나만 보기 설정 -> 확인 -> 수정 -> 기관내공유

import sys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time

from utils.credentials import USER_EMAIL, USER_PASSWORD
from utils.driver_setup import login_driver
from utils.login_module import perform_login
from utils.common_actions import click_make_button

agent_rule = "길 찾기용 에이전트 입니다.  서울 위주 대중교통을 안내합니다"
LOGIN_URL = "https://accounts.elice.io/accounts/signin/me?continue_to=https%3A%2F%2Fqaproject.elice.io%2Fai-helpy-chat%2Fagents&lang=en-US&org=qaproject"

PRIVATE_BUTTON = (By.XPATH, "//input[@type = 'radio' and @value='private']") #나만보기 버튼
ORG_BUTTON = (By.XPATH,"//input[@type = 'radio' and @value = 'organization']") #기관내보기
PRIVATE_STATE = (By.XPATH, "//span[normalize-space()='나만보기']") #내 에이전트 브라우저 나만보기 확인
EDIT_BUTTON = (By.XPATH, "//button[.//*[name()='svg' and @data-icon='pen']]") # 수정버튼

#main 스크립트와 동일
CREATE_BUTTON = (By.XPATH, "//button[normalize-space()='만들기']") 
CREATE_SAVE_BUTTON = (By.XPATH,"//button[@type ='submit' and normalize-space() = '저장']")
SYSTEM_PROMPT_SELECTOR = (By.NAME, 'systemPrompt')
NAME = (By.NAME, "name")
SUMMARY_INPUT = (By.XPATH, "//input[@placeholder='에이전트의 짧은 설명을 입력해보세요']")
MY_AGENTS_BUTTON = (By.XPATH, "//a[@href='/ai-helpy-chat/agents/mine']")

base_time = int(time.time())
driver = login_driver(LOGIN_URL) 
driver.maximize_window()

# 2. 로그인 실행
perform_login(driver, USER_EMAIL, USER_PASSWORD)
print(f"로그인 후 현재 URL: {driver.current_url}") 

wait = WebDriverWait(driver, 10)

#만들기 버튼 클릭
try:
    agent_btn = wait.until(EC.element_to_be_clickable(MY_AGENTS_BUTTON))
    
    agent_btn.click()
    print("[SUCCESS] 내 에이전트 클릭 완료")
    
    wait.until(EC.url_to_be("https://qaproject.elice.io/ai-helpy-chat/agents/mine"))
    print("[INFO] '/mine' 페이지로 이동 확인.")

    time.sleep(1)
    
    #나만보기, 기관내 공유 리스트
    configs = [
        {"name": f"test_{int(time.time())}", "target": "private"},
        {"name": f"test_{int(time.time())}", "target": "organization"}
    ]
    for config in configs:
    
        click_make_button(driver, wait_time =10) 
        print("--- 에이전트 생성 프로세스 시작 ---")
        
        agent_make_name = wait.until(
            EC.visibility_of_element_located(NAME)
        )
        
        #이름 입력
        agent_make_name.send_keys(config["name"])
        print(f"[SUCCESS] '{config['name']}' 이름 입력 성공!")
    
        #한줄 소개 입력
        agent_make_name = wait.until(
            EC.visibility_of_element_located(SUMMARY_INPUT)
        )
    
        agent_make_name.send_keys("길 찾기 에이전트 입니다")
        print("[SUCCESS] 한줄 소개 입력 성공!")
        
        time.sleep(2)
        
        #규칙 입력
        agent_make_rule = wait.until(
            EC.visibility_of_element_located(SYSTEM_PROMPT_SELECTOR)
        )
        agent_make_rule.send_keys(agent_rule)
        print("[SUCCESS] 규칙 입력 성공!")
        
        # 에이전트 작성 만들기 버튼
        upload_btn = wait.until(
            EC.element_to_be_clickable(CREATE_BUTTON)
                )
        upload_btn.click() 
        print("[ACTION] '만들기' 클릭 확인")  
        
        wait_long = WebDriverWait(driver,20)
        
        target_locator = PRIVATE_BUTTON if config['target'] == "private" else ORG_BUTTON
        
        #나타날 때까지 대기 후 가져오기
        radio_element = wait_long.until(EC.presence_of_element_located(target_locator))
        

        try:
     
            if not radio_element.is_selected():
                # 일반 클릭 시도
                radio_element.click()
            print(f"[SUCCESS] {config['target']} 라디오 버튼 클릭 성공")
        except:
            # 일반 클릭 실패 시 JS 강제 클릭
            driver.execute_script("arguments[0].click();", radio_element)
            print(f"[SUCCESS] {config['target']} 라디오 버튼 JS 강제 클릭 완료")
      
                    
        #완료버튼
        final_save_button = wait_long.until(
            EC.element_to_be_clickable(CREATE_SAVE_BUTTON)
        )
        driver.execute_script("arguments[0].click();", final_save_button)
        print("[SUCCESS] 에이전트 생성 및 최종 '저장' 완료.")
        
        # 4.목록 페이지 이동 확인
        time.sleep(2)
        
        if "/mine" not in driver.current_url:
            driver.get("https://qaproject.elice.io/ai-helpy-chat/agents/mine")
        
        wait_long.until(EC.url_contains("/agents/mine"))
        
        #내 에이전트에서 나만보기/기관내 공유 체크
        try:
            AGENT_CARD_XPATH = f"//a[contains(@class, 'MuiCard-root') and .//p[text()='{config['name']}']]"
            status_text = "나만보기" if config['target'] == "private" else "기관 공개"
            STATUS_XPATH = f"{AGENT_CARD_XPATH}//span[normalize-space()='{status_text}']"
            
            wait_long.until(EC.visibility_of_element_located((By.XPATH, STATUS_XPATH)))
            print(f"[PASS] 검증 성공: 목록에서 '{config['name']}' 에이전트의 '{status_text}' 상태를 확인했습니다.")
            
        except TimeoutException:
            print(f"[FAIL] 검증 실패: 목록에서 '{config['name']}' 또는 '{status_text}' 상태를 찾을 수 없습니다.")
            

    print("\n[ALL PASS] 모든 에이전트 생성 테스트가 완료되었습니다.")
        
    
except Exception as e:
    print(f"\n[CRITICAL ERROR] 자동화 프로세스 중 예상치 못한 오류 발생.")
    print(f"오류 클래스: {e.__class__.__name__}")
    print(f"오류 메시지: {e}")
    
finally:
    if 'driver' in locals() and driver:
        # 최종 상태 확인을 위해 3초 대기 후 종료
        driver.quit()
        print("\n[INFO] 드라이버 종료.")
