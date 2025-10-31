from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time


options = Options()
options.binary_location = r"F:\Google\Chrome\Application\chrome.exe"  # 你的chrome路径
options.add_argument("--start-maximized")
options.add_experimental_option("detach", True)

service = Service(r"E:\Code\130.0.6723.58 chromedriver-win64\chromedriver-win64\chromedriver.exe")  # 手动指定驱动路径
driver = webdriver.Chrome(service=service, options=options)



driver.get("https://www.cnki.net/")

# 输入搜索词
search_box = driver.find_element(By.CLASS_NAME, "search-input")
search_box.send_keys("人工智能")

# 点击搜索按钮
search_button = driver.find_element(By.CLASS_NAME, "search-btn")
search_button.click()
time.sleep(3)  # 等待搜索结果加载

# 找到所有 tbody
tbodys = driver.find_elements(By.CSS_SELECTOR, "table.result-table-list tbody")

# 遍历 tbody
for tbody in tbodys:
    rows = tbody.find_elements(By.TAG_NAME, "tr")
    for row in rows:
        # 找第二个 td，class="name"
        title_td = row.find_element(By.CSS_SELECTOR, "td.name")
        title_author = row.find_element(By.CSS_SELECTOR, "td.author")
        # 来源
        source_td = row.find_element(By.CSS_SELECTOR, "td.source")
        source_text = source_td.find_element(By.TAG_NAME, "p").text
        source_link = source_td.find_element(By.TAG_NAME, "a").get_attribute("href")

        title = title_td.text
        author = title_author.text
        output = f"标题:{title} 作者:{author} 来源:{source_text} 来源链接:{source_link}"
        print(output)








