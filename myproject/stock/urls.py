from django.urls import path
from . import views
from .views import RecordView, RecordDetailView, RecordCreateView, RecordUpdateView, RecordDeleteView

app_name = "stock"
urlpatterns = [
    path("", views.index, name="index"),
    path("settings/", views.settings, name="settings"),
    path("record/", RecordView.as_view(), name="record"),
    path('record/<uuid:pk>/', RecordDetailView.as_view(), name='record_detail'),
    path('record/create/', RecordCreateView.as_view(), name="record_create"),
    path('record/<uuid:pk>/edit/', RecordUpdateView.as_view(), name="record_edit"),
    path('record/<uuid:pk>/delete/', RecordDeleteView.as_view(), name="record_delete"),
]
