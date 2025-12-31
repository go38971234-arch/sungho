from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def click_make_button(driver, wait_time =10):
    """
    WebDriver를 사용하여 '만들기' 버튼을 클릭하고 다음 화면으로 넘어갈 때까지 대기합니다.
    """
    wait = WebDriverWait(driver, wait_time)
    
    #'만들기' 버튼을 클릭 가능한 상태가 될 때까지 기다립니다.
    make_btn_xpath = "//a[normalize-space()='만들기']"
    
    agent_make_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, make_btn_xpath)))
    
    agent_make_btn.click()
    print("[Common Action] '만들기' 버튼 클릭 성공.")
    time.sleep(1)
    
    # 모달 또는 다음 페이지의 요소가 나타날 때까지 대기 (이름 입력 필드로 가정)
    wait.until(
        EC.visibility_of_element_located((By.NAME, "name")))
    print("[Common Action] 에이전트 생성 모달 로딩 확인.")
