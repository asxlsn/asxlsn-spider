import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import os


def scrape_cnki(keyword, chrome_path, driver_path, excel_file=None):
    """
    知网论文抓取函数

    :param keyword: 搜索关键词
    :param chrome_path: Chrome 浏览器路径
    :param driver_path: ChromeDriver 路径
    :param excel_file: 保存的 Excel 文件路径，如果为 None 默认 cnki_<keyword>.xlsx
    """
    # ---------- 配置日志 ----------
    log_file = "cnki_scrapy.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_file, mode='w', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

    if excel_file is None:
        excel_file = f"cnki_{keyword}.xlsx"
    if os.path.exists(excel_file):
        os.remove(excel_file)

    # ---------- 配置浏览器 ----------
    options = Options()
    options.binary_location = chrome_path
    options.add_argument("--headless")  # 无界面
    options.add_argument("--disable-gpu")
    options.add_argument("--start-maximized")

    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    # ---------- 打开知网 ----------
    driver.get("https://www.cnki.net/")
    time.sleep(2)

    # ---------- 搜索关键词 ----------
    search_box = driver.find_element(By.CLASS_NAME, "search-input")
    search_box.send_keys(keyword)
    search_button = driver.find_element(By.CLASS_NAME, "search-btn")
    search_button.click()
    time.sleep(3)

    all_data = []
    page_num = 1

    logging.info(f"开始抓取知网论文，关键词：{keyword}")

    while True:
        try:
            logging.info(f"=== 开始抓取第 {page_num} 页 ===")

            # 等待表格 tbody 出现
            tbody = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table.result-table-list tbody"))
            )

            # 遍历每行 tr
            rows = tbody.find_elements(By.TAG_NAME, "tr")
            page_data = []

            for idx, row in enumerate(rows, start=1):
                title_td = row.find_element(By.CSS_SELECTOR, "td.name")
                author_td = row.find_element(By.CSS_SELECTOR, "td.author")
                source_td = row.find_element(By.CSS_SELECTOR, "td.source")

                title = title_td.text
                author = author_td.text
                source_text = source_td.find_element(By.TAG_NAME, "p").text
                links = source_td.find_elements(By.TAG_NAME, "a")
                source_link = links[0].get_attribute("href") if links else ""

                page_data.append({
                    "标题": title,
                    "作者": author,
                    "来源文字": source_text,
                    "来源链接": source_link
                })

                logging.info(
                    f"抓取第 {page_num} 页，第 {idx} 条：标题={title}, 作者={author}, 来源={source_text}, 链接={source_link}")

            # 追加到总数据
            all_data.extend(page_data)

            # 每页抓完就写入 Excel
            df = pd.DataFrame(all_data)
            df.to_excel(excel_file, index=False)
            logging.info(f"第 {page_num} 页抓取完成，已写入 Excel，总共 {len(all_data)} 条数据")

            # ---------- 翻页 ----------
            try:
                pages_div = driver.find_element(By.CLASS_NAME, "pages")
                next_page = pages_div.find_element(By.XPATH, './/a[@class="pagesnums" and text()="下一页"]')
                if "disabled" in next_page.get_attribute("class"):
                    logging.info("已到最后一页")
                    break
                next_page.click()
                page_num += 1
                time.sleep(3)
            except:
                logging.info("没有下一页，抓取结束")
                break

        except Exception as e:
            logging.error(f"抓取第 {page_num} 页出错: {e}", exc_info=True)
            break

    driver.quit()
    logging.info(f"抓取完成，所有数据已保存到 Excel: {excel_file}")


# ---------- 调用示例 ----------
if __name__ == "__main__":
    scrape_cnki(
        keyword="人工智能",
        chrome_path=r"F:\Google\Chrome\Application\chrome.exe",
        driver_path=r"E:\Code\130.0.6723.58 chromedriver-win64\chromedriver-win64\chromedriver.exe"
    )
