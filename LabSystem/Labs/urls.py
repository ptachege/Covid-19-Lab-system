from os import name
from . import views
from django.urls import path

app_name = 'Labs'

urlpatterns = [
    path('', views.index, name='index'),
    path('register_tester/', views.register_tester, name='register_tester'),
    path('tester_list/', views.tester_list, name='tester_list'),
    path('tester_details/<int:pk>/', views.tenant_details, name='tester_details'),
    path('delete_tester/<int:pk>/', views.delete_tester, name='delete_tester'),

    #patients
    path('register_patient', views.register_patient, name='register_patient'),
    path('patient_list', views.patient_list, name='patient_list'),
    path('patients_details/<int:pk>/', views.patients_details, name='patients_details'),
    path('delete_patient/<int:pk>/', views.delete_patient, name='delete_patient'),

    #samples
    path('register_sample/', views.register_sample, name='register_sample'),
    path('sample_list/', views.sample_list, name='sample_list'),
    path('update_sample_result/<int:pk>/', views.update_sample_result, name='update_sample_result'),

    #vaccination
    path('register_vaccination/', views.register_vaccination, name='register_vaccination'),
    path('vaccination_list/', views.vaccination_list, name='vaccination_list'),

    #authentication
    path('login_user/', views.login_user, name='login_user'),
    path('logout_user', views.logout_user, name='logout_user'),
    path('register_user/', views.register, name='register'),

    #reports
    path('infection_per_county/', views.infection_per_county, name='infection_per_county'),
    path('infection_per_county/<str:county>/', views.infection_per_county_detail, name='infection_per_county_detail')
]
