from django.shortcuts import render, redirect

# Handles common user functionalities
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

# Handles user authentication and user creation
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm

from .models import Task

# Create your views here.
class CustomLoginView(LoginView):
    template_name = 'base/login.html' # Specifies the template name that the class uses
    fields = '__all__'
    redirect_authenticated_user = True # Redirects authenticated users away from register/login page and automatically to task list

    def get_success_url(self):
        return reverse_lazy('tasks') # Redirects user to 'tasks' page which is connected to the TaskList class when logged in
    

class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm # Built-in form for user registration
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks') # After registering, url is redirected to 'tasks' (the task list page)
    
    def form_valid(self, form):
        user = form.save() # Saves the data into the database and returns user instance
        if user is not None:
            login(self.request, user) # Checks if user is successfully created and logs in the user
        return super(RegisterPage, self).form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks') # Returns authenticated user to 'tasks'
        return super(RegisterPage, self).get(*args, **kwargs) # If not authenticated, proceed with register form 


def LogoutUser(request):
    logout(request) # Makes user logout and redirects to the login page
    return redirect('login')


class TaskList(LoginRequiredMixin, ListView): # LoginRequiredMixin ensures only authenticated users can access page
    model = Task # Access Task model
    context_object_name = 'tasks' # Sets name of variable that can be used in HTML templates

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tasks"] = context["tasks"].filter(user=self.request.user) # Filters tasks so user will only see their own tasks
        context["count"] = context["tasks"].filter(complete=False).count() # Uses filtered tasks and counts number of incomplete tasks

        search_input = self.request.GET.get('search-area') or '' # Gets the inputted query in the search bar or an empty string if nothing is there
        if search_input:
            context['tasks'] = context['tasks'].filter(title__icontains=search_input) # Filters the user's tasks to the ones that contain the search_input string
        
        context['search_input'] = search_input 
        return context # Returns context dictionary
    

class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task' # Sets name of variable
    template_name = 'base/task.html' # Specifies name of template


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'complete'] # Specifies which fields to display
    success_url = reverse_lazy('tasks') # Redirects to 'tasks' after creating task

    def form_valid(self, form):
        form.instance.user = self.request.user # Makes the user of the newly created task the logged in user 
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')


class DeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')