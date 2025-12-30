from django.urls import path
from . import views
import uuid

urlpatterns = [
    path('get-token/',views.get_token,name='getToken'),
    path('create-token/',views.create_token,name='createToken'),
    path('update-token-status/<uuid:token_id>/',views.update_token_status,name='updateTokenStatus'),
]