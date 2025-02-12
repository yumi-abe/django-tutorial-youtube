from django.shortcuts import render
from django.views import View
from .stock_search import stock_search

class IndexView(View):
    def get(self, request):
        quantity_options = list(range(100, 1001, 100))
        month_options = list(range(1, 13))
        context = {
            'quantity_options': quantity_options,
            'month_options' : month_options
            }
        return render(request, "stock/index.html", context)
        
        
        
    def post(self, request):
        code = request.POST.get('code')
        result = stock_search(code)
        context = {
            'result': result
        }
        return render(request, "stock/index.html", context)
    
index = IndexView.as_view()