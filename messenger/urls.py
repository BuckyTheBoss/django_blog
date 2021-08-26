from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='message_homepage'),
    path('conversation/<int:profile_id>/',views.conversation, name='conversation')
]