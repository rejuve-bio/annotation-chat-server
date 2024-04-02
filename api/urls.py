from django.urls import path
from .views import *

urlpatterns = [
    path('topics/', TopicList.as_view()),
    path('topics/<int:pk>/', TopicDetail.as_view()),

    path('chats/', ChatListAll.as_view()),
    path('topics/<int:topic_id>/chats/', ChatList.as_view()),
    path('chats/<int:pk>/', ChatDetail.as_view()), # TODO: This is not necessary

    path('chats/<int:chat_id>/messages/', MessageList.as_view()),
    path('messages/<int:pk>/', MessageDetail.as_view()), # TODO: This is not necessary

    path('topics/<int:topic_id>/examples/', ExampleList.as_view()),
    path('examples/<int:pk>/', ExampleDetail.as_view()), # TODO: This is not necessary
]