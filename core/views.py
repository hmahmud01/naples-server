from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required

from core.models import Document, TopStory, AppUser, Faq

def home(request):
    documents = Document.objects.all()    
    faq = Faq.objects.all()
    return render(request, 'index.html', {'data' : documents, 'faq': faq})


def faq(request):
    data = ""
    return render(request, 'faq.html', {'data': data})


def about(request):
    data = ""
    return render(request, 'about.html', {'data': data})


def article(request, aid):
    article = Document.objects.get(id=aid)
    return render(request, 'article.html', {'data': article})


def changePassword(request):
    data = ""
    return render(request, 'changePassword.html', {'data': data})


def passwordchange(request):
    post_data = request.POST
    user = User.objects.get(id=request.user.id)
    if post_data['password'] == post_data['conf_pass']:
        user.password = post_data['password']
        user.set_password(post_data['password'])
        user.save()
        return redirect("/")
    else :
        return redirect('profile')
    

def contact(request):
    data = ""
    return render(request, 'contact.html', {'data': data})


@login_required(login_url='/login/')
def dashboard(request):
    documents = Document.objects.all()
    faq = Faq.objects.all()
    return render(request, 'dashboard.html', {'data': documents, 'faq': faq})


@login_required(login_url='/login/')
def userlist(request):
    users = AppUser.objects.all()
    return render(request, 'userlist.html', {'data': users})


def deleteuser(request, uid):
    appuser = AppUser.objects.get(id=uid)
    user = User.objects.get(id=appuser.user_id)
    appuser.delete()
    user.delete()
    return redirect('userlist')

@login_required(login_url='/login/')
def documentAdd(request):
    data = ""
    return render(request, 'documentAdd.html', {'data': data})


@login_required(login_url='/login/')
def savedocument(request):
    print(request)
    print("POST DATA")
    print(request.POST)
    print("FILES DATA")
    print(request.FILES)    

    post_data = request.POST
    
    request.FILES.get('filepath')
    # doc = request.FILES['docs']
    # thumbnail = request.FILES['thumb']

    doc = request.FILES.get('docs')
    thumbnail = request.FILES.get('thumb')

    if doc and thumbnail:
        document = Document(
            title = post_data['title'],
            summary = post_data['summary'],
            description = post_data['description'],
            category = post_data['category'],
            doctype = post_data['type'],
            author = post_data['author'], 
            document = request.FILES['docs'],
            thumbnail = request.FILES['thumb'],
        )
        document.save()
    elif doc:
        document = Document(
            title = post_data['title'],
            summary = post_data['summary'],
            description = post_data['description'],
            category = post_data['category'],
            doctype = post_data['type'],
            author = post_data['author'], 
            document = request.FILES['docs'],
        )
        document.save()
    elif thumbnail:
        document = Document(
            title = post_data['title'],
            summary = post_data['summary'],
            description = post_data['description'],
            category = post_data['category'],
            doctype = post_data['type'],
            author = post_data['author'], 
            thumbnail = request.FILES['thumb'],
        )
        document.save()
    else:
        document = Document(
            title = post_data['title'],
            summary = post_data['summary'],
            description = post_data['description'],
            category = post_data['category'],
            doctype = post_data['type'],
            author = post_data['author'], 
        )
        document.save()

    return redirect('dashboard')


@login_required(login_url='/login/')
def savefaq(request):
    post_data = request.POST
    faq = Faq(
        title = post_data['title'],
        description = post_data['description'],
    )
    faq.save()
    return redirect('dashboard')
    

def createAccount(request):
    data = "failed"
    post_data = request.POST
    if post_data['pass'] == post_data['conf_pass']:
        user = User.objects.create_user(post_data['client_phone'], post_data['client_email'], post_data['pass'])
        
        appuser = AppUser(
            user = user,
            name = post_data['client_name'],
            email = post_data['client_email'],
            username = post_data['client_phone'],
            phone = post_data['client_phone'],
            status = "active",
            subscription_type = post_data['subscription_type'],
            charge = 0.00,
        )        
        
        appuser.save()
        return redirect('/')
    else:
        return redirect('about')


def login(request):
    data = ""
    return render(request, 'login.html', {'data': data})
 

def verifylogin(request):
    post_data = request.POST
    if 'user' and 'pass' in post_data:
        user = authenticate(
            request,
            username = post_data['user'],
            password = post_data['pass']
        )
        if user is None:
            return redirect('/')
        elif user.is_superuser:
            auth_login(request, user)
            return redirect('dashboard')
        else:
            auth_login(request, user)            
            return redirect('/')


def userLogout(request):
    logout(request)
    return redirect('/')


def profile(request):
    data = ""
    user_id = request.user.id
    appuser = AppUser.objects.get(user_id=user_id)
    print(user_id)
    return render(request, 'profile.html', {'data': appuser})