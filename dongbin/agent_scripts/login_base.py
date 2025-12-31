import os
import sys

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from credentials import USER_EMAIL, USER_PASSWORD
from utils.driver_setup import login_driver
from utils.login_module import perform_login

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, '..')
sys.path.append(project_root)

LOGIN_URL = "https://accounts.elice.io/accounts/signin/me?continue_to=https%3A%2F%2Fqaproject.elice.io%2Fai-helpy-chat%2Fagents&lang=en-US&org=qaproject"

# 1. 브라우저 초기화 및 창 최대화 (가장 중요한 안정화 조치)
driver = login_driver(LOGIN_URL) 
driver.maximize_window()

# 2. 로그인 실행
perform_login(driver, USER_EMAIL, USER_PASSWORD)
print(f"[INFO] 로그인 후 현재 URL: {driver.current_url}") 

# 3. WebDriverWait 객체 생성 (다음 테스트 로직에서 사용)
# 대부분의 요소 찾기 대기에 사용되므로 15초 정도로 설정하는 것이 안전합니다.
wait = WebDriverWait(driver, 15) 

print("--- 자동 로그인 및 초기 설정 완료. 테스트 로직을 여기에 추가하세요. ---")



# 4. 테스트 종료 및 드라이버 종료 (항상 finally 블록 사용 권장)
try:
    pass # 실제 테스트 로직이 들어가는 곳
    
except Exception as e:
    print(f"\n[CRITICAL ERROR] 자동화 프로세스 중 오류 발생.")
    print(f"오류 클래스: {e.__class__.__name__}")
    print(f"오류 메시지: {e}")
    
finally:
    if 'driver' in locals() and driver:
        # 드라이버 객체가 존재할 경우에만 종료합니다.
        driver.quit()
        print("\n[INFO] 드라이버 종료.")