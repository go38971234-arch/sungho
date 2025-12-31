# driver_setup.py

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def login_driver(url: str, implicit_wait_time: int = 10, sleep_time: int = 2):

    
    chrome_options = Options()
    
    # 1. 브라우저 닫힘 방지 옵션 (스크립트 종료 후에도 창 유지)
    chrome_options.add_experimental_option("detach", True) 
    
    # 2. 필수 옵션 (리눅스/자동화 환경에서 안정적인 실행을 위해 필요)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # 드라이버 생성 (WebDriver Manager가 자동으로 Chrome 버전에 맞는 드라이버 설치)
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Implicit Wait 설정
    driver.implicitly_wait(implicit_wait_time) 
    
    # URL 접속
    driver.get(url)
    time.sleep(sleep_time) # 페이지 로드 후 추가 대기 (필요 시)
    
    return driver