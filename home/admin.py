from django.contrib import admin
from .models import *

# Register your models here.
# admin.site.register(Disease)
# admin.site.register(Medicine)
# admin.site.register(Pre_Details)
# admin.site.register(Health)

class PostPersonal(admin.ModelAdmin):
    list_display = ['id','ten', 'gioitinh', 'sdt']

admin.site.register(Personal, PostPersonal)

class PostDisease(admin.ModelAdmin):
    list_display = ['id','ten_benh']

admin.site.register(Disease, PostDisease)

class PostDisease_Vac(admin.ModelAdmin):
    list_display = ['id','ten_benh']

admin.site.register(Disease_Vac, PostDisease_Vac)

class PostMedicine(admin.ModelAdmin):
    list_display = ['id','ten_goc', 'ten_bd']

admin.site.register(Medicine, PostMedicine)

class PostHealth(admin.ModelAdmin):
    list_display = ['id','ma_canhan', 'ma_benh']

admin.site.register(Health, PostHealth)

class PostPre_Details(admin.ModelAdmin):
    list_display = ['id','ma_toa', 'ma_thuoc', 'lieuluong']

admin.site.register(Pre_Details, PostPre_Details)

class PostVaccination(admin.ModelAdmin):
    list_display = ['id','canhan','ten_vac', 'ngay_tiem', 'dia_chi']

admin.site.register(Vaccination, PostVaccination)
