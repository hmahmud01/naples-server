from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from core import views

urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('faq/', views.faq, name="faq"),
    path('article/<int:aid>/', views.article, name="article"),
    path('changepassword/', views.changePassword, name="changepassword"),
    path('passwordchange/', views.passwordchange, name="passwordchange"),
    path('contact/', views.contact, name="contact"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('userlist/', views.userlist, name="userlist"),
    path('deleteuser/<int:uid>', views.deleteuser, name="deleteuser"),
    path('documentadd/', views.documentAdd, name="documentadd"),
    path('savedocument', views.savedocument, name='savedocument'),
    path('savefaq/', views.savefaq, name='savefaq'),
    path('createaccount/', views.createAccount, name='createaccount'),
    path('login/', views.login, name="login"),
    path('verifylogin/', views.verifylogin, name="verifylogin"),
    path('userLogout/', views.userLogout, name="userLogout"),
    path('profile/', views.profile, name="profile"),
    path('subscription/', views.subscription, name="subscription"),
    path('subscriptionsubmit/', views.subscriptionsubmit, name="subscriptionsubmit"),
]   

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)