from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta
from typing import Union, Dict
from .BusinessDayCalculator import BusinessDayCalculator
from ..models import Calendar

# strからdate型に変換する
def strToDate(date_input:Union[str, date]) -> date:
    if isinstance(date_input, str):
        toDate = datetime.strptime(date_input, "%Y/%m/%d").date()
    else:
        toDate = date_input
    return toDate

# strを入れたらdateに変換しつつ、日数差を計算する
def diff_days(start:Union[str, date], end:Union[str, date]) -> int:
    start = strToDate(start)
    end = strToDate(end)
    delta = end - start
    return delta.days

def get_cross_day(month:int) -> Dict[str, date]:
        """
        クロス取引の日付を計算する
        :param month:対象月
        :return: クロス取引の各日付{権利確定日、権利付き最終日、権利落ち日}(dict形式)
        """
        calendar = Calendar.objects.values_list('date', flat=True)
        closed_days = [dt.date() for dt in calendar]
        businessDayCalculator = BusinessDayCalculator(closed_days)
        cross_day = {}
        cross_day["month"] = month
        # 権利確定日(決算月の月末営業日)
        confirmed_date = businessDayCalculator.last_business_day(month)
        cross_day["confirmed_date"] = confirmed_date

        # 権利付き最終日（権利確定日の2営業日前）
        get_date = businessDayCalculator.subtract_business_days(confirmed_date)
        cross_day["get_date"] = get_date

        # 権利落ち日（権利月最終日の1営業日後）
        ex_date = businessDayCalculator.add_business_days(get_date, 1)
        cross_day["ex_date"] = ex_date

        #現渡受け渡し日(権利落ち日の2営業日後)
        transaction_date = businessDayCalculator.add_business_days(ex_date)
        cross_day["transaction_date"] = transaction_date


        return cross_day
    