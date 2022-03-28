"""
Definition of urls for DjangoWebProject1.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views


urlpatterns = [
    path('', views.overview, name='overview'),
    path('GreatGrade/dataschange/', views.datas_change, name='dataschange'),
    path('GreatGrade/datasearch/', views.datas_search, name='datasearch'),
    path('GreatGrade/subjectpredict/', views.subject_predict, name='subjectpredict'),
    path('GreatGrade/classpredict/', views.class_predict, name='classpredict'),
    path('GreatGrade/classanalysis/', views.class_analysis, name='classanalysis'),
    path('GreatGrade/subjectanalysis/', views.subject_analysis, name='subjectanalysis'),
    path('GreatGrade/datasadd/', views.datas_add, name='datasadd'),
    path('GreatGrade/datasdel/', views.datas_del, name='datasdel'),
    path('GreatGrade/register/', views.register, name='register'),
    path('GreatGrade/login/',
         LoginView.as_view
         (   
             template_name='app/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Log in',
                 'year' : datetime.now().year,
             }
         ),
         name='login'),
    path('GreatGrade/logout/', LogoutView.as_view(next_page='/GreatGrade/login'), name='logout'),
    path('admin/', admin.site.urls),
]
handler400 = views.bad_request
handler403 = views.permission_denied
handler404 = views.page_not_found
handler500 = views.page_error