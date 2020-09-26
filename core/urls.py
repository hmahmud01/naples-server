from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from core import views

urlpatterns = [
    path('', views.home, name="home"),
    path('article/<int:aid>/', views.article, name="article"),
    path('changepassword/', views.changePassword, name="changepassword"),
    path('contact/', views.contact, name="contact"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('documentadd/', views.documentAdd, name="documentadd"),
    path('savedocument', views.savedocument, name='savedocument'),
    path('savefaq/', views.savefaq, name='savefaq'),
    path('login/', views.login, name="login"),
    path('profile/', views.profile, name="profile"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)