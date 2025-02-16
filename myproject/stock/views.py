from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from datetime import datetime
from .models import StockInfo, Calendar, Record
from .forms import CalcForm, RecordForm
from .views_operations.stock_search import stock_search
from .views_operations.get_stockInfo import GetStockInfo
from .views_operations.CrossTradeCalculator import CrossTradeCaluculator
from .views_operations.functions import get_cross_day

class IndexView(View):
    def cross_day(self):
        """当月の権利日取得"""
        dt = datetime.now()
        month = dt.month
        cross_day = get_cross_day(month)
        return cross_day
    
    def closed_days(self):
        """休業日をデータベースから取得して配列化"""
        calendar = Calendar.objects.values_list('date', flat=True)
        closed_days = [dt.date() for dt in calendar]
        return closed_days
    
    def get(self, request):
        form = CalcForm()
        cross_day = self.cross_day()
        context = {
            'form': form,
            'cross_day': cross_day,
        }
        return render(request, "stock/index.html", context)

    def post(self, request):
        form = CalcForm()
        cross_day = self.cross_day()
        if 'search' in request.POST:
            """検索ボタン（銘柄名・株価表示）"""
            code = request.POST.get('code')
            result = stock_search(code)
            context = {
                'result': result,
                'form': form,
                'cross_day': cross_day,
            }
            return render(request, "stock/index.html", context)
        
        if 'calc' in request.POST:
            """計算ボタン（手数料計算）"""
            form = CalcForm(request.POST)
            if form.is_valid():
                quantity = form.cleaned_data['quantity']
                price = form.cleaned_data['price']
                date = form.cleaned_data['date']
                month = form.cleaned_data['get_month']
                closed_days = self.closed_days()
                crossTradeCaluculator = CrossTradeCaluculator(closed_days, price, quantity)
                fee = crossTradeCaluculator.calculate_cross_fee(month, date)
                context = {
                    'quantity': quantity,
                    'price': price,
                    'date': date,
                    'month': month,
                    'form': form,
                    'cross_day': cross_day,
                    'fee': fee
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


class RecordView(LoginRequiredMixin, ListView):
    model = Record
    template_name = 'stock/record.html'
    context_object_name = 'records'
    
class RecordDetailView(LoginRequiredMixin, DetailView):
    model = Record
    template_name = 'stock/record_detail.html'
    context_object_name = 'record'

class RecordCreateView(LoginRequiredMixin, CreateView):
    model = Record
    template_name = 'stock/record_form.html'
    form_class = RecordForm
    success_url = reverse_lazy('stock:record')

class RecordUpdateView(LoginRequiredMixin, UpdateView):
    model = Record
    template_name = 'stock/record_form.html'
    form_class = RecordForm
    success_url = reverse_lazy('stock:record')

class RecordDeleteView(LoginRequiredMixin, DeleteView):
    model = Record
    template_name = 'stock/record_confirm_delete.html'
    success_url = reverse_lazy('stock:record')

index = IndexView.as_view()
settings = SettingsView.as_view()