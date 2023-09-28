import json
from channels.generic.websocket import WebsocketConsumer
from .serializers import TaskSerializer, TableSerializer
from .models import WorkSpace, Task, Table
from asgiref.sync import async_to_sync


class ConsumerView(WebsocketConsumer):

    def join_workspace_group(self, workspace_id):
        # Agregar al usuario al grupo correspondiente
        async_to_sync(self.channel_layer.group_add)(
            f'workspace_{workspace_id}',
            self.channel_name
        )

    def leave_workspace_group(self):
        # Sacar al usuario del grupo correspondiente
        if self.workspace_id:
            async_to_sync(self.channel_layer.group_discard)(
                f'workspace_{self.workspace_id}',
                self.channel_name
            )
            self.workspace_id = None

    def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.workspace_id = self.scope['url_route']['kwargs']['workspace_id']

        print('cliente conectado')
        self.join_workspace_group(self.workspace_id)
        self.accept()

    def disconnect(self, close_code):
        self.leave_workspace_group()
        self.disconnect()

    def getTaskEvent(self, data, updating=False):
        workspace_id = data.get('workspaceId')
        user_id = self.user_id

        try:
            current_workspace = WorkSpace.objects.get(id=workspace_id)
        except WorkSpace.DoesNotExist:
            raise ValueError("El espacio de trabajo no existe")

        workspace_members = current_workspace.menbers.all()

        if not workspace_members.filter(id=user_id).exists():
            raise ValueError(
                "El usuario no pertenece a este espacio de trabajo")
        if not current_workspace.status:
            raise ValueError(
                "Espacio de trabajo no existe o está deshabilitado")

        allTasks = Task.objects.filter(
            workspace_id=workspace_id, status=True)
        serialized_tasks = TaskSerializer(allTasks, many=True).data

        if updating == True:
            return serialized_tasks

        self.send(text_data=json.dumps({
            'event_type': 'tasks',
            'tasks': serialized_tasks
        }))

    def send_updated_tasks_to_group(self, workspace_id, data):
        updated_tasks = self.getTaskEvent(data, True)

        group_name = f'workspace_{workspace_id}'
        message = {
            'type': 'updated_tasks',
            'updated_tasks': updated_tasks,
        }

        async_to_sync(self.channel_layer.group_send)(group_name, message)

    def updated_tasks(self, event):
        updated_tasks = event['updated_tasks']

        self.send(text_data=json.dumps({
            'event_type': 'updatedTasks',
            'tasks': updated_tasks,
        }))

    def getTables(self, data):
        workspace_id = data.get('workspaceId')
        user_id = self.user_id

        allTables = Table.objects.filter(workspace_id=workspace_id)
        serialized_tables = TableSerializer(allTables, many=True).data

        print(serialized_tables)

        self.send(text_data=json.dumps({
            'event_type': 'tables',
            'tables': serialized_tables
        }))

    def receive(self, text_data):
        data = json.loads(text_data)
        event_type = data.get('event_type')

        if event_type == 'getTasks':
            self.getTaskEvent(data)

        if event_type == 'updated_tasks':
            workspace_id = data.get('workspaceId')
            print('llamar a la funcion send_updated_tasks_to_group')
            self.send_updated_tasks_to_group(workspace_id, data)

        if event_type == 'getTables':
            self.getTables(data)
