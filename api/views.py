"""Module to define views for API."""

#from rest_framework.views import APIView
from datetime import datetime, timezone
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated # , AllowAny
from rest_framework.parsers import MultiPartParser
from rest_framework.exceptions import APIException
from rest_framework.generics import GenericAPIView
from rest_framework import status
from django.core.cache import cache
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import TaskSerializer
from .models import Task


# Core Operations

class TaskCreate(GenericAPIView):
    """
    An API view to create a task in user's todo list.
    Takes Token in headers and Title, Description, DueDate,
    Attachment, CompletionStatus, CompletionDate in body.
    Creates task in user's todo list (upto 50 tasks per user)
    and return task details in json format.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer
    parser_classes = [MultiPartParser]

    attachment_parameter_config = openapi.Parameter(
    	'attachment', in_=openapi.IN_FORM, description='Description',
    	type=openapi.TYPE_FILE, required=True)

    @swagger_auto_schema(manual_parameters=[attachment_parameter_config])
    def post(self, request):
        """POST method to receive data, validate it and create new task."""

        try:
            user_id = self.request.user.pk
            task = Task(user_id=user_id)
            queryset = Task.objects.filter(user_id=user_id)

            if ('title' not in request.data or
                'dueDate' not in request.data or
                'attachment' not in request.data):

                return Response({'error': 'missing required field(s)'},
                                status=status.HTTP_400_BAD_REQUEST)

            if len(queryset) > 49:
                raise OverflowError("Can't add more tasks, you have reached maximum limit of 50.")

            for query in queryset:
                if query.title==request.data['title']:
                    raise ValueError('Task with this title already exists')
                    break

            if 'completionStatus' in request.data:
                request.data['completionStatus'] = request.data['completionStatus'].lower()

                if (request.data['completionStatus'] == 'true' and
                    'completionDate' not in request.data):

                    request.data['completionDate'] = datetime.utcnow()


            request.data['user'] = user_id
            serializer = TaskSerializer(task, data=request.data)
            serializer.is_valid(raise_exception=True)
            task = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except OverflowError as error:
            return Response({'error': str(error)}, status=status.HTTP_403_FORBIDDEN)

        except ValueError as error:
            return Response({'error': str(error)}, status=status.HTTP_409_CONFLICT)

        except:
            return Response({'error':"task creation failed"}, status=status.HTTP_400_BAD_REQUEST)



class TaskUpdate(GenericAPIView):
    """
    An API view to update an existing task in user's todo list.
    Takes Token in headers and Title, Description, DueDate,
    Attachment, CompletionStatus, CompletionDate in body.
    Updates task in user's todo list and return task details in json format.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer
    parser_classes = [MultiPartParser]

    attachment_parameter_config = openapi.Parameter(
        'attachment', in_=openapi.IN_FORM, description='file attachment',
        type=openapi.TYPE_FILE, required=True)

    title_parameter_config = openapi.Parameter(
        'title', in_=openapi.IN_PATH, description='Title of task to update',
        type=openapi.TYPE_STRING, required=True)

    @swagger_auto_schema(manual_parameters=[attachment_parameter_config, title_parameter_config])
    def put(self, request, title):
        """PUT method to receive data, validate it and update the task."""

        try:
            user_id = self.request.user.pk
            if not Task.objects.filter(user_id=user_id, title=title).exists():
                raise Task.DoesNotExist('Task matching query does not exist')

            if ('title' not in request.data or
                'dueDate' not in request.data or
                'attachment' not in request.data):
                return Response({'error': 'missing required field(s)'},
                                status=status.HTTP_400_BAD_REQUEST)


            queryset = Task.objects.filter(user_id=user_id)
            for query in queryset:
                if title==request.data['title']:
                    break
                elif query.title==request.data['title']:
                    raise ValueError('Task with this title already exists')
                    break

            queryset = queryset.get(title=title)
            if 'completionStatus' not in request.data:
                request.data['completionStatus'] = queryset.completionStatus

            elif 'completionStatus' in request.data:
                request.data['completionStatus'] = request.data['completionStatus'].lower()

                if (request.data['completionStatus'] == 'true' and
                    'completionDate' not in request.data):
                    request.data['completionDate'] = datetime.utcnow()


            request.data['user'] = user_id
            serializer = TaskSerializer(queryset, data=request.data)
            serializer.is_valid(raise_exception=True)
            task = serializer.save()
            return Response(serializer.data)

        except ValueError as error:
            return Response({'error': str(error)}, status=status.HTTP_409_CONFLICT)

        except Task.DoesNotExist as error:
            return Response({'error': str(error)}, status=status.HTTP_404_NOT_FOUND)

        except APIException as error:
            return Response({'error':str(error)}, status=status.HTTP_400_BAD_REQUEST)




class TaskDelete(GenericAPIView):
    """
    An API view to delete a task from todo list.
    Takes Token in headers and Title in request.
    Deletes task (if exists) from user's todo list.
    """

    permission_classes = [IsAuthenticated]

    def delete(self, request, title):
        """DELETE method to receive title of task, validate it and delete the task."""

        try:
            user_id = self.request.user.pk
            queryset = Task.objects.filter(user_id=user_id).get(title=title)
        except Task.DoesNotExist:
            return Response({'error': 'task does not exist'}, status=status.HTTP_404_NOT_FOUND)

        operation = queryset.delete()
        if operation:
            return Response({"success" : "delete successful"}, status=status.HTTP_200_OK)
        else:
            return Response({"failure": "delete failed"}, status=status.HTTP_400_BAD_REQUEST)



class TaskList(GenericAPIView):
    """
    An API view to list all the tasks from user's todo list.
    Takes Token in headers.
    Returns list of tasks details from user's todo list in json format.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Return list of all the tasks of user."""

        try:
            user_id = self.request.user.pk
            queryset = Task.objects.all().filter(user_id=user_id)

        except Task.DoesNotExist:
            return Response({'response': 'tasks does not exist'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TaskSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class TaskDetail(GenericAPIView):
    """
    An API view to get details of a specific task from user's todo list.
    Takes Token in headers and Title of the task.
    Returns task's details (if exists) from user's todo list in json format.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, title):
        """Return detail of a specific task."""

        try:
            user_id = self.request.user.pk
            queryset = Task.objects.filter(user_id=user_id).get(title=title)
            serializer = TaskSerializer(queryset)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Task.DoesNotExist:
            return Response({'error': 'task does not exist'}, status=status.HTTP_404_NOT_FOUND)




# Reports

class TotalTasks(GenericAPIView):
    """
    An API view to generate Total tasks report.
    Takes Token in headers.
    Return report containing - Count of total tasks,
    completed tasks, and remaining tasks.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Return total, completed and remaining tasks of user."""

        try:
            if cache.get(str(request.user.pk)+'_TotalTasks'):
                print('from cache')
                return Response(cache.get(str(request.user.pk)+'_TotalTasks'),
                	            status=status.HTTP_201_CREATED)

            user_id = self.request.user.pk
            queryset = Task.objects.all().filter(user_id=user_id)
            total_tasks = len(queryset)
            completed_tasks = len(queryset.filter(completionStatus=True))
            remaining_tasks = total_tasks - completed_tasks
            report = {'Total Tasks' : total_tasks,
                    'Completed Tasks' : completed_tasks,
                    'Remaining Tasks' : remaining_tasks}

            cache.set(str(request.user.pk)+'_TotalTasks', report, 60*15)
            print('from db')

            return Response(report, status=status.HTTP_201_CREATED)

        except Task.DoesNotExist:
            return Response({'error': 'tasks does not exist'}, status=status.HTTP_404_NOT_FOUND)



class AverageCompleted(GenericAPIView):
    """
    An API view to generate Average Completed report.
    Takes Token in headers.
    Return report containing - Average number of tasks
    completed per day since creation of account.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Return average completed tasks since day of account creation."""

        try:
            if cache.get(str(request.user.pk)+'_AverageCompleted'):
                print('from cache')
                return Response(cache.get(str(request.user.pk)+'_AverageCompleted'),
                	            status=status.HTTP_201_CREATED)

            user_id = self.request.user.pk
            queryset = Task.objects.all().filter(user_id=user_id, completionStatus=True)
            creation_date = request.user.created_at
            now = datetime.now(timezone.utc)
            total_days = (now-creation_date).days
            completed_tasks = len(queryset)
            report = {}

            if total_days == 0:
                report['Average completed tasks'] = str(completed_tasks)+'/day'
            else:
                report['Average completed tasks'] = str(completed_tasks/total_days)+'/day'

            cache.set(str(request.user.pk)+'_AverageCompleted', report, 60*15)
            print('from db')
            return Response(report, status=status.HTTP_201_CREATED)

        except Task.DoesNotExist:
            return Response({'error': 'tasks does not exist'}, status=status.HTTP_404_NOT_FOUND)



class OverdueTasks(GenericAPIView):
    """
    An API view to generate Overdue tasks report.
    Takes Token in headers.
    Return report containing - Count of tasks which
    could not be completed on time.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Return no of overdue tasks."""

        try:
            if cache.get(str(request.user.pk)+'_OverdueTasks'):
                print('from cache')
                return Response(cache.get(str(request.user.pk)+'_OverdueTasks'),
                	            status=status.HTTP_201_CREATED)

            user_id = request.user.pk
            queryset = Task.objects.all().filter(user_id=user_id)
            now = datetime.now(timezone.utc)
            report = {}
            overdue_tasks = 0

            for query in queryset:
                if query.completionStatus: # ==True:
                    if query.completionDate > query.dueDate:
                        overdue_tasks += 1
                else:
                    if now > query.dueDate:
                        overdue_tasks += 1

            if overdue_tasks==0:
                report['Response'] = 'No any task overdue'
            else:
                report['No. of tasks not completed on time'] = str(overdue_tasks)

            cache.set(str(request.user.pk)+'_OverdueTasks', report, 60*15)
            print('from db')
            return Response(report, status=status.HTTP_201_CREATED)

        except Task.DoesNotExist:
            return Response({'error': 'tasks does not exist'}, status=status.HTTP_404_NOT_FOUND)



class MaxDate(GenericAPIView):
    """
    An API view to generate Max Date report.
    Takes Token in headers.
    Return report containing - Date on which maximum
    number of tasks were completed in a single day.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Return date on which maximum tasks were completed."""

        try:
            if cache.get(str(request.user.pk)+'_MaxDate'):
                print('from cache')
                return Response(cache.get(str(request.user.pk)+'_MaxDate'),
                	            status=status.HTTP_201_CREATED)

            user_id = request.user.pk
            queryset = Task.objects.all().filter(user_id=user_id, completionStatus=True)
            completion_dates = {}
            report = {}

            for query in queryset:
                date = str(query.completionDate.date())
                if date not in completion_dates:
                    completion_dates[date] = 1
                else:
                    completion_dates[date] += 1

            max_tasks = 0
            max_date = None
            for date, completed_tasks in completion_dates.items():
                if completed_tasks > max_tasks:
                    max_tasks = completed_tasks
                    max_date = date

            report['Maximum tasks completed on'] = max_date
            report['No. of tasks'] = str(max_tasks)

            cache.set(str(request.user.pk)+'_MaxDate', report, 60*15)
            print('from db')
            return Response(report, status=status.HTTP_201_CREATED)

        except Task.DoesNotExist:
            return Response({'error': 'tasks does not exist'}, status=status.HTTP_404_NOT_FOUND)




class CountOpened(GenericAPIView):
    """
    An API view to generate Total tasks report.
    Takes Token in headers.
    Return report containing - How many tasks are opened on every
    day of the week (mon, tue, wed, ....) since creation of account.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Return weekdays count, specifying how many tasks
        were created on each weekday.
        """

        try:
            if cache.get(str(request.user.pk)+'_CountOpened'):
                print('from cache')
                return Response(cache.get(str(request.user.pk)+'_CountOpened'),
                	            status=status.HTTP_201_CREATED)

            user_id = request.user.pk
            queryset = Task.objects.all().filter(user_id=user_id)
            weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
                        'Friday', 'Saturday', 'Sunday']
            opened_dates = {}

            for query in queryset:
                weekday = query.creationDate.weekday()
                if weekdays[weekday] not in opened_dates:
                    opened_dates[weekdays[weekday]] = 1
                else:
                    opened_dates[weekdays[weekday]] += 1

            if len(opened_dates)==0:
                print('from db')
                return Response({'response':None}, status=status.HTTP_200_OK)

            cache.set(str(request.user.pk)+'_CountOpened', opened_dates, 60*15)
            print('from db')
            return Response(opened_dates, status=status.HTTP_201_CREATED)

        except Task.DoesNotExist:
            return Response({'error': 'tasks does not exist'}, status=status.HTTP_404_NOT_FOUND)



# Algorithms

class SimilarTasks(GenericAPIView):
    """
    An API view to find similar tasks in user's todo list.
    Takes Token in headers.
    Return list of similar tasks from user's todo list.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Return list containing lists of similar tasks."""

        try:
            user_id = request.user.pk
            queryset = Task.objects.all().filter(user_id=user_id)
            if len(queryset)==0:
                raise Task.DoesNotExist('tasks does not exist')
            elif len(queryset)==1:
                return Response({"response" : "Can't find similar tasks, only 1 task exists"},
                	            status=status.HTTP_200_OK)

            similar_tasks = []
            for i in range(0, len(queryset)-1):
                for j in range(i+1, len(queryset)):
                    if len(queryset[i].title) > len(queryset[j].title):
                        title1 = queryset[j].title.split(' ')
                        title2 = queryset[i].title.split(' ')
                    else:
                        title1 = queryset[i].title.split(' ')
                        title2 = queryset[j].title.split(' ')

                    similarity = True
                    for word in title1:
                        if word not in title2:
                            similarity = False
                            break

                    if similarity:
                        similar_tasks.append([queryset[i].title, queryset[j].title])

            if len(similar_tasks)==0:
                return Response({'response': 'No any similar tasks found'},
                	            status=status.HTTP_200_OK)
            else:
                return Response({'List of similar tasks': str(similar_tasks)},
                	            status=status.HTTP_201_CREATED)

        except Task.DoesNotExist:
            return Response({'error': 'tasks does not exist'}, status=status.HTTP_404_NOT_FOUND)
