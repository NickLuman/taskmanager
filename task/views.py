from .models import Task, TaskChange
from .serializers import UserSerializer, TaskSerializer, TaskChangeSerializer

from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated

from datetime import datetime, timedelta


# URL /api/signup/
class UserCreate(generics.CreateAPIView):
    """
    View to sign users up the system.

    Returns JSON with status of request.
    """
    authentication_classes = ()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer


# URL /api/login/
class LoginView(APIView):
    """
    View to log users in the system.

    Returns JSON with token for authentication in the system.
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            return Response({"token": user.auth_token.key})
        else:
            return Response({"error": "invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


# URL /api/all/
@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def all_tasks(request):
    """
    View to display all user's tasks.

    Returns JSON with all user's tasks.

    Arg filter_by helps to set the filtering parameter.
    """
    tasks_set = request.user.task_set.all()

    if request.data.get('filter_by_status'):
        tasks_set = tasks_set.filter(status=request.data['filter_by_status'])

    if request.data.get('filter_by_completion'):
        filter_arg = request.data['filter_by_completion']
        now = datetime.now()
        if filter_arg == 'old':
            tasks_set = tasks_set.filter(completion__lt=now)
        elif filter_arg == 'today':
            tasks_set = tasks_set.filter(completion__gt=now,
                                         completion__lt=datetime.fromordinal((now+timedelta(days=1)).toordinal()))
        elif filter_arg == 'tomorrow':
            tasks_set = tasks_set.filter(completion__gt=datetime.fromordinal((now+timedelta(days=1)).toordinal()),
                                         completion__lt=datetime.fromordinal((now+timedelta(days=2)).toordinal()))
        elif filter_arg == 'this month':
            tasks_set = tasks_set.filter(completion__gt=now,
                                         completion__lt=datetime.fromordinal((now+timedelta(days=30)).toordinal()))

    tasks = TaskSerializer(tasks_set, many=True)
    return Response(tasks.data, status=status.HTTP_200_OK)


# URL /api/new/
@api_view(['POST'])
@authentication_classes((SessionAuthentication, BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def api_new_task(request):
    """
    View to adding new task.
    """
    task = Task(user=request.user,
                title=request.data.get('title'),
                description=request.data.get('description'),
                status=request.data.get('status'),
                completion=request.data.get('completion'))
    task.save()
    url = '/'.join(request.build_absolute_uri().split('/')[:-2] + ['task', str(task.id)])
    return Response({'URL': url}, status=status.HTTP_201_CREATED)


# URL /api/task/<slug>
@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes((SessionAuthentication, BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def api_get_update_delete_task(request, slug):
    """
    View to get, update, delete task.
    """
    try:
        task = request.user.task_set.get(id=int(slug))
    except ObjectDoesNotExist:
        return Response({"error": "invalid credentials or no such task"},
                        status=status.HTTP_404_NOT_FOUND
                        )
    if request.method == 'GET':
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        response_map = {
            'title': 'empty/invalid format/the same data',
            'description': 'empty/invalid format/the same data',
            'status': 'empty/invalid format/the same data',
            'completion': 'empty/invalid format/the same data',
        }
        change = TaskChange(task=task)

        def changes_controller(field, task_field, change_field):
            if request.data.get(field) and request.data.get(field) != task_field:
                if (field == 'status' and request.data[field] in ('new', 'planned', 'in progress', 'done')) or field != 'status':
                    response_map[field] = '{0} -> {1}'.format(
                        task_field, request.data[field])
                    task_field = request.data[field]
                    change_field = response_map[field]
            return task_field, change_field

        task.title, change.changed_title = changes_controller(
            'title', task.title, change.changed_title)
        task.description, change.changed_description = changes_controller('description', task.description,
                                                                          change.changed_description)
        task.completion, change.changed_completion = changes_controller('completion', task.completion,
                                                                        change.changed_completion)
        task.status, change.changed_status = changes_controller(
            'status', task.status, change.changed_status)
        task.save()
        change.save()
        return Response(response_map, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        task.delete()
        return Response({'done': True}, status=status.HTTP_204_NO_CONTENT)


# URL /api/task/<slug>/changes
@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def api_get_task_changes(request, slug):
    """
    View to get list of task's changes.
    """
    try:
        task = request.user.task_set.get(id=int(slug))
    except ObjectDoesNotExist:
        return Response({"error": "invalid credentials or no such task"},
                        status=status.HTTP_404_NOT_FOUND
                        )
    changes_set = task.taskchange_set.all()
    changes = TaskChangeSerializer(changes_set, many=True)
    return Response(changes.data, status=status.HTTP_200_OK)
