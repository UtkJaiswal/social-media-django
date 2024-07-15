from .models import *
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email','name','phone','age','gender','password')
        
    def create(self,validated_data):
        user = User(
            name        = validated_data['name'],
            email       = validated_data['email'],
            phone       = validated_data['phone'],
            age         = validated_data['age'],
            gender      = validated_data['gender']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class EditUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class EmailLoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

class OtpLoginSerializer(serializers.Serializer):
    i_key = serializers.CharField()
    _pcode = serializers.CharField()

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()



class ResetPasswordsSerializer(serializers.Serializer):
    password = serializers.CharField()
    confirm_password = serializers.CharField()
    key = serializers.CharField(max_length= 25)
