from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePage, name='home'),
    path('login/', views.LoginPage, name='login'),
    path('register/', views.register, name='register'),
    path('submissions/', views.user_submissions, name='user_submissions'),
    path('submissions/<int:submission_id>/', views.view_submission, name='view_submission'),
]