from django.db import models 
from django.contrib.auth.models import User



class SearchQuery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE ,null=True)
    query = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add= True)

    def __str__(self) :
        return self.query  
