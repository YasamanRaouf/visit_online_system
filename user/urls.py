from django.urls import path
from .views import signup_view, edit_profile, login_view, edit_doctor

app_name = 'user'

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('edit_doctor/', edit_doctor, name='edit_doctor'),
]
