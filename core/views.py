from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required

from core.models import Document, TopStory, AppUser, Faq

def home(request):
    documents = Document.objects.all()    
    faq = Faq.objects.all()
    return render(request, 'index.html', {'data' : documents, 'faq': faq})


def article(request, aid):
    article = Document.objects.get(id=aid)
    return render(request, 'article.html', {'data': article})


def changePassword(request):
    data = ""
    return render(request, 'changePassword.html', {'data': data})


def contact(request):
    data = ""
    return render(request, 'contact.html', {'data': data})


def dashboard(request):
    documents = Document.objects.all()
    faq = Faq.objects.all()
    return render(request, 'dashboard.html', {'data': documents, 'faq': faq})


def documentAdd(request):
    data = ""
    return render(request, 'documentAdd.html', {'data': data})


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


def savefaq(request):
    post_data = request.POST
    faq = Faq(
        title = post_data['title'],
        description = post_data['description'],
    )
    faq.save()
    return redirect('dashboard')


def login(request):
    data = ""
    return render(request, 'login.html', {'data': data})


def profile(request):
    data = ""
    return render(request, 'profile.html', {'data': data})