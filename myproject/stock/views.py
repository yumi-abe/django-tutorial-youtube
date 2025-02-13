from django.shortcuts import render
from django.views import View
from .models import StockInfo, Calendar
from .views_operations.stock_search import stock_search
from .views_operations.get_stockInfo import GetStockInfo

class IndexView(View):
    def get(self, request):
        quantity_options = list(range(100, 1001, 100))
        month_options = list(range(1, 13))
        context = {
            'quantity_options': quantity_options,
            'month_options' : month_options,
            }
        return render(request, "stock/index.html", context)

    def post(self, request):
        code = request.POST.get('code')
        result = stock_search(code)

        context = {
            'result': result
        }
        return render(request, "stock/index.html", context)


class SettingsView(View):
    def get(self, request):
        stock_data = StockInfo.objects.all().order_by('-updated_at').first()
        calendar_data = Calendar.objects.all().order_by('-updated_at').first()
        context = {
            "stock_data": stock_data,
            "calendar_data": calendar_data,
        }
        return render(request, "stock/settings.html", context)

    def post(self, request):
        get_info = GetStockInfo()
        if 'get_stock_info' in request.POST:
            if get_info.get_stock_info():
                if get_info.insert_stock_info():
                    message = "書き込みに成功しました"
                else:
                    message = "書き込みに失敗しました。"
            else:
                message = "データを取得できませんでした。"

        if 'search' in request.POST:
            code = request.POST.get('code')
            result = StockInfo.objects.filter(code=code).first()
            if not result:
                result = {'message': '見つかりませんでした'}
        
        if 'calendar' in request.POST:
            get_info.get_calendar()
            message = 'カレンダーを更新しました。'
        
        stock_data = StockInfo.objects.all().order_by('-updated_at').first()
        calendar_data = Calendar.objects.all().order_by('-updated_at').first()
        context = {
            "stock_data": stock_data,
            "calendar_data": calendar_data,
        }
        if 'message' in locals():
            context['message'] = message
        if 'result' in locals():
            context['result'] = result
        return render(request, "stock/settings.html", context)
        
index = IndexView.as_view()
settings = SettingsView.as_view()