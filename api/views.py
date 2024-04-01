from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .models import *
from .serializers import *
from .utils import *

class TopicList(generics.ListCreateAPIView):
    serializer_class = TopicSerializer
    pagination_class = PageNumberPagination
    queryset = Topic.objects.all()  

    def list(self, request):
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(self.get_queryset(), request)
        serialized_topics = self.serializer_class(result_page, many=True)
        return paginator.get_paginated_response(serialized_topics.data)

class TopicDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TopicSerializer
    queryset = Topic.objects.all()

class ChatListAll(generics.ListAPIView):
    pagination_class = PageNumberPagination
    serializer_class = ChatSerializer
    queryset = Chat.objects.all()

    def list(self, request):
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(self.get_queryset(), request)
        serialized_chats = self.serializer_class(result_page, many=True)
        return paginator.get_paginated_response(serialized_chats.data)    

class ChatList(APIView):
    def get(self, request, topic_id):
        valid, msg = check_id_exists(topic_id=topic_id)
        if not valid:
            return Response(msg, status=status.HTTP_404_NOT_FOUND)
        
        chats = Chat.objects.filter(topic_id=topic_id)
        if not chats.exists():
            return Response('No Chats in Topic!', status=status.HTTP_404_NOT_FOUND)
        
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(chats, request)
        serialized_chats = ChatSerializer(result_page, many=True)
        return paginator.get_paginated_response(serialized_chats.data)
        # serialized_chats = ChatSerializer(chats, many=True)
        # return Response(serialized_chats.data, status=status.HTTP_200_OK)
    
    def post(self, request, topic_id):
        valid, msg = check_id_exists(topic_id=topic_id)
        if not valid:
            return Response(msg, status=status.HTTP_404_NOT_FOUND)
        
        # Append topic_id to chat data
        chat_data = dict(request.data)
        chat_data['topic_id'] = topic_id
        serialized_chat = ChatSerializer(data=chat_data)

        if serialized_chat.is_valid():
            created_chat = Chat.objects.create(**serialized_chat.validated_data)
            serialized_chat = ChatSerializer(created_chat)
            return Response(serialized_chat.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized_chat.errors, status=status.HTTP_400_BAD_REQUEST)

class ChatDetail(APIView):
    def get(self, request, chat_id):
        valid, msg = check_id_exists(chat_id=chat_id)
        if not valid:
            return Response(msg, status=status.HTTP_404_NOT_FOUND)
        
        chat = Chat.objects.get(pk=chat_id)
        serialized_chat = ChatSerializer(chat)
        return Response(serialized_chat.data, status=status.HTTP_200_OK)


    def put(self, request, chat_id):
        valid, msg = check_id_exists(chat_id=chat_id)
        if not valid:
            return Response(msg, status=status.HTTP_404_NOT_FOUND)

        chat_instance = Chat.objects.get(pk=chat_id)
        update_record(
            record_instance=chat_instance,
            update_data=request.data
            )
        
        updated_chat = ChatSerializer(chat_instance).data
        return Response(updated_chat, status=status.HTTP_200_OK)
    
    def delete(self, request, chat_id):
        valid, msg = check_id_exists(chat_id=chat_id)
        if not valid:
            return Response(msg, status=status.HTTP_404_NOT_FOUND)
        
        deleted_chat = Chat.objects.get(pk=chat_id).delete()
        return Response(deleted_chat, status=status.HTTP_200_OK)


class MessageList(APIView):
    def get(self, request, topic_id, chat_id):
        pass

class MessageDetail(APIView):
    def get(self, request, message_id):
        pass

class ExampleList(APIView):
    def get(self, request, topic_id):
        examples = Example.objects.filter(topic_id=topic_id)
        serialized_examples = ExampleSerializer(examples, many=True)
        return Response(serialized_examples.data, status=status.HTTP_200_OK)

    def post(self, request, topic_id):
        example_data = dict(request.data)
        example_data['topic_id'] = topic_id
        serialized_example = ExampleSerializer(data=example_data)

        if serialized_example.is_valid():
            created_example = Example.objects.create(**serialized_example.validated_data)
            serialized_example = ExampleSerializer(created_example)
            return Response(serialized_example.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized_example.errors, status=status.HTTP_400_BAD_REQUEST)        

class ExampleDetail(APIView):
    def get(self, request, example_id):
        example = Example.objects.get(pk=example_id)
        serialized_example = ExampleSerializer(example)
        return Response(serialized_example.data, status=status.HTTP_200_OK)
    
    def put(self, request, example_id):
        example_instance = Example.objects.get(pk=example_id)
        update_record(
            record_instance=example_instance,
            update_data=request.data
            )
        
        updated_example = ExampleSerializer(example_instance).data
        return Response(updated_example, status=status.HTTP_200_OK)
    
    def delete(self, request, example_id):
        deleted_example = Example.objects.get(pk=example_id).delete()
        return Response(deleted_example, status=status.HTTP_200_OK)