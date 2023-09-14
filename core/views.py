from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserProfileForm, UserPersonalProfileForm,PostUploadForm
from django.contrib.auth.models import User
from .models import ProfileUser,UserFollowing,PostModel



@login_required(login_url='signin')
def index(request):
    current_user = request.user
    current_profile = ProfileUser.objects.get(user=current_user)
    upload_form = PostUploadForm(request.POST or None,request.FILES)
    followed_people = UserFollowing.objects.filter(user_id=current_user).values('following_user_id')
    posts = PostModel.objects.filter(post_owner__in=followed_people)
        
    
    context = {
        'current_profile':current_profile,
        'upload_form':upload_form,
        'posts':posts,
        
    }

    if upload_form.is_valid():
        instance = upload_form.save(commit=False)
        instance.post_owner = current_user
        instance.save()
        messages.success(request,"Picture has uploaded!!!")
        return redirect('index')
        
    return render(request,'index.html',context)


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
            UserFollowing.objects.create(user_id=current_user,following_user_id=current_user)
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

@login_required(login_url='signin')
def profile(request, pk):
    current_user = User.objects.get(username=pk)
    post_number = current_user.poster.all().count()
    current_active_user = request.user
    current_profile = ProfileUser.objects.get(user=current_user)
    following_num = current_user.following.all().count()-1
    followers_num = current_user.followers.all().count()-1
    takip = current_user.following.filter(following_user_id=current_user).exists()
    post_content = current_user.poster.all()
    context = {
        'current_user':current_user,
        'following_num':following_num,
        'followers_num':followers_num,
        'current_profile':current_profile,
        'takip':takip,
        'post_number':post_number,
        'post_content':post_content
    }
    if request.method == 'POST':
        if takip:
           current_user.followers.get(following_user_id=current_user).delete()
           context['followers_num'] -=1
           context['takip'] = False
        else:
            UserFollowing.objects.create(user_id=current_active_user,following_user_id=current_user).save()
            context['followers_num'] +=1
            context['takip'] = True
        return render(request,'profile.html',context)
    return render(request,'profile.html',context)