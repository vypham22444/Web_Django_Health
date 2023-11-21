from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home, name="home"),
    path('index/', views.index, name="index"),
    
    path('tiem/', views.tiem, name="tiem"),
    path('add_tiem/', views.add_tiem, name="add_tiem"),
    path('edit_tiem/<int:id>/', views.edit_tiem, name="edit_tiem"),
    path('delete_tiem/<int:id>/', views.delete_tiem, name="delete_tiem"),
    
    path('add_benh/', views.add_benh, name="add_benh"),
    path('add_benhtiem/', views.add_benhtiem, name="add_benhtiem"),
    path('add_vacxin/', views.add_vacxin, name="add_vacxin"),

    path('tk/', views.tk, name="tk"),
    path('register/', views.register, name="register"),
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),
    # path('change_mk/', views.change_mk, name="change_mk"),

    path('add_tn/', views.add_tn, name="add_tn"),
    path('edit_tn/<int:id>/', views.edit_tn, name="edit_tn"),
    path('delete_tn/<int:id>/', views.delete_tn, name="delete_tn"),

    path('health/<int:id>/', views.health, name="health"),
    path('add_health/<int:id>/', views.add_health, name="add_health"), 
    path('edit_health/<int:id_per>/<int:id_health>/', views.edit_health, name="edit_health"),
    path('delete_health/<int:id_per>/<int:id_health>/', views.delete_health, name="delete_health"),

    path('detail_health/<int:id>/', views.detail_health, name="detail_health"),

    path('tk_benh/', views.tk_benh, name="tk_benh"),
    path('tk_tiem/', views.tk_tiem, name="tk_tiem"),

    # path('add_thuoc/', views.add_thuoc, name="add_thuoc"),
] 