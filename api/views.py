from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination

from .models import *
from .serializers import *
from .utils import *

import os
from datetime import datetime
from biochatter_metta.prompts import BioCypherPromptEngine, get_llm_response
# from biochatter_metta.llm_connect import Conversation, GptConversation
# =========================================================== TOPIC ===========================================================

# class TopicList(generics.ListCreateAPIView):
#     serializer_class = TopicSerializer
#     pagination_class = LimitOffsetPagination
#     queryset = Topic.objects.all()

#     def list(self, request):
#         return get_paginated_records(
#             pagination_class=self.pagination_class,
#             request=request,
#             record_items=self.queryset,
#             record_serializer_class=self.serializer_class
#         )

# class TopicDetail(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = TopicSerializer
#     queryset = Topic.objects.all()

# =========================================================== CHAT ===========================================================

class ChatList(APIView):
    def get(self, request):
        chats = Chat.objects.all()
        return get_paginated_records(
            pagination_class=LimitOffsetPagination,
            request=request,
            record_items=chats,
            record_serializer_class=ChatSerializer
        )
    
    def post(self, request):
        message_text = request.data.get('message_text', '')
        if not message_text:
            return Response('message_text is missing!', status=status.HTTP_400_BAD_REQUEST)

        llm_response, _, _ = get_llm_response(
            openai_api_key='*',
            prompt=f'''\
            Write a short and descriptive chat title based on the sample message below:
            "{message_text}"\
            The title should not me more than fifty characters long.\
            Return only the title and without any explanations.\
            '''.strip()
        )

        chat_record = add_record(
            record_data = {'chat_name': llm_response},
            record_model = Chat,
            record_serializer= ChatSerializer,
            get_serialized_record=True
        )
        chat_id = chat_record['id']

        user_record, llm_record = add_message_record(
            user_data=request.data,
            chat_id=chat_id,
            message_model=Message,
            message_serializer_class=MessageSerializer
        )

        return Response({
            'chat_record': chat_record,
            'user_record': user_record,
            'llm_record': llm_record
        }, status=status.HTTP_201_CREATED)

class ChatDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ChatSerializer
    queryset = Chat.objects.all()

    def update(self, request, pk):
        chat_instance = Chat.objects.get(pk=pk)
        request.data.update({'chat_updated_at': datetime.now()})
        return update_record(
            record_instance = chat_instance,
            update_data = request.data
        )

# =========================================================== MESSAGE ===========================================================

class MessageList(APIView):
    def get(self, request, chat_id):
        chat_exists = record_exists(record_model=Chat, record_id=chat_id)
        if not chat_exists:
            return Response('Invalid Chat ID!' ,status=status.HTTP_400_BAD_REQUEST)
        
        messages = Message.objects.filter(chat_id=chat_id).order_by('-message_created_at')

        # /api/chats/<chat_id>/messages/?limit=2&offset=2 (Limit = no. of messages, Offset = start from)
        return get_paginated_records(
            pagination_class=LimitOffsetPagination,
            request=request,
            record_items=messages,
            record_serializer_class=MessageSerializer
        )
    
    def post(self, request, chat_id):
        chat_exists = record_exists(record_model=Chat, record_id=chat_id)
        if not chat_exists:
            return Response('Invalid Chat ID!' ,status=status.HTTP_400_BAD_REQUEST)

        # Get context length from query parameter
        context_length = self.request.query_params.get('context_length', 20)
        message_history = MessageSerializer( Message.objects.filter(chat_id=chat_id).order_by('-message_created_at')[:context_length], many=True ).data
        # Get the list in ascending chronological order
        message_history.reverse()
        # Format in chat style message
        llm_context = 'Use this interaction history between the "User" and the "Assistant" as additional context.\n\n ###\n'
        for message in message_history:
            smn = 'User' if message['is_user_message'] else 'Assistant'
            llm_context += f"{smn}: {message['message_text']}\n"
        llm_context += '\n###\n\n'

        user_record, llm_record = add_message_record(
            user_data=request.data,
            chat_id=chat_id,
            message_model=Message,
            message_serializer_class=MessageSerializer,
            llm_context=llm_context
        )

        # TODO: check both responses and return a single response
        return Response({
            'user_question': user_record,
            'llm_response': llm_record
        }, status=status.HTTP_201_CREATED)

class MessageDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()

    def update(self, request, pk):
        message_instance = Message.objects.get(pk=pk)
        request.data.update({'message_updated_at': datetime.now()})
        return update_record(
            record_instance = message_instance,
            update_data = request.data
        )

# =========================================================== EXAMPLE ===========================================================

class ExampleList(APIView):
    def get(self, request):
        examples = Example.objects.all()

        return get_paginated_records(
            pagination_class=LimitOffsetPagination,
            request=request,
            record_items=examples,
            record_serializer_class=ExampleSerializer
        )

    def post(self, request):
        return add_record(
            record_data = dict(request.data),
            record_model = Example,
            record_serializer= ExampleSerializer
        )       

class ExampleDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ExampleSerializer
    queryset = Example.objects.all()

    def update(self, request, pk):
        example_instance = Example.objects.get(pk=pk)
        
        return update_record(
            record_instance = example_instance,
            update_data = request.data
        )
