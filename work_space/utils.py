from .models import WorkSpace, Task
from rest_framework import exceptions

def get_filtered_tasks(user_id, workspace_id):
    try:
        current_workspace = WorkSpace.objects.get(id=workspace_id)
    except WorkSpace.DoesNotExist:
        raise ValueError("El espacio de trabajo no existe")
    
        
    workspace_members = current_workspace.menbers.all()

    if not workspace_members.filter(id=user_id).exists():
        raise ValueError("El usuario no pertenece a este espacio de trabajo")
    if not current_workspace.status:
        raise ValueError("Espacio de trabajo no existe o está deshabilitado")
    
    return Task.objects.filter(workspace_id=workspace_id, status=True)
