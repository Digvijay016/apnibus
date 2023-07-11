from django.contrib import admin
from task.models.task import Task


class TaskAdmin(admin.ModelAdmin):
    model = Task
    list_display = ('title', 'description','priority','task','status','team_type')
    search_fields = ['priority','status','team_type']

admin.site.register(Task, TaskAdmin)