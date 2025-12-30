from django.urls import path,include
from . import views
import uuid

urlpatterns = [
    path('get-session/<str:clinic_username>/',views.get_session,name='getSession'),
    path('update-session/<uuid:id>/',views.update_session,name='updateSession'),
    path('create-session/',views.create_session,name='createSession'),
    path('delete-session/<uuid:id>/',views.delete_session,name='deleteSession'),
]