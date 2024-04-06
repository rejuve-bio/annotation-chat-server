from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination

from .models import *
from .serializers import *
from .utils import *

from datetime import datetime
from biochatter_metta.prompts import BioCypherPromptEngine
# =========================================================== TOPIC ===========================================================

class TopicList(generics.ListCreateAPIView):
    serializer_class = TopicSerializer
    pagination_class = LimitOffsetPagination
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
            pagination_class=LimitOffsetPagination,
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
            additional_fields={'topic_id': topic_id}
        )

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
        # print(llm_context)

        # TODO
        # get user message_text
        # get last n interactions / 20 messages
        # pass both to biochatter, receive llm response
        # add Message record with is_user_message=False
        prompt_engine = BioCypherPromptEngine(
                model_name='gpt-3.5-turbo',
                schema_config_or_info_path='./api/bio_data/biocypher_config/schema_config.yaml',
                schema_mappings='./api/bio_data/biocypher_config/schema_mappings.json',
                openai_api_key='*****'
            )
        # user_question = 'What is gene ENSG00000237491 transcribed to?'

        user_message = request.data['message_text']
        try:
            metta_response = prompt_engine.get_metta_response(
                user_question=user_message,
                get_llm_response=True,
                llm_context=llm_context
                )
            # print(metta_response)
            if not metta_response['llm_response']:
                raise Exception('Unable to get LLM response!')
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        llm_message = {
            'message_text': metta_response['llm_response']
        }

        user_record = add_record(
            record_data = dict(request.data),
            record_model = Message,
            record_serializer= MessageSerializer,
            additional_fields={'chat_id': chat_id},
            get_serialized_record=True
        )

        llm_record = add_record(
            record_data = llm_message,
            record_model = Message,
            record_serializer= MessageSerializer,
            additional_fields={'chat_id': chat_id, 'is_user_message': False},
            get_serialized_record=True
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
    def get(self, request, topic_id):
        topic_exists = record_exists(record_model=Topic, record_id=topic_id)
        if not topic_exists:
            return Response('Invalid Topic ID!' ,status=status.HTTP_400_BAD_REQUEST)

        examples = Example.objects.filter(topic_id=topic_id)

        return get_paginated_records(
            pagination_class=LimitOffsetPagination,
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
