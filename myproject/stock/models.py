from django.db import models

class StockInfo(models.Model):
    code = models.CharField(max_length=4)
    stock_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.stock_name
    
class Calendar(models.Model):
    date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.date.strftime('%Y-%m-%d')