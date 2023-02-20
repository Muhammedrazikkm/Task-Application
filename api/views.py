from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from api.serializers import TasksSerializers,UserSerializer
from django.contrib.auth.models import User
from api.models import Tasks
from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework.decorators import action
from rest_framework import authentication,permissions
# Create your views here.
class TasksView(APIView):
    def get(self,request,*args,**kwargs):
        qs=Tasks.objects.all()
        serializer=TasksSerializers(qs,many=True)
        return Response(data=serializer.data)

    def post(self,request,*args,**kwargs):
        serializer=TasksSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

class TaskDetailView(APIView):
    
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        qs=Tasks.objects.get(id=id)
        serializer=TasksSerializers(qs,many=False)
        return Response(data=serializer.data)

    def delete(self,request,*args,**kwargs):
        id=kwargs.get("id")
        qs=Tasks.objects.get(id=id).delete()
        return Response(data="deleted")

    def put(self,request,*args,**kwargs):
        id=kwargs.get("id")
        obj=Tasks.objects.get(id=id)
        serializer=TasksSerializers(data=request.data,instance=obj)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

class TaskViewsetView(ViewSet):


    def list(self,request,*args,**kwargs):
        qs=Tasks.objects.all()
        serializer=TasksSerializers(qs,many=True)
        return Response(data=serializer.data)

    def create(self,request,*args,**kwargs):
        serializer=TasksSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Tasks.objects.get(id=id)
        serializer=TasksSerializers(qs)
        return Response(data=serializer.data)

    def update(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        obj=Tasks.objects.get(id=id)
        serializer=TasksSerializers(data=request.data,instance=obj)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    def destroy(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        obj=Tasks.objects.get(id=id).delete()
        return Response(data="deleted")

class TasksModelViewsetView(ModelViewSet):
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=TasksSerializers
    queryset=Tasks.objects.all()

    
    def perform_create(self, serializer):
            serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        qs=Tasks.objects.filter(user=request.user)
        serializer=TasksSerializers(qs,many=True)
        return Response(data=serializer.data)

    #def create(self, request, *args, **kwargs):
        #serializer=TasksSerializers(data=request.data)
        #if serializer.is_valid():
            ##serializer.save(user=request.user)
            #return Response(data=serializer.data)
        #else:
            #return Response(data=serializer.errors)


    #def list(self, request, *args, **kwargs):
        #qs=Tasks.objects.all()
        #serializer=TasksSerializers(qs,many=True)
        #print(request.user)
        #return Response(data=serializer.data)
        
    @action(methods=["GET"],detail=False)
    def finished_work(self,request,*args,**kwargs):
        qs=Tasks.objects.filter(status=True)
        serializer=TasksSerializers(qs,many=True)
        return Response(data=serializer.data)
#localhost:8000/api/v1/tasks/{1}/marks_as_done
    @action(methods=["POST"],detail=True)
    def mark_as_done(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Tasks.objects.filter(id=id).update(status=True)
        return Response(data="status updated")

class UserView(ModelViewSet):
    serializer_class=UserSerializer
    queryset=User.objects.all()

    

    def create(self,request,*args,**kwargs):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            ur=User.objects.create_user(**serializer.validated_data)
            serializer=UserSerializer(ur,many=False) #deseialization
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)