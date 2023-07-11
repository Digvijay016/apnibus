from rest_framework import serializers
from task.models.task import Task


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'priority',
                  'task', 'status', 'team_type')