from django.shortcuts import render,get_object_or_404
from django.contrib.auth.models import User
from notes_app.serializers import RegisterSerializer,NoteSerializer,TaskSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from notes_app.models import NoteDB,TaskDB
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.


class RegistrationView(APIView):
    def post(self,request):
        serializer_instance=RegisterSerializer(data=request.data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response( data={"Message":"REGISTRATION SUCCESSFUL"})
        else:
            return Response(data=serializer_instance.errors)

class NotesListCreateView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        notes=NoteDB.objects.filter(user=request.user)
        serializer_instance=NoteSerializer(notes,many=True)
        return Response(serializer_instance.data)

    def post(self, request):
        serializer_instance = NoteSerializer(data=request.data)

        if serializer_instance.is_valid():
            serializer_instance.save(user=request.user)
            return Response(serializer_instance.data)

        else:
            return Response(serializer_instance.errors)

class NotesRetrieveUpdateDelete(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request, pk):
        note_object = get_object_or_404(NoteDB, id=pk)

        if note_object.user == request.user:
            serializer_instance = NoteSerializer(note_object)
            return Response(data=serializer_instance.data)
        else:
            raise serializers.ValidationError("Access denied")

    def put(self, request, pk):
        note_object = get_object_or_404(NoteDB, id=pk)

        if note_object.user == request.user:
            serializer_instance = NoteSerializer(note_object, data=request.data)

            if serializer_instance.is_valid():
                serializer_instance.save()
                return Response(data=serializer_instance.data)
            else:
                return Response(data=serializer_instance.errors)
        else:
            raise serializers.ValidationError("Access denied")

    def delete(self, request, pk):
        note_object = get_object_or_404(NoteDB, id=pk)

        if note_object.user == request.user:
            note_object.delete()
            return Response(data={"message": "Note deleted successfully"})
        else:
            raise serializers.ValidationError("Access denied")

class LogoutView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        request.user.auth_token.delete()
        return Response({"message":"logout success"})


class TaskView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        task_object = TaskDB.objects.filter(user=request.user)

        serializer_instance = TaskSerializer(task_object, many=True)

        return Response(data=serializer_instance.data)

    def post(self,request):
        serializer_instance=TaskSerializer(data=request.data)
        if serializer_instance.is_valid():
            serializer_instance.save(user=request.user)
            return Response(serializer_instance.data)
        else:
            
            return Response(serializer_instance.errors)


class TaskRetrieveUpdateDeleteView(APIView):
     permission_classes=[IsAuthenticated]
     def get_task(self,request,id):
         return get_object_or_404(TaskDB,id=id,user=request.user)
     
     def get(self, request, id):
        task_object = self.get_task(request, id)

        serializer_instance = TaskSerializer(task_object)

        return Response(data=serializer_instance.data)
     def put(self, request, id):
        task_object = self.get_task(request, id)

        serializer_instance = TaskSerializer(
            task_object,
            data=request.data
        )

        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data=serializer_instance.data)
        else:
            return Response(data=serializer_instance.errors)

     def delete(self, request, id):
        task_object = self.get_task(request, id)

        task_object.delete()

        return Response(data={"message": "Task deleted successfully"})


class JWT_Logout(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        try:
           refresh_token=request.data.get('refresh')
           token=RefreshToken(refresh_token)
           token.blacklist()
           return Response({
               "message":"logout success"
           })
        except Exception:
            return Response({
                "ERROR":"REFRESH TOKEN"
            })