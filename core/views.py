from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required

from core.models import Document, TopStory, AppUser, Faq, Subscription

def home(request):    
    documents = Document.objects.all()    
    faq = Faq.objects.all()
    topstory = TopStory.objects.all().last()

    username = "USER"
    if request.user.is_authenticated:
        uid = request.user.id
        appuser = AppUser.objects.get(user_id=uid)
        username = appuser.name        

    if topstory:
        return render(request, 'index.html', {'data' : documents, 'faq': faq, 'topstory': topstory, 'username': username})
    else:
        return render(request, 'index.html', {'data' : documents, 'faq': faq, 'username':username})
    


def faq(request):    
    data = ""
    username = "USER"
    if request.user.is_authenticated:
        uid = request.user.id
        appuser = AppUser.objects.get(user_id=uid)
        username = appuser.name     
    return render(request, 'faq.html', {'data': data, 'username':username})


def about(request):
    data = ""
    username = "USER"
    if request.user.is_authenticated:
        uid = request.user.id
        appuser = AppUser.objects.get(user_id=uid)
        username = appuser.name    
    return render(request, 'about.html', {'data': data, 'username':username})


def article(request, aid):
    article = Document.objects.get(id=aid)
    username = "USER"
    if request.user.is_authenticated:
        uid = request.user.id
        appuser = AppUser.objects.get(user_id=uid)
        username = appuser.name    
    return render(request, 'article.html', {'data': article, 'username':username})


def changePassword(request):
    data = ""
    user_id = request.user.id
    appuser = AppUser.objects.get(user_id=user_id)
    username = appuser.name
    return render(request, 'changePassword.html', {'data': data, 'username':username})


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
    if request.user.is_superuser:
        return render(request, 'dashboard.html', {'data': documents, 'faq': faq})   
    else:
        return redirect('/')


@login_required(login_url='/login/')
def topstory(request):
    documents = Document.objects.all()
    topstory = TopStory.objects.all()
    ts_id = ""
    if topstory.last():
        ts_id = topstory.last().document.id
    else:
        ts_id = -1
    if request.user.is_superuser:
        return render(request, 'topstory.html', {'data': documents, 'topstory': topstory, 'ts_id': ts_id})       
    else:
        return redirect('/')


@login_required(login_url='/login/')
def maketopstory(request, did):
    doc = Document.objects.get(id=did)
    ts = TopStory(
        document = doc,
    )
    ts.save()
    return redirect('topstory')


@login_required(login_url='/login/')
def removetopstory(request, did):
    ts = TopStory.objects.get(document__id=did)
    ts.delete()
    return redirect('topstory')


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
        user = User.objects.create_user(post_data['client_email'], post_data['client_email'], post_data['pass'])
        
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
    username = appuser.name
    print(user_id)
    return render(request, 'profile.html', {'data': appuser, 'username':username })


def subscription(request):    
    data = ""
    uid = request.user.id
    appuser = AppUser.objects.get(user_id=uid)

    if appuser.subscription is None:
        data = "Unsubscribed"
    else :
        data = appuser.subscription
    return render(request, 'subscription.html', {'data': data})


def subscriptionsubmit(request):
    uid = request.user.id
    appuser = AppUser.objects.get(user_id=uid)    
    post_data = request.POST

    if appuser.subscription is None:
        print("not subsribed yet")
        subscription = Subscription(
            first_name = post_data['first_name'],
            last_name = post_data['last_name'],
            phone = post_data['phone'],
            email = post_data['email'],
            address = post_data['address'],
            subscription_type = post_data['subscription_type'],
            charge = post_data['subscription_type'],
        )

        subscription.save()
        appuser.subscription = subscription
        appuser.subscription_type = post_data['subscription_type']
        appuser.save()
        return redirect("profile")
    else:
        print(post_data)
        print("subscript exists")
        appuser.subscription.first_name = post_data['first_name'],
        appuser.subscription.last_name = post_data['last_name'],
        appuser.subscription.phone = post_data['phone'],
        appuser.subscription.email = post_data['email'],
        appuser.subscription.address = post_data['address'],
        appuser.subscription.subscription_type = post_data['subscription_type'],
        appuser.subscription.charge = post_data['subscription_type'],
        appuser.subscription.save()
        appuser.subscription_type = post_data['subscription_type']
        appuser.save()

        return redirect("profile")
    