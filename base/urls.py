from django.urls import path
from .views import TaskList, TaskDetail, TaskCreate, TaskUpdate, DeleteView, CustomLoginView, LogoutUser, RegisterPage

# urlpatterns connects URLs to the correct view
urlpatterns = [
    # Since we have class based views, we need to add .as_view() to convert it into a function
    # name="" makes it so templates can reference that path using that name
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutUser, name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),

    path('', TaskList.as_view(), name='tasks'),
    path('task/<int:pk>', TaskDetail.as_view(), name='task'),
    path('task-create/', TaskCreate.as_view(), name='task-create'),
    path('task-update/<int:pk>/', TaskUpdate.as_view(), name='task-update'),
    path('task-delete/<int:pk>/', DeleteView.as_view(), name='task-delete'),
]   