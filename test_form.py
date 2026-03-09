import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_successful_login(driver):
    driver.get("https://the-internet.herokuapp.com/login")
    
    username_field = driver.find_element(By.ID, "username")
    password_field = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    
    username_field.send_keys("tomsmith")
    password_field.send_keys("SuperSecretPassword!")
    login_button.click()
    
    success_message = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".flash.success"))
    )
    
    assert "You logged into a secure area!" in success_message.text
    assert "Secure Area" in driver.page_source
    
    logout_button = driver.find_element(By.CSS_SELECTOR, "a.button.secondary.radius")
    assert logout_button.is_displayed()

def test_unsuccessful_login(driver):
    # Тест с неверным логином
    driver.get("https://the-internet.herokuapp.com/login")
    
    username_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "username"))
    )
    password_field = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    
    username_field.send_keys("wrongusername")
    password_field.send_keys("SuperSecretPassword!")
    login_button.click()
    
    error_message = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".flash.error"))
    )
    
    assert "Your username is invalid!" in error_message.text
    
    # Тест с неверным паролем - создаем новый драйвер или перезагружаем страницу
    driver.get("https://the-internet.herokuapp.com/login")
    
    # ЯВНО находим элементы заново после перезагрузки страницы
    username_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "username"))
    )
    password_field = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    
    username_field.send_keys("tomsmith")
    password_field.send_keys("wrongpassword")
    login_button.click()
    
    # Ждем появления сообщения об ошибке
    error_message = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".flash.error"))
    )
    
    # Проверяем текст сообщения
    error_text = error_message.text
    assert "Your password is invalid!" in error_text, f"Expected 'Your password is invalid!', but got '{error_text}'"
    
    # Проверяем, что мы все еще на странице логина
    assert "Login Page" in driver.page_source or "login" in driver.current_url.lower()

def test_empty_fields_login(driver):
    """Дополнительный тест для проверки пустых полей"""
    driver.get("https://the-internet.herokuapp.com/login")
    
    login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    login_button.click()
    
    error_message = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".flash.error"))
    )
    
    assert "Your username is invalid!" in error_message.text

if __name__ == "__main__":
    pytest.main(["-v", "test_form.py"])
