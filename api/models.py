import os, yaml
from random import randint
from django.db import models

class Chat(models.Model):
    # topic_id = models.ForeignKey(Topic, on_delete=models.CASCADE)
    chat_name = models.CharField(max_length=100)
    chat_created_at = models.DateTimeField(auto_now_add=True)
    chat_updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.chat_name

class Message(models.Model):
    chat_id = models.ForeignKey(Chat, on_delete=models.CASCADE)
    message_text = models.CharField(max_length=2000)
    is_user_message = models.BooleanField(default=True)
    message_created_at = models.DateTimeField(auto_now_add=True)
    message_updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return 'User Message' if self.is_user_message else 'LLM Message'

class Example(models.Model):
    example_text = models.CharField(max_length=900)
    
    def __str__(self) -> str:
        return self.example_title

class Setting(models.Model):
    message_context_length = models.IntegerField(default=10)
    openai_api_key = models.CharField(max_length=900)

class Schema(models.Model):
    def schema_file_path(instance, filename):
        base_filename, file_extension = os.path.splitext(filename)
        new_filename = f"schema_config{file_extension}"
        return os.path.join('bio_data/biocypher_schema', new_filename)

    schema_file = models.FileField(upload_to=schema_file_path)

class Atomspace(models.Model):
    def metta_file_path(instance, filename):
        base_filename, file_extension = os.path.splitext(filename)
        rand_num = randint(10000, 99999)
        new_filename = f"{base_filename}_{rand_num}{file_extension}"
        return os.path.join('bio_data/bioatomspace', new_filename)
    
        # new_filename = f"custom_prefix_{instance.pk}{file_extension}"
        # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        # return "bio_data/bioatomspace/".format(instance.user.id, filename)

    entity_name = models.CharField(max_length=100)
    entity_type = models.CharField(max_length=10)
    metta_file = models.FileField(upload_to=metta_file_path)

