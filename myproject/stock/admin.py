from django.contrib import admin
from .models import StockInfo, Calendar

admin.site.register(StockInfo)
# admin.site.register(Calendar)
@admin.register(Calendar)
class PageAdmin(admin.ModelAdmin):
    readonly_fields = ["created_at", "updated_at"]