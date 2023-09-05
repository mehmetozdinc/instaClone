from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserProfileForm
from django.contrib.auth.models import User



@login_required(login_url='signin')
def index(request):
    return render(request,'index.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            messages.error(request,'Invalid Credentials!')
            return render(request,'signin.html')
    else:
        return render(request,'signin.html')


@login_required(login_url='signin')
def signout(request):
    logout(request)
    return redirect('signin')

def signup(request):
    if request.method == 'POST':
       
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # email = form.cleaned_data['email']
            # if User.objects.filter(email=email).exists():
            #     messages.error(request,"email kayıtlı!!!")
            #     return render(request,'signup.html',{'form':form})
            # else:
            form.save()
            messages.success(request,"Kayıt Başarılı! Lütfen Giriş Yapınız!!!")
            return redirect('signin')
        else:
            return render(request,'signup.html',{'form':form})
    else:
        form = UserRegisterForm()
        return render(request,'signup.html',{'form':form})


def setting(request):
    form = UserProfileForm()
    

    return render(request, 'setting.html',{'form':form})
