from django.contrib import admin
from .models import StockInfo, Calendar, Record

admin.site.register(StockInfo)

@admin.register(Calendar)
class PageAdmin(admin.ModelAdmin):
    readonly_fields = ["created_at", "updated_at"]

@admin.register(Record)
class PageAdmin(admin.ModelAdmin):
    readonly_fields = ["id", "created_at", "updated_at"]