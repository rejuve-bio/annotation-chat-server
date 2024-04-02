from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination

from .models import *
from .serializers import *
from .utils import *

# =========================================================== TOPIC ===========================================================

class TopicList(generics.ListCreateAPIView):
    serializer_class = TopicSerializer
    pagination_class = PageNumberPagination
    queryset = Topic.objects.all()

    def list(self, request):
        return get_paginated_records(
            pagination_class=self.pagination_class,
            request=request,
            record_items=self.queryset,
            record_serializer_class=self.serializer_class
        )

class TopicDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TopicSerializer
    queryset = Topic.objects.all()

# =========================================================== CHAT ===========================================================

class ChatList(APIView):
    def get(self, request, topic_id):
        topic_exists = record_exists(record_model=Topic, record_id=topic_id)
        if not topic_exists:
            return Response('Invalid Topic ID!' ,status=status.HTTP_400_BAD_REQUEST)

        chats = Chat.objects.filter(topic_id=topic_id)
        return get_paginated_records(
            pagination_class=PageNumberPagination,
            request=request,
            record_items=chats,
            record_serializer_class=ChatSerializer
        )
    
    def post(self, request, topic_id):
        topic_exists = record_exists(record_model=Topic, record_id=topic_id)
        if not topic_exists:
            return Response('Invalid Topic ID!' ,status=status.HTTP_400_BAD_REQUEST)

        return add_record(
            record_data = dict(request.data),
            record_model = Chat,
            record_serializer= ChatSerializer,
            foreign_key={'topic_id': topic_id}
        )

class ChatDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ChatSerializer
    queryset = Chat.objects.all()

    def update(self, request, pk):
        chat_instance = Chat.objects.get(pk=pk)
        return update_record(
            record_instance = chat_instance,
            update_data = request.data
        )

class ChatListAll(APIView):
    def get(self, request):
        all_chats = Chat.objects.all()

        # /api/chats/?limit=_&offset=_ (Limit = No. of chats, Offset = start from)
        return get_paginated_records(
            pagination_class=LimitOffsetPagination,
            request=request,
            record_items=all_chats,
            record_serializer_class=ChatSerializer
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
        
        return add_record(
            record_data = dict(request.data),
            record_model = Message,
            record_serializer= MessageSerializer,
            additional_fields={'chat_id': chat_id}
        )

class MessageDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()

    def update(self, request, pk):
        message_instance = Message.objects.get(pk=pk)
        return update_record(
            record_instance = message_instance,
            update_data = request.data
        )

# =========================================================== EXAMPLE ===========================================================

class ExampleList(APIView):
    def get(self, request, topic_id):
        topic_exists = record_exists(record_model=Topic, record_id=topic_id)
        if not topic_exists:
            return Response('Invalid Topic ID!' ,status=status.HTTP_400_BAD_REQUEST)

        examples = Example.objects.filter(topic_id=topic_id)

        return get_paginated_records(
            pagination_class=PageNumberPagination,
            request=request,
            record_items=examples,
            record_serializer_class=ExampleSerializer
        )

    def post(self, request, topic_id):
        topic_exists = record_exists(record_model=Topic, record_id=topic_id)
        if not topic_exists:
            return Response('Invalid Topic ID!' ,status=status.HTTP_400_BAD_REQUEST)

        return add_record(
            record_data = dict(request.data),
            record_model = Example,
            record_serializer= ExampleSerializer,
            additional_fields={'topic_id': topic_id}
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
