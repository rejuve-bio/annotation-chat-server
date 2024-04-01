from rest_framework.response import Response
from rest_framework import status
from .models import *

# Check if the id exists in the database
def check_id_exists(
        topic_id=None,
        chat_id=None,
        message_id=None,
        example_id=None):
    
    if topic_id and not Topic.objects.filter(pk=topic_id).exists():
        return False, 'Invaild Topic ID!'
    
    if chat_id and not Chat.objects.filter(pk=chat_id).exists():
        return False, 'Invaild Chat ID!'
    
    if message_id and not Chat.objects.filter(pk=message_id).exists():
        return False, 'Invaild Message ID!'
    
    if example_id and not Chat.objects.filter(pk=example_id).exists():
        return False, 'Invaild Example ID!'

    return True, 'Valid!'

# Update only the fields present in update_data
def update_record(record_instance, update_data):
    if record_instance:
        for key, value in update_data.items():
            setattr(record_instance, key, value)
        record_instance.save()