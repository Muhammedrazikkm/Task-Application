from django.shortcuts import render,redirect
from django.views.generic import View
from Taskweb.forms import Userform,Loginform,Taskform,TaskEditform
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from api.models import Tasks
from django.utils.decorators import method_decorator
from django.contrib import messages
# Create your views here.
def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper

class SignView(View):

    def get(self,request,*args,**kwargs):
        form=Userform()
        return render(request,"register.html",{"form":form})

    def post(self,request,*args,**kwargs):
        form=Userform(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            messages.success(request,"account has been created")
            return redirect("signin")
        else:
            messages.error(request,"failed to create")
            return render(request,"register.html",{"form":form})

class LoginView(View):

    def get(self,request,*args,**kwargs):
        form=Loginform()
        return render(request,"login.html",{"form":form})

    def post(self,request,*args,**kwargs):
        form=Loginform(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            psd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=psd)
            if usr:
                login(request,usr)
                return redirect("home")
            else:
                return render(request,"login.html",{"form":form})

@method_decorator(signin_required,name="dispatch")
class LogOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        messages.success(request,"logout successfully")
        return redirect("signin")

@method_decorator(signin_required,name="dispatch")
class IndexView(View):
    def get(self,request,*args,**kwargs):
        return render(request,"index.html")

@method_decorator(signin_required,name="dispatch")    
class TaskCreateView(View):
    def get(self,request,*args,**kwargs):
        form=Taskform()
        return render(request,"task-add.html",{"form":form})

    def post(self,request,*args,**kwargs):
        form=Taskform(request.POST)
        if form.is_valid():
            form.instance.user=request.user
            form.save()
            print("saved")
            messages.success(request,"task added")
            return redirect("task-list")
        else:
            messages.error(request,"failed to create task")
            return render(request,"task-add.html",{"form":form})

@method_decorator(signin_required,name="dispatch")
class TaskListView(View):
    def get(self,request,*args,**kwargs):
        qs=Tasks.objects.filter(user=request.user).order_by("-create_date")
        return render(request,"task-list.html",{"tasks":qs})

@method_decorator(signin_required,name="dispatch")           
class TaskDetailView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        qs=Tasks.objects.get(id=id)
        return render(request,"task-detail.html",{"task":qs})

@method_decorator(signin_required,name="dispatch")
class TaskDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        Tasks.objects.filter(id=id).delete()
        messages.success(request,"task deleted")
        return redirect("task-list")

@method_decorator(signin_required,name="dispatch")
class TaskEditView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        obj=Tasks.objects.get(id=id)
        form=TaskEditform(instance=obj)
        return render(request,"task-edit.html",{"form":form})
    def post(self,request,*args,**kwargs):
        id=kwargs.get("id")
        obj=Tasks.objects.get(id=id)
        form=TaskEditform(request.POST, instance=obj)
        if form .is_valid():
            form.save()
            messages.success(request,"task has been edited")
            return redirect("task-list")
        else:
            messages.error(request,"failed to edit")
            return render(request,"task-edit.html",{"form":form})
