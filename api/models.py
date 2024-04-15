from django.db import models

class Atomspace(models.Model):
    def user_directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        return "bio_data/bioatomspace/".format(instance.user.id, filename)

    schema_name = models.CharField(max_length=100, default='Shema')
    metta_file_name = models.CharField(max_length=100, default='Shema')
    metta_file = models.FileField(upload_to=f"bio_data/bioatomspace/{schema_name}", null=True)

class Schema(models.Model):
    schema_name = models.CharField(max_length=100, default='Shema')
    schema_file = models.FileField(upload_to="bio_data/biocypher_schema", null=True)

    def __str__(self) -> str:
        return self.schema_name

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