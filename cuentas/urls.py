from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views


urlpatterns = [
    path('registro/', views.RegistroView.as_view(), name='registro'),
    path('login/', views.LoginPersonalizadoView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('panel/', views.panel_usuario, name='panel_usuario'),
]
