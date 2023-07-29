from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.say_hello),
    path('barang/', views.barang, name='get_barang'),
    path('perusahaan/', views.perusahaan, name='get_perusahaan'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('barang/<str:id>/', views.barang_by_id, name='barang_by_id'),
    path('perusahaan/<str:id>/', views.perusahaan_by_id, name='perusahaan_by_id'),
]