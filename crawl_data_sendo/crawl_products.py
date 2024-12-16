from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def setting_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument("--disable-webgl")
    # options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--lang=vi")
    driver = webdriver.Chrome(service=Service("./chrome_driver/chromedriver-win64/chromedriver.exe"), options=options)
    return driver

def crawl_id_product(url, driver, number_comment):
    number_product = number_comment / 20
    driver.get(url)
    time.sleep(8)
    products = None
    lazy_load(driver=driver)
    time.sleep(8)
    while True:
        products = driver.find_elements(
            By.XPATH, 
            "//div[@class='d7ed-fdSIZS d7ed-OoK3wU d7ed-mPGbtR']//a"
        )
        if len(products) >= number_product:
            products = [
                product.get_attribute("href")
                for product in products
                if "html?" in product.get_attribute("href")
            ]
            break
        else:
            while check_null("//button[@class='d7ed-s0YDb1 d7ed-jQXTxb d7ed-ZPZ4Mf d7ed-YaJkXL d7ed-bTLFAv']", driver) is None:
                lazy_load(driver=driver, check_box = True)
            load_more_button = WebDriverWait(driver, 240).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@class='d7ed-s0YDb1 d7ed-jQXTxb d7ed-ZPZ4Mf d7ed-YaJkXL d7ed-bTLFAv']"))
            )
            load_more_button.click()
    return products

def check_null(xpath, driver):
    try:
        return driver.find_element(By.XPATH, xpath)
    except:
        return None

def lazy_load(driver, check_box=False):
    last_scroll_position = 0
    if check_box:
        document_height = driver.execute_script("return document.body.scrollHeight;")
        scroll_up_position = document_height * 0.3
        driver.execute_script(f"window.scrollTo(0, {scroll_up_position});")
        time.sleep(5)
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(10)
        new_scroll_position = driver.execute_script("return window.pageYOffset;")
        if new_scroll_position == last_scroll_position:
            break
        last_scroll_position = new_scroll_position

if __name__ == "__main__":
    url = "https://www.sendo.vn/"
    driver = setting_driver()
    products = crawl_id_product(url, driver, number_comment=3200)
    print(products)
    with open("./data/products_id.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(products))
    driver.quit()