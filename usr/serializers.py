from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator

from .models import EntryModel

class NewUserSerializer(serializers.ModelSerializer):
    # username = serializers.CharField(
    #     validators=[UniqueValidator(queryset=User.objects.all())],
    #     max_length=20,
    #     min_length = 4,
    #     required=True
    # )
    username = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())],
        max_length=100, 
        required=True)
    password = serializers.CharField(
        max_length=100,
        min_length = 4,
        write_only=True,
        required=True
    )
    
    class Meta:
        model=User
        fields=['username','password']
        
    def create(self,validated_data):
        return User.objects.create_user(**validated_data)
        



class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = EntryModel
        fields = ['date','entry', 'entry_body', 'amount','owner']