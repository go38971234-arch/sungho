import os
import sys

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

from utils.credentials import USER_EMAIL, USER_PASSWORD
from utils.driver_setup import login_driver
from utils.login_module import perform_login
from utils.common_actions import click_make_button

agent_rule = "길 찾기용 에이전트 입니다.  서울 위주 대중교통을 안내합니다"

#파일 업로드
file_name = "elice_logo.png"
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, file_name)

project_root = os.path.join(current_dir, '..')
sys.path.append(project_root)
 
LOGIN_URL = "https://accounts.elice.io/accounts/signin/me?continue_to=https%3A%2F%2Fqaproject.elice.io%2Fai-helpy-chat%2Fagents&lang=en-US&org=qaproject"


ALL_CHECKBOXES_SELECTOR = (By.CSS_SELECTOR, 'input[name="toolIds"][type="checkbox"]') #체크박스 선택자
STARTER_FIELD_XPATH = (By.XPATH, '//input[@placeholder="이 에이전트의 시작 대화를 입력하세요"]') #시작대화
SYSTEM_PROMPT_SELECTOR = (By.NAME, 'systemPrompt') #규칙
NAME = (By.NAME, "name") #이름
SUMMARY_INPUT = (By.XPATH, "//input[@placeholder='에이전트의 짧은 설명을 입력해보세요']") #한줄소개

#만들기 버튼
CREATE_BUTTON = (By.XPATH, "//button[normalize-space()='만들기']")
CREATE_SAVE_BUTTON = (By.XPATH,"//button[@type ='submit' and normalize-space() = '저장']")

driver = login_driver(LOGIN_URL) 
driver.maximize_window()

# 2. 로그인 실행
perform_login(driver, USER_EMAIL, USER_PASSWORD)
print(f"로그인 후 현재 URL: {driver.current_url}") 

wait = WebDriverWait(driver, 10)

#만들기 버튼 클릭
try:
    click_make_button(driver, wait_time =10) 
    print("--- 에이전트 생성 프로세스 시작 ---")
    
    agent_make_name = wait.until(
        EC.visibility_of_element_located(NAME)
    )
    
    #이름 입력
    agent_make_name.send_keys("동빈")
    print("[SUCCESS] 이름 입력 성공!")
   
    #한줄 소개 입력
    agent_make_name = wait.until(
        EC.visibility_of_element_located(SUMMARY_INPUT)
    )
   
    agent_make_name.send_keys("길 찾기 에이전트 입니다")
    print("[SUCCESS] 한줄 소개 입력 성공!")
     
    #규칙 입력
    agent_make_rule = wait.until(
        EC.visibility_of_element_located(SYSTEM_PROMPT_SELECTOR)
    )
    agent_make_rule.send_keys(agent_rule)
    print("[SUCCESS] 규칙 입력 성공!")
    
    #시작 대화 입력
    agent_starter_field = wait.until(
        EC.visibility_of_element_located(STARTER_FIELD_XPATH)
    )
    agent_starter_field.send_keys("대중교통")
    print("[SUCCESS] 시작 대화 입력 성공!")
     
    #파일 업로드
    file_upload = driver.find_element(By.XPATH,"//input[@type='file']")
    file_upload.send_keys(file_path)
    print(f"[SUCCESS] 파일 업로드 완료: {file_name}")
     
    # ALL_CHECKBOXES_SELECTOR = (By.CSS_SELECTOR, 'input[name="toolIds"][type="checkbox"]')
    # 체크박스 중복 테스트
    try:
        
        checkboxes = wait.until(
            EC.presence_of_all_elements_located(ALL_CHECKBOXES_SELECTOR) # 모든 체크박스가 나타날 때까지 대기
            )   
           
        if checkboxes :
            print(f"총 {len(checkboxes)}개의 체크박스 발견. 중복 선택 테스트 시작")
            
            for i, box in enumerate(checkboxes):
                if not box.is_selected():
                    box.click()
                    box_value = box.get_attribute('value')
                    print(f"[{i+1}]번째 체크박스 ({box_value}) 클릭 완료.")
                   
            is_all_checked = all(box.is_selected() for box in checkboxes)

            if is_all_checked:
                print("[SUCCESS] 모든 체크박스가 성공적으로 중복 선택(다중 선택)되었습니다.")
            else:
                print("[FAIL] 중복 선택 테스트 실패. 일부 체크박스가 선택되지 않았습니다.")

                
            
                
    except NameError:
        print("[ERROR] 'driver' 객체가 정의되지 않았습니다. WebDriver를 먼저 초기화해야 합니다.")
    except Exception as e:
        print(f"[UNEXPECTED ERROR] 테스트 실행 중 오류 발생: {e}")

# 에이전트 작성 만들기 버튼
    upload_btn = wait.until(
        EC.element_to_be_clickable(CREATE_BUTTON)
             )
    upload_btn.click() 
    print("[ACTION] '만들기' 클릭 후, 게시 설정 팝업의 최종 '저장' 버튼 클릭 시도...")      
# 만들기 최종 확인 버튼    
    final_save_button = wait.until(
        EC.element_to_be_clickable(CREATE_SAVE_BUTTON)
    )
    final_save_button.click()
    print("[SUCCESS] 에이전트 생성 및 최종 '저장' 완료.")
    
    wait.until(EC.url_contains("/agents/mine")) 
    print("[INFO] '내 에이전트' 목록 페이지로 이동 확인.")
      
except Exception as e:
    print(f"\n[CRITICAL ERROR] 자동화 프로세스 중 오류 발생.")
    print(f"오류 클래스: {e.__class__.__name__}")
    print(f"오류 메시지: {e}")
    
finally:
    if 'driver' in locals() and driver:
        driver.quit()
        print("\n[INFO] 드라이버 종료.")