import pytest
import time
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

parent_dir = os.path.dirname(current_dir)

if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

print(f"\n[DEBUG] Project Root added to sys.path: {parent_dir}")

from utils.driver_setup import login_driver
from utils.login_module import perform_login
from utils.credentials import USER_EMAIL, USER_PASSWORD

@pytest.fixture(scope="session")
def driver():
    """전체 테스트 세션 동안 브라우저를 하나만 유지"""
    url = "https://qaproject.elice.io/ai-helpy-chat"
    driver = login_driver(url)
    driver.maximize_window()
    
    # 1. 공통 로그인 수행
    perform_login(driver, USER_EMAIL, USER_PASSWORD)
    time.sleep(2)
    
    yield driver  # 테스트 함수들에 드라이버 전달
    
    print("\n[INFO] 모든 테스트 종료. 드라이버를 닫습니다.")
    driver.quit()