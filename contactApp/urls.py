from django.urls import path
from .views import *

urlpatterns = [
    path('', index),

    # REGISTRATION PATHS
    path('register_page', register_page, name='register_page'),
    path('register', register, name='register'),
    
    path('create_otp', create_otp, name='create_otp'),
    path('otp_page', otp_page, name='otp_page'),
    path('verify_otp', verify_otp, name='verify_otp'),

    # LOGIN PATHS
    path('login_page', login_page, name='login_page'),
    path('login', login, name='login'),

    # PROFILE PATHS
    path('profile_page', profile_page, name='profile_page'),
    path('profile_update', profile_update, name='profile_update'),
    path('profile_image_upload', profile_image_upload, name='profile_image_upload'),
    path('password_update', password_update, name='password_update'),

    # CONTACT PATHS
    path('add_contact', add_contact, name='add_contact'),
    path('contact_update/<int:pk>/', contact_update, name='contact_update'),
    path('contact_delete/<int:pk>/', contact_delete, name='contact_delete'),

    # LOGOUT
    path('logout', logout, name='logout'),
    path('profile_data', profile_data, name='profile_data'),

]