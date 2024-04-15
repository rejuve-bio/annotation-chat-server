from django.urls import path
from .views import *

urlpatterns = [
# ---------------------------------- TOPICS ----------------------------------
    # path('topics/', TopicList.as_view()),
    # GET - List all topics
    # POST - Create a topic  | required fields= topic_name(str), topic_file(file)
                            # | Send request as Multipart formdata
    # path('topics/<int:pk>/', TopicDetail.as_view()),
    # GET - Fetch a topic by ID
    # PUT - Update the topic    | only pass the updated fields
    # DELETE - Delete the topic

# ---------------------------------- CHATS ----------------------------------
    # path('chats/', ChatListAll.as_view()),
    path('chats/', ChatList.as_view()),
    # GET - List all chats
    # POST - Create a chat  | required field = chat_name(str)
    path('chats/<int:pk>/', ChatDetail.as_view()),
    # GET - Fetch a chat by ID
    # PUT - Update the chat    | only pass the updated fields
    # DELETE - Delete the chat

# ---------------------------------- MESSAGES ----------------------------------
    path('chats/<int:chat_id>/messages/', MessageList.as_view()),
    # GET - List all messages in a chat
    # POST - Create a message(question) inside that chat  | required field = message_text(str)
            # | This will take some time as it has to query metta files and prompt the llm 
            # | If successful, the response will be the user's question and the llm's answer (in markdown)
    path('messages/<int:pk>/', MessageDetail.as_view()),
    # GET - Fetch a message by ID
    # PUT - Update the message    | only pass the updated fields
    # DELETE - Delete the message

# ---------------------------------- EXAMPLES ----------------------------------
    path('examples/', ExampleList.as_view()),
    # GET - List all examples
    # POST - Create an example  | required fields = example_text(str)
    path('examples/<int:pk>/', ExampleDetail.as_view())
    # GET - Fetch an example by ID
    # PUT - Update the example    | only pass the updated fields
    # DELETE - Delete the example
]