from telnetlib import LOGOUT
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import *
from django.contrib.auth.models import User, auth
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.db.models import Q
from django.views.generic import TemplateView, ListView

from django.core.mail import send_mail
from django.conf import settings
import datetime

# Create your views here.
def register(request):
    if request.method == 'POST':
        # first_name = request.POST['first_name']
        # last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password==confirm_password:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Tên người này đã được sử dụng')
                return redirect(register)
            # elif User.objects.filter(email=email).exists():
            #     messages.info(request, 'Email này đã được sử dụng')
            #     return redirect(register)
            else:
                user = User.objects.create_user(username=username,email=email, password=password
                                         )
                user.save()
                
                return redirect('login')


        else:
            messages.info(request, 'Cả hai mật khẩu đều không khớp')
            return redirect(register)
            

    else:
        return render(request, 'register.html')
    
def login_user(request):
    # if request.user.is_authenticated:
    #     return redirect('home')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Tên hoặc mật khẩu không đúng')
            return redirect('login')

    else:
        return render(request, 'login.html')
# chưa sd  
def change_mk(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, _('Your password was successfully updated!'))
            return redirect('accounts:change_password')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_mk.html', {
        'form': form
    })

def logout_user(request):
    logout(request)
    return redirect('home')

def home(request):
    if request.user.is_authenticated:
        personals = Personal.objects.filter(user=request.user.id).order_by('-namsinh')
        
        context = {'personals':personals}
    
        return render(request, 'home.html', context)
    else:
        return redirect('login')


def tk(request):
    if request.user.is_authenticated:
        
        if request.method == "POST":
            personals = Personal.objects.filter(user=request.user.id).order_by('-namsinh')
            tk_ed = request.POST["tk_ed"]
            tieude=request.POST.get('tieude')
            if tieude=='1':
                benh=Disease.objects.filter(ten_benh__icontains = tk_ed)
                for k in benh:
                    # health=Health.objects.get(ma_benh=k, ma_canhan=personals)
                
                    health = Health.objects.filter(ma_canhan__id__in=personals, ma_benh=k)
                    # key.append({'ma_canhan': h.ma_canhan})
                    t='Bệnh'
                    return render(request, 'tk.html',{"tk_ed":tk_ed, "health":health, 'tieude':t})
            
            elif tieude=='3':
                t='Tên Cá nhân'
                ten=Personal.objects.filter(ten__icontains = tk_ed, user=request.user.id)
                health=Health.objects.filter(ma_canhan__in=ten.all())
                return render(request, 'tk.html',{"tk_ed":tk_ed, "health":health, 'tieude':t})
            
            elif tieude=='2':
                t='Thuốc'
                thuoc=Medicine.objects.filter(ten_goc__icontains = tk_ed)
                pre=Pre_Details.objects.filter(ma_thuoc__in=thuoc).values('ma_toa')
                # pre=Pre_Details.objects.filter(ma___in__ma_toa=thuoc)
                health = Health.objects.filter(id__in=pre.all())
            
                return render(request, 'tk.html',{"tk_ed":tk_ed, "health":health, "tieude":t})
        
            elif tieude=='4':
                # ten=Personal.objects.filter(user=request.user.id).values('ten')
                vac=Vaccination.objects.filter(ten_vac__icontains = tk_ed).values('canhan')
                for i in vac:
                    t='Tên Vắc xin'
                    # đang lỗi
                    ten1=Personal.objects.filter(user=request.user.id, ten=i).values('ten')
                    health=Health.objects.filter(ma_canhan__in=vac.all())
                    return render(request, 'tk.html',{"tk_ed":tk_ed, "health":health, 'tieude':t})
                  
            else:
                return redirect(home) 
        else:
            return redirect(home)  
    else:
        return redirect('login')   

    # return render(request, 'tk.html',{"tk_ed":tk_ed, "health":health})

    # if request.method == "POST":
    #     tk_ed = request.POST["tk_ed"]
    #     keys = Disease.objects.filter(ten_benh__icontains = tk_ed)
        
    #     health = []
    #     for k in keys:
    #         health=Health.objects.filter(ma_benh=k)
    #         # key.append({'ma_canhan': h.ma_canhan})

    # return render(request, 'tk.html',{"tk_ed":tk_ed, "health":health})


def add_tn(request):
    # form = PesonalForm()
    # if request.method == "POST":
    #     form = PesonalForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         form.save()
    #         return HttpResponseRedirect('/')
    # # anh = Personal.objects.all()
    # return render(request, 'add_tn.html', context={'form':form})
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PesonalForm(request.POST or None, request.FILES)

            if form.is_valid():
                data = form.save()
                data.user = request.user
                data.save()
                return redirect(home)
            
        else:
            form = PesonalForm()
        return render(request,'add_tn.html', {'form':form})
    return redirect(login_user)
  
def edit_tn(request,id):
    if request.user.is_authenticated:
        produ = Personal.objects.get(id=id)
        if request.method == 'POST':
            form = PesonalForm(request.POST or None, request.FILES, instance=produ)
    
            if form.is_valid():
                data = form.save()
                data.user = request.user
                data.save()
                # img_obj = form.instance
                # return render(request, 'add_tn.html', {'form': form, 'img_obj': img_obj})
                return redirect(home)
        else:
            form = PesonalForm(instance=produ)
            return render(request,'add_tn.html',{"form":form})
    return redirect(login_user)

def delete_tn(request,id):
	if request.user.is_authenticated:
            produ = Personal.objects.get(id=id)
            produ.delete()
            return redirect(home)


def health(request,id):
    # if request.user.is_authenticated:
    #     personal = request.user.personal
    #     health, created = Health.objects.get_or_create(personal = personal, complex= False)
    # else:
    # if request.user.is_authenticated:
        # id = request.GET.get(id=id)
        healths = Health.objects.filter(ma_canhan=id)

        context = {'healths': healths, 'id':id}
        return render(request, 'health.html', context)

def detail_health(request,id):
    if request.user.is_authenticated:
        # idd = request.GET.get('id','')
        healths = Health.objects.filter(id=id)
        pre_details= Pre_Details.objects.filter(ma_toa=id)
        he = Health.objects.get(id=id)

        if request.method == 'POST':
            me = MedicineForm(request.POST or None)
            if me.is_valid():
                mee = me.save()
                mee.ma_toa=he
                mee.save()
                return redirect(detail_health,id)
        else:
            me = MedicineForm()

        context = {'healths': healths, 'pre_details': pre_details, 'me':me}
        return render(request, 'detail_health.html', context)


def add_health(request,id):
    if request.user.is_authenticated:
        per = Personal.objects.get(id=id)
        # pre = Pre_Details.objects.get(ma_toa=per.id)
        if request.method == 'POST':
            form = HealthForm(request.POST or None)
    
            if form.is_valid():
                data = form.save()
                data.ma_canhan = per
                data.save()
                return redirect(health,id)
        else:
            form = HealthForm()
        return render(request, 'add_health.html', {'form' : form})


def edit_health(request,id_per,id_health):
    if request.user.is_authenticated:
        per = Personal.objects.get(id=id_per)
        hea = Health.objects.get(ma_canhan=per, id = id_health)
        if request.method == 'POST':
            form = HealthForm(request.POST or None, request.FILES, instance=hea)

            if form.is_valid():
                data = form.save()
                data.ma_canhan = per
                data.save()
                return redirect(health,id_per)
        else:
            form = HealthForm(instance=hea)
        return render(request, 'add_health.html', {'form' : form})
    else:
        return redirect(login_user)
  

def delete_health(request,id_per,id_health):
    if request.user.is_authenticated:
        per = Personal.objects.get(id=id_per)
        hea = Health.objects.get(ma_canhan=per, id = id_health)
        hea.delete()
        return redirect(health,id_per)
    else:
        return redirect(login_user)
    
# def add_thuoc(request):
#     if request.user.is_authenticated:
#         if request.method == 'POST':
#             form = PreForm(request.POST or None)
    
#             if form.is_valid():
#                 form.save()
#                 return redirect(add_thuoc)
#         else:
#             form = PreForm()
#         return render(request,'add_thuoc.html',{"form":form})
#     return redirect(login_user)

def add_benh(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            tenbenh = request.POST["tenbenh"]
            ten_benh = Disease.objects.create(ten_benh=tenbenh)
            ten_benh.save()
            return redirect(add_benh)
        benh = Disease.objects.all()
        return render(request, 'add_benh.html',{'benh':benh})
    return redirect(login_user)

def add_benhtiem(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            tenbenh = request.POST["tenbenh"]
            ten_benh = Disease_Vac.objects.create(ten_benh=tenbenh)
            ten_benh.save()
            return redirect(add_benhtiem)
        benh = Disease_Vac.objects.all()
        return render(request, 'add_benhtiem.html',{'benh':benh})
    return redirect(login_user)

def add_vacxin(request):
    
    return redirect(home)



def tiem(request):
    if request.user.is_authenticated:
        personals = Personal.objects.filter(user=request.user.id).order_by('-namsinh')
        
        vac = Vaccination.objects.filter(canhan__id__in=personals.all())

        currentdate = datetime.date.today()
        
        for i in vac:
            v=i.ngay_hen
            tr = (v-currentdate).days
            print(tr)
            
            # t=i.canhan
            # for j in ten1:
            if tr == 2  :
                per = Personal.objects.get(user=request.user.id, ten=i.canhan)
                # ten1 = Vaccination.objects.get(canhan=per)
                p=per.email
                text = 'Xin chào ' + per.ten + ', ' + i.ngay_hen.strftime('%d-%m-%Y') +' là ngày hẹn tiêm phòng bệnh '+ i.ten_benh.ten_benh +'. Mời bạn đến: ' + i.dia_chi+' để tiêm mũi tiếp theo. Cảm ơn đã đọc email'
                send_mail(
                    'LỊCH HẸN TIÊM PHÒNG',
                    text,
                    'settings.EMAIL_HOST_USER',
                    [p],
                    fail_silently=True)
        return render(request, 'tiem.html', {'vac':vac, 'personals':personals})
        
    else:
        return redirect(login_user)

def add_tiem(request):
    if request.user.is_authenticated:
        per = Personal.objects.filter(user=request.user.id)
        vac = Vaccination.objects.filter(canhan__id__in=per.all())
        
        # vac = Vaccination.objects.get(canhan=per.id)
        
        if request.method == 'POST':
            form = VaccinationForm(request.POST or None)
            ten1=request.POST.get('ten')
            per=Personal.objects.get(user=request.user.id,ten=ten1)
            if form.is_valid():
                data = form.save()
                data.canhan = per
                data.save()
                return redirect(tiem)
        else:
            form = VaccinationForm()
        return render(request, 'add_tiem.html', {'form' : form, 'personals':per})
    return redirect(login_user)

def edit_tiem(request,id):
    if request.user.is_authenticated:
        per = Personal.objects.filter(user=request.user.id)
        vac = Vaccination.objects.get(id=id)
        # vac = Vaccination.objects.get(canhan=per.id)
        if request.method == 'POST':
            form = VaccinationForm(request.POST or None, instance=vac)
            if form.is_valid():
                data = form.save()
                data.save()
                return redirect(tiem)
        else:
            form = VaccinationForm(instance=vac)
        return render(request, 'add_tiem.html', {'form' : form, 'personals':per})
    return redirect(login_user)

def delete_tiem(request,id):
	if request.user.is_authenticated:
            produ = Vaccination.objects.get(id=id)
            produ.delete()
            return redirect(tiem)

def tk_benh(request):
        if request.user.is_authenticated:
            if request.method == "POST":
                ngaybd = request.POST['ngaybd']
                ngaykt = request.POST['ngaykt']
            
                health = Health.objects.filter(ngay__range=[ngaybd, ngaykt])
                b=datetime.datetime.strptime(ngaybd,'%Y-%m-%d')
                bd=b.strftime("%d-%m-%Y")
                k=datetime.datetime.strptime(ngaykt,'%Y-%m-%d')
                kt=k.strftime("%d-%m-%Y")
                return render(request, 'tk_benh.html', {'health':health, 'ngaybd':bd, 'ngaykt':kt})
            return render(request, "tk_benh.html")
        else:
            return redirect(login_user)
        
import datetime
def tk_tiem(request):
        if request.user.is_authenticated:
            if request.method == "POST":
                ngaybd = request.POST['ngaybd']
                ngaykt = request.POST['ngaykt']
            
                vac = Vaccination.objects.filter(ngay_hen__range=[ngaybd, ngaykt])
                print(ngaybd)
                b=datetime.datetime.strptime(ngaybd,'%Y-%m-%d')
                bd=b.strftime("%d-%m-%Y")
                print(bd)
                k=datetime.datetime.strptime(ngaykt,'%Y-%m-%d')
                kt=k.strftime("%d-%m-%Y")
                print(kt)
                return render(request, 'tk_tiem.html', {'vac':vac, 'ngaybd':bd, 'ngaykt':kt})
            return render(request, "tk_tiem.html")
        else:
            return redirect(login_user)
	

def index(request):
    if request.method == 'POST':
        ten = request.POST['ten']
        email = request.POST['email']
        text = request.POST['text']
        sdt = request.POST['sdt']
        nd = request.POST['nd']
        send_mail(
            'Contact',
            text,
            'settings.EMAIL_HOST_USER',
            [email],
            fail_silently=False
        )
        
    return render(request, 'index.html')

# import os
# from twilio.rest import Client


# # Find your Account SID and Auth Token at twilio.com/console
# # and set the environment variables. See http://twil.io/secure
# account_sid = "ACef3bd73569621774a5f70b07cfcfab0f"
# auth_token = "fe252810b5e163ff4a60ee88471535e9"
# client = Client(account_sid, auth_token)

# message = client.messages \
#                 .create(
#                      body="Join Earth's mightiest heroes. Like Kevin Bacon.",
#                      from_='+13344328644',
#                      to='+84796842836'
#                  )

# print(message.sid)

def uploadok(request):
    return HttpResponse(' upload successful')

# available_slots = []
#     for slots in TIME_SLOTS:
#         if slots[0] not in booked_slots:
#             available_slots.append(slots)

# send_sms('Here is the message','+84796842836',['+84788075127'], fail_silently=False)