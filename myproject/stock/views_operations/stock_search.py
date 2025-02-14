import os
import sys
import pandas as pd
import yfinance as yf
from ..models import StockInfo

# from Get_DBdata import Get_DBdata

"""
yahoofinanceAPIを使用し、
入力された銘柄コードに該当する株式情報を取得
"""

def stock_search(code):

    stock_code = f"{code}.T"

    stock = yf.Ticker(stock_code)
    # if stock == None:
    #     result = "該当の銘柄は見つかりませんでした。"
    # else:
    try:
        data = stock.history(period="1d")
        if data.empty:
            return {'message': "該当の銘柄は見つかりませんでした。"}
            

        price = round(data['Close'].iloc[0])
        stock_name = StockInfo.objects.filter(code=code).filter().first()
        

        result = {
            'code': code,
            'stock_name': stock_name,
            'stock_price': price,
        }
    except Exception as e:
        result = {
            'message': f"エラーが発生しました: {e}"
        }


    return result







