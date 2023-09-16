from rest_framework import permissions
from .models import WorkSpace

class IsOwnerPermission(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """
    def has_object_permission(self, request, view, obj):
        print('has_object_permission')
        if request.method in permissions.SAFE_METHODS:
            return True
        # Check if the user is the owner of the object
        return obj.owner == request.user
    
    def has_permission(self, request, view):
        reques_user = request.user.id
        user_in_kwargs = int(view.kwargs['owner_id'])
        print(reques_user ,user_in_kwargs )
        return reques_user == user_in_kwargs
    
