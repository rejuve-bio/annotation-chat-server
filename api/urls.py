from django.urls import path
from .views import *

urlpatterns = [
    path('topics/', TopicList.as_view()),
    path('topics/<int:pk>/', TopicDetail.as_view()),

    path('topics/<int:topic_id>/chats/', ChatList.as_view()),
    path('topics/<int:topic_id>/chats/<int:chat_id>/', ChatDetail.as_view()), # TODO: This is not necessary

    path('topics/<int:topic_id>/chats/<int:chat_id>/messages/', MessageList.as_view()),
    path('topics/<int:topic_id>/chats/<int:chat_id>/messages/<int:message_id>/', MessageDetail.as_view()), # TODO: This is not necessary

    path('topics/<int:topic_id>/examples/', ExampleList.as_view()),
    path('topics/<int:topic_id>/examples/<int:example_id>/', ExampleDetail.as_view()), # TODO: This is not necessary
]