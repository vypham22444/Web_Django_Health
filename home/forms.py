from typing import Any, Dict, Mapping, Optional, Type, Union
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import *
import re
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


class PesonalForm(forms.ModelForm):

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
        
        # self.fields["qhe"].widget.attrs.update({
        #     'required':'',
        #     'name': 'qhe',
        #     'type': 'text',
        #     'class': 'form-control',
        #     'placeholder': 'Nam, Nữ'
        # })
  
    class Meta:
        model = Personal
        fields = ('ten', 'namsinh','gioitinh', 'sdt','email' ,'thebh', 'anh', 'qhe')

        widgets = {
            'ten' : forms.TextInput(attrs={'class':'form-control', 'placeholder':''}),
            'gioitinh' : forms.TextInput(attrs={'class':'form-control','placeholder':'Nam, Nữ' }),
            'namsinh' : forms.DateInput(
                attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)', 'class': 'form-control'}
            ),
            'sdt' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'0912345678'}),
            'email' : forms.EmailInput(attrs={'class':'form-control', 'placeholder':'...@gmail.com'}),
            'thebh' : forms.TextInput(attrs={'class':'form-control'}),
            'anh' : forms.FileInput(),
            'qhe' : forms.Select(attrs={'class':'form-select'}),
        }

class HealthForm(forms.ModelForm):
  
    class Meta:
        model = Health
        fields = ('ma_benh','ngay','diachi','tenbs','anh')

        widgets ={
            'ma_benh' : forms.Select(attrs={'class':'form-select'}),
            'ngay' : forms.DateInput(
                attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)', 'class': 'form-control'}
            ),
            'diachi' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Bệnh viện...'}),
            'tenbs' : forms.TextInput(attrs={'class':'form-control'}),
            'anh' : forms.FileInput(),
        }


class MedicineForm(forms.ModelForm):
  
    class Meta:
        model = Pre_Details
        fields =('ma_thuoc','lieuluong')

class VaccinationForm(forms.ModelForm):
  
    class Meta:
        model = Vaccination
        fields = ('ten_vac', 'ten_benh', 'ngay_tiem','ngay_hen','phan_ung','dia_chi')

        widgets = {
            'ten_vac' : forms.TextInput(attrs={'class':'form-control'}),
            'ten_benh' : forms.Select(attrs={'class':'form-select'}),
            'ngay_tiem' : forms.DateInput(
                attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)', 'class': 'form-control'}
            ),
            'ngay_hen' : forms.DateInput(
                attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)', 'class': 'form-control'}
            ),
            'phan_ung' : forms.TextInput(attrs={'class':'form-control'}),
            'dia_chi' : forms.TextInput(attrs={'class':'form-control'}),
        }

class DiseaseForm(forms.ModelForm):

    class Meta:
        model = Disease
        fields = '__all__'

# class PesonalForm(forms.Form):
#     ten = forms.CharField(label='tên')
#     sdt = forms.CharField(label='Số điện thoại')
#     namsinh = forms.DateField(label='năm sinh')
#     thebh = forms.CharField(label='Thẻ bảo hiểm')
#     gioitinh = forms.CharField(label='Giới tính')
#     anh = forms.ImageField(label ='Ảnh cá nhân', required=False)

#     def save(self):
#         Personal.objects.create(ten=self.cleaned_data['ten'], namsinh=self.cleaned_data['namsinh'],gioitinh=self.cleaned_data['gioitinh'],sdt=self.cleaned_data['sdt'], thebh=self.cleaned_data['thebh'], anh=self.cleaned_data['anh'])
    

# class HealthForm(forms.Form):
#     ngay = forms.CharField(label='Ngày Khám')
#     diachi = forms.CharField(label='Địa chỉ')
#     namsinh = forms.DateField(label='năm sinh')
#     thebh = forms.CharField(label='Thẻ bảo hiểm')
#     gioitinh = forms.CharField(label='Giới tính')
#     # anh = forms.ImageField(label ='Ảnh cá nhân', required=False)

#     def save(self):
#         Personal.objects.create(ten=self.cleaned_data['ten'], namsinh=self.cleaned_data['namsinh'],gioitinh=self.cleaned_data['gioitinh'],sdt=self.cleaned_data['sdt'], thebh=self.cleaned_data['thebh'])
    
	# class Meta:
	# 	model = Personal
	# 	fields = ("ten","namsinh", "gioitinh", "sdt", "thebh")
# class ProductForm(forms.ModelForm):
# 	class Meta:
# 		model = Product
# 		fields = ('name','typ','size','cost','description','release_date','image','averagerating')

# class ReviewForm(forms.ModelForm):
# 	class Meta:
# 		model = Review
# 		fields = ("comment","rating")
