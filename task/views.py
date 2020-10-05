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
    """
    if parametrs.find('completion'):
        pass
    """
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
    return Response({'slug': task.id}, status=status.HTTP_201_CREATED)


# URL /api/task/<slug>
@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes((SessionAuthentication, BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def api_get_update_delete_task(request, slug):
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
        # -- refactoring --
        if request.data.get('title') and request.data.get('title') != task.title:
            response_map['title'] = '{0} -> {1}'.format(
                task.title, request.data['title'])
            task.title = request.data['title']
            change.changed_title = response_map['title']
        if request.data.get('description') and request.data.get('description') != task.description:
            response_map['description'] = '{0} -> {1}'.format(
                task.description, request.data['description'])
            task.title = request.data['description']
            change.changed_description = response_map['description']
        if request.data.get('completion') and request.data.get('completion') != task.completion:
            response_map['completion'] = '{0} -> {1}'.format(
                task.completion, request.data['completion'])
            task.completion = request.data['completion']
            change.changed_completion = response_map['completion']
        try:
            if request.data['status'] in ('new', 'planned', 'in progress', 'done'):
                response_map['status'] = '{0} -> {1}'.format(
                    task.status, request.data['status'])
                task.status = request.data['status']
                change.changed_status = response_map['status']
        except:
            pass
        # -- --
        task.save()
        change.save()
        return Response(response_map, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        task.delete()
        return Response({'done': True}, status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({'detail': "Method \{0}\ not allowed.".format(request.method)},
                        status=status.HTTP_400_BAD_REQUEST)


# URL /api/task/<slug>/changes
@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def api_get_task_changes(request, slug):
    try:
        task = request.user.task_set.get(id=int(slug))
    except ObjectDoesNotExist:
        return Response({"error": "invalid credentials or no such task"},
                        status=status.HTTP_404_NOT_FOUND
                        )
    changes_set = task.taskchange_set.all()
    changes = TaskChangeSerializer(changes_set, many=True)
    return Response(changes.data, status=status.HTTP_200_OK)
