from django.urls import path,include
from . import views
urlpatterns = [
    path('', views.index,name="index"),
    path('birinci_form/<int:seans_id>/', views.birinci_form, name='birinci_form'),
    path('seat-selection/<int:tam_bilet_sayisi>/<int:ogrenci_bilet_sayisi>/<int:seans_id>/<str:son_tarih>/', views.seat_selection, name='seat_selection'),
    path('ikinci_form/<int:tam_bilet_sayisi>/<int:ogrenci_bilet_sayisi>/<int:seans_id>/<str:son_tarih>/<str:selected_seat_positions>/', views.ikinci_form, name='ikinci_form'),
    path('bilet_olustur_sonuc/<int:seans_id>/<str:ad_soyad>/', views.bilet_olustur_sonuc, name='bilet_olustur_sonuc'),
    path('bilet_iade/<int:bilet_id>/', views.bilet_iade, name='bilet_iade'),
    path('hakkimizda/', views.hakkimizda, name='hakkimizda'),
    path('sinemalar/', views.sinemalar, name="sinemalar"),
    path('kampanya/', views.kampanya, name="kampanya"),
    path('biletlerim/', views.biletlerim, name='biletlerim'),
    path('<str:film_title>/comment/', views.comment_create, name='comment_create'),
    path('<str:film_title>/', views.film_detail, name='film_detail'),

]
