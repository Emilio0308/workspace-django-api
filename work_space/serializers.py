from rest_framework import serializers
from .models import WorkSpace, Task
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name',
                  'email', 'password', 'date_joined', 'is_active')


class UserSerializerOne(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class UserSerializerUpdate(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

    def update(self, instance, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().update(instance, validated_data)










class WorkSpaceSerializer(serializers.ModelSerializer):
    menbers = UserSerializer(many=True)
    owner = serializers.StringRelatedField()

    class Meta:
        model = WorkSpace
        fields = '__all__'


class CreateWorkSpaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkSpace
        fields = ('name', 'menbers')


class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()
    workspace = serializers.StringRelatedField()

    class Meta:
        model = Task
        exclude = ('status',)

# class CreateTaskSerializer(serializers.ModelSerializer):
    # class Meta:
    #     model = Task
    #     fields = ('title','description')


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        data['user_id'] = user.id
        data['username'] = user.username
        return data
