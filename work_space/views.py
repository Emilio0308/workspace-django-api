from django.shortcuts import render
from rest_framework import viewsets, status, exceptions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import WorkSpace, Task
from .serializers import TaskSerializer, UserSerializer, WorkSpaceSerializer, CreateWorkSpaceSerializer, UserSerializerOne, UserSerializerUpdate
from .permissions import IsOwnerPermission
from django.contrib.auth.models import User
from django.db.models import Q

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .serializers import CustomTokenObtainPairSerializer

# Create your views here.
class WorkSpaceViewSet(viewsets.ModelViewSet):
    serializer_class = WorkSpaceSerializer
    permission_classes = (IsAuthenticated, IsOwnerPermission)

    def get_queryset(self):
        owner_id = self.kwargs['owner_id']
        workSpaces = WorkSpace.objects.filter( Q(menbers=owner_id), status=True)
        # WorkSpace.objects.filter(Q(owner_id=owner_id) | Q(menbers=owner_id), status=True)
        return workSpaces
    
    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve' :
            return WorkSpaceSerializer
        return CreateWorkSpaceSerializer
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_create(self, serializer):
        owner_id = self.kwargs['owner_id']
        serializer.save(owner_id=owner_id, status=True)

    def update(self, request, *args, **kwargs):
        owner_id = int(self.kwargs['owner_id'])
        member_list = request.data['menbers']

        if owner_id not in member_list:
            raise exceptions.ValidationError({"detail": "no puedes eliminar al dueño del espacio de trabajo"})
        return super().update(request, *args, **kwargs)
    

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class= TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        owner_id = self.kwargs['owner_id']
        workspace_id = self.kwargs['workspace_id']

        try:
            currentWorkSpace = WorkSpace.objects.get(id=workspace_id)
        except WorkSpace.DoesNotExist:
            raise exceptions.ValidationError({"detail": "El espacio de trabajo no existe"})
        
        workSpace_menbers = currentWorkSpace.menbers.all()

        print(currentWorkSpace.status)
        if not workSpace_menbers.filter(id=owner_id).exists():
            raise exceptions.ValidationError({"detail": "El usuario no pertenece a este espacio de trabajo"})
        if currentWorkSpace.status == False :
            raise exceptions.ValidationError({"detail": "espacio de trabajo no existe o deshabilitado"})
        return Task.objects.filter(workspace_id=workspace_id, status=True)
    
    # def get_serializer_class(self):
    #     if self.action == 'create':
    #         return CreateTaskSerializer
    #     return TaskSerializer
    
    def perform_create(self, serializer):
        owner_id = self.kwargs['owner_id']
        workspace_id = self.kwargs['workspace_id']
        serializer.save(owner_id = owner_id, workspace_id= workspace_id)

    def perform_destroy(self, instance):
        instance.status = False
        instance.save()

            

class UserViewSet(viewsets.ModelViewSet):
    queryset= User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserSerializerOne
        if self.action == 'update':
            return UserSerializerUpdate
        return UserSerializer
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

    


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenObtainPairSerializer
