from django.db import models  

class Creator(models.Model):
    id = models.AutoField(primary_key=True)  
    username = models.CharField(max_length=20)  
    name = models.CharField(max_length=100)  
    email = models.EmailField()  
    password = models.CharField(max_length=150)
    def __str__(self):
        return self.username
      
class Viewer(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20)  
    name = models.CharField(max_length=100)  
    email = models.EmailField()  
    password = models.CharField(max_length=150)   
    def __str__(self):
        return self.username   
  
class Video(models.Model):
    id = models.AutoField(primary_key=True)
    creator = models.ForeignKey(Creator, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    release_date = models.DateField()
    url = models.URLField(max_length=200)
    likes =  models.ManyToManyField(Viewer,blank=True, related_name='likes')
    @property
    def total_likes(self):
        return self.likes.count() 

    def __str__(self):
        return self.name

    
