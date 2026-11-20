from rest_framework import serializers
from django.contrib.auth.models import User
from notes_app.models import NoteDB,TaskDB

class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields=['id','username','password','email']
    def create(self,validated_data):
        user= User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email']
        )
        return user

class NoteSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = NoteDB
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
         model = TaskDB
         read_only_fields = ['user']
         fields = '__all__'
