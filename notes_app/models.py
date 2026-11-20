from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class NoteDB(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    discription=models.TextField()
    created_date=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

class TaskDB(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    description=models.TextField()
    due_date=models.DateField()
    status=models.CharField(max_length=100,default="pending")
    created_date=models.DateField( auto_now_add=True)

    def __str__(self):
        return self.title
    
