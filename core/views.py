from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserProfileForm, UserPersonalProfileForm
from django.contrib.auth.models import User
from .models import ProfileUser



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
            current_user = User.objects.get(email=form.cleaned_data['email'])
            ProfileUser.objects.create(user=current_user,id_user=current_user.id)
            messages.success(request,"Kayıt Başarılı! Lütfen Giriş Yapınız!!!")
            return redirect('signin')
        else:
            return render(request,'signup.html',{'form':form})
    else:
        form = UserRegisterForm()
        return render(request,'signup.html',{'form':form})
    

@login_required(login_url='signin')
def setting(request, pk):
    if request.user.id == pk:
        current_record1 = User.objects.get(id=pk)
        current_record2 = ProfileUser.objects.get(user=current_record1)
        form1 = UserProfileForm(request.POST or None, instance=current_record2)
        form2 = UserPersonalProfileForm(request.POST or None, instance=current_record1)
        if form1.is_valid() and form2.is_valid():
            form1.save() 
            form2.save()
            if request.FILES.get('image') != None:
                image_record =ProfileUser.objects.get(user=current_record1)
                image = request.FILES.get('image')
                image_record.profileimg = image
                image_record.save()
            messages.success(request,"Kayıt Başarılı!")
            return redirect('index')
        
        return render(request, 'setting.html',{
            'form1':form1, 
            'form2':form2,
            'current_record2':current_record2})
    else:
        return render(request, 'error.html')

