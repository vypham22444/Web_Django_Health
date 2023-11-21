from django.db import models
from django.contrib.auth.models import User

# Create your models here.

SHIRT_SIZES = [
        ("0", "admin"),
        ("1", "Ông"),
        ("2", "Bà"),
        ("3", "Cha"),
        ("4", "Mẹ"),
        ("5", "Anh"),
        ("6", "Chị"),
        ("7", "Em"),
        ("8", "Cô"),
        ("9", "Dì"),
        ("10", "Chú"),
        ("11", "Bác"),
    ]
# thong tin nguoi dung
class Personal(models.Model):
    ten = models.CharField(max_length=50, null=True)
    namsinh = models.DateField()
    gioitinh = models.CharField(max_length=10)
    sdt = models.CharField(max_length=15)
    email = models.EmailField(max_length=50, null=True)
    thebh = models.CharField(max_length=50)
    anh = models.ImageField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    # gioitinh = models.CharField(blank=True, choices=gt_type.choices, max_length=10)
    qhe = models.CharField(max_length=2, choices=SHIRT_SIZES)

    def __str__(self):
        return self.ten
    @property
    def ImageURL(self):
        try:
            url = self.anh.url
        except:
            url = ''
        return url


# benh
class Disease(models.Model):
    # ma_benh = models.CharField(max_length=20)
    ten_benh = models.CharField(max_length=30)

    def __str__(self):
        return self.ten_benh


# thuoc
class Medicine(models.Model):
    ten_goc = models.CharField(max_length=30, null=False)
    ten_bd = models.CharField(max_length=30)
    gia = models.FloatField()

    # def __init__(self, ten_goc, ten_bd):
    #     self.ten_goc = ten_goc
    #     self.ten_bd = ten_bd
    def __str__(self):
        return f"{self.ten_goc} ({self.ten_bd}) "

# toa thuoc
# class Prescription(models.Model):
#     ten_bs = models.CharField(max_length=50)
#     anh = models.ImageField(null=True, blank=True)
#     ngay = models.DateField()

#     def __str__(self):
#         return str(self.id)

# thong tin suc khoe, toa thuoc
class Health(models.Model):
    ma_canhan = models.ForeignKey(Personal, on_delete=models.SET_NULL, null=True, blank=False)
    ma_benh = models.ForeignKey(Disease,on_delete=models.SET_NULL, null=True, blank=False)
    # ma_toa = models.ForeignKey(Prescription, on_delete=models.SET_NULL, null=True, blank=False)
    ngay = models.DateField()
    diachi = models.TextField(max_length=50)
    tenbs = models.CharField(null=True, max_length=30)
    anh = models.ImageField(null=True, blank=True)

    def __str__(self):
        return str(self.id)
    
# chi tiet toa thuoc
class Pre_Details(models.Model):
    ma_toa = models.ForeignKey(Health, on_delete=models.SET_NULL, null=True, blank=False)
    ma_thuoc = models.ForeignKey(Medicine, on_delete=models.SET_NULL, null=True, blank=False)
    lieuluong = models.IntegerField()

    def __str__(self):
        return str(self.id)
    
class Disease_Vac(models.Model):
    # ma_benh = models.CharField(max_length=20)
    ten_benh = models.CharField(max_length=30)

    def __str__(self):
        return self.ten_benh
    
class Vaccination(models.Model):
    canhan = models.ForeignKey(Personal, on_delete=models.SET_NULL, null=True, blank=False)
    ten_vac = models.CharField(max_length=100)
    ten_benh = models.ForeignKey(Disease_Vac, on_delete=models.SET_NULL, null=True, blank=False)
    phan_ung = models.CharField(max_length=100)
    ngay_tiem = models.DateField()
    ngay_hen = models.DateField(null=True, blank=False)
    dia_chi = models.TextField(max_length=200)
    
    def __str__(self):
        return str(self.id)


