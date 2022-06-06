from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login_user, name='login_user'),
    path('signup', views.registeruser, name='signup'),
    path('register', views.registerstudent, name='register'),
    path('section-events/<str:pk>/', views.getSectionEvents, name='section-events'),
    path('your-events/<str:pk>/', views.studentpersonalevents, name='student-events'),
    path('your-details/<str:pk>/', views.studentdetails, name='student-details'),
    path('logout', views.logoutUser, name='logout'),
    path('create-section', views.cs, name='create-section'),
    path('delete-sevent/<str:pk>/<str:pk2>',
         views.deleteevents, name='deletes'),
    path('delete-pevent/<str:pk>/<str:pk2>',
         views.deleteeventp, name='deletep'),
    path('change-password', views.changep, name='change-password')
]
