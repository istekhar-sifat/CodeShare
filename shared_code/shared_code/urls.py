from django.urls import path
from app import views
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_page, name='home_page'),
    path('create/', views.create_text, name='create_text'),
    path('get/', views.get_text, name='get_text'),
    path('text/<str:pin>/', views.text_detail, name='text_detail'),
]