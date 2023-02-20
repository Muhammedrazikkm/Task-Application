from django.urls import path
from Taskweb import views

urlpatterns=[
    path("signup",views.SignView.as_view(),name="register"),
    path("",views.LoginView.as_view(),name="signin"),
    path('home',views.IndexView.as_view(),name="home"),
    path('tasks/add/',views.TaskCreateView.as_view(),name="task-add"),
    path('tasks/all',views.TaskListView.as_view(),name="task-list"),
    path('tasks/details/<int:id>',views.TaskDetailView.as_view(),name="task-detail"),
    path('tasks/remove/<int:id>',views.TaskDeleteView.as_view(),name="task-delete"),
    path('tasks/<int:id>/change',views.TaskEditView.as_view(),name="task-edit"),
    path('signout',views.LogOutView.as_view(),name="signout")
]