from django.db import models

class Topic(models.Model):
    topic_name = models.CharField(max_length=100)
    topic_file = models.FileField(upload_to="bio_atomspace", null=True)

    def __str__(self) -> str:
        return self.topic_name

class Chat(models.Model):
    topic_id = models.ForeignKey(Topic, on_delete=models.CASCADE)
    chat_name = models.CharField(max_length=100)
    chat_created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.chat_name

class Message(models.Model):
    chat_id = models.ForeignKey(Chat, on_delete=models.CASCADE)
    message_text = models.CharField(max_length=2000)
    message_time = models.DateTimeField(auto_now_add=True)
    is_user_message = models.BooleanField(default=True)

    def __str__(self) -> str:
        return 'User Message' if self.is_user_message else 'LLM Message'

class Example(models.Model):
    topic_id = models.ForeignKey(Topic, on_delete=models.CASCADE)
    example_title = models.CharField(max_length=100)
    example_question = models.CharField(max_length=900)
    
    def __str__(self) -> str:
        return self.example_title

class Setting(models.Model):
    message_context_length = models.IntegerField(default=10)