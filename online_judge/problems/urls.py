from django.urls import path
from . import views

urlpatterns = [
    path('', views.problems_list, name='problems_list'),
    path('<int:id>/', views.problem_details, name='problem_detail'),
    path('problems/add/', views.add_problem, name='add_problem'),
    path('contests/', views.contests_list, name='contests_list'),
    path('contests/create/', views.create_contest, name='create_contest'),
    path('contests/<int:contest_id>/', views.contest_detail, name='contest_detail'),
    path('contests/<int:contest_id>/results/', views.contest_results, name='contest_results'),

]