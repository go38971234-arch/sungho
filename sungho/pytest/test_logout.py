from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utills import (login,logout,type_text,click_element)

def test_login_logout(driver):
        # TC-LOGOUT-17,18 테스트 순차적으로 진행 
        login(driver, "qa3team03@elicer.com", "@qa12345")
        print("로그인 완료")
        logout(driver)
        print("TC17-로그인 후 로그아웃 완료")

        type_text(driver, "Password", "@qa12345")
        click_element(driver, "button[type='submit']")
        
        WebDriverWait(driver, 15).until(
                EC.url_contains("/ai-helpy-chat")
            )
        icon = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, '[data-testid="PersonIcon"]')
        )
    )
        assert icon.is_displayed()
        print("✔ ai-helpy-chat 페이지 이동 확인 (테스트 성공)")
        print("TC18 재로그인 성공")
    
