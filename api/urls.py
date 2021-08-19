from django.urls import path
from . import views

urlpatterns = [
	path('task-create/', views.TaskCreate.as_view(), name="task-create"),
	path('task-list/', views.TaskList.as_view(), name="task-list"),
	path('task-detail/<str:title>/', views.TaskDetail.as_view(), name="task-detail"),
	path('task-update/<str:title>/', views.TaskUpdate.as_view(), name="task-update"),
	path('task-delete/<str:title>/', views.TaskDelete.as_view(), name="task-delete"),

	# paths for reports generation
	path('reports/total-tasks/', views.TotalTasks.as_view(), name="total-tasks"),
	path('reports/average-completed/', views.AverageCompleted.as_view(), name="average-completed"),
	path('reports/overdue-tasks/', views.OverdueTasks.as_view(), name="overdue-tasks"),
	path('reports/max-date/', views.MaxDate.as_view(), name="max-date"),
	path('reports/count-opened/', views.CountOpened.as_view(), name="count-opened"),

	#path for algorithm
	path('reports/similar-tasks/', views.SimilarTasks.as_view(), name="similar-tasks"),
]