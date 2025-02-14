import os
import pandas as pd
import requests

from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from typing import Optional
from ..models import StockInfo, Calendar



class GetStockInfo:
    def __init__(self):
        self.save_dir = "./stock/views_operations/files"
        self.file_path = os.path.join(self.save_dir, "stock_name.xls")

    def _setup_diver(self):
        """WebDriverのセットアップ"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=chrome_options)

    def get_stock_info(self):
        url = "https://www.jpx.co.jp/markets/statistics-equities/misc/tvdivq0000001vg2-att/data_j.xls"
        r = requests.get(url)

        os.makedirs(self.save_dir, exist_ok=True)
        
        if r.status_code == 200:
        # ファイルをダウンロード
            with open(self.file_path, 'wb') as f:
                f.write(r.content)
            return True
        else:
            return False
    
    def insert_stock_info(self):
        df = pd.read_excel(self.file_path, engine='xlrd')
        for index, row in df.iterrows():
            StockInfo.objects.update_or_create(
                code = row['コード'],
                defaults={'stock_name': row['銘柄名']}
            )
        return True

    def get_calendar(self):
        """JPXカレンダー情報を取得する"""
        # スクレイピング
        self._setup_diver()
        self.driver.get("https://www.jpx.co.jp/corporate/about-jpx/calendar/index.html")
        self.driver.implicitly_wait(5)

        # 休業日部分を取得してカレンダー配列に格納
        elements = self.driver.find_elements(By.XPATH, "//tr/td[1]")
        for element in elements:
            date = element.text.split('（')[0] #（曜日）を切り離す
            date = datetime.strptime(date, '%Y/%m/%d') #datetime型へ
            date = date.date()
            
            Calendar.objects.update_or_create(
                date=date,
                defaults={'updated_at': datetime.now()}
            )
        
        self.driver.quit()
