from django.contrib import admin
from .models import User, Task, WorkSpace
# Register your models here.

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display= ('id','title','description','done', 'owner_id')
    list_filter = ('title', )
    search_fields = ('title', )

@admin.register(WorkSpace)
class WorkSpaceAdmin(admin.ModelAdmin):
    list_display= ('id','name','created', 'owner_id')
    list_filter = ('name', )
    search_fields = ('name', )