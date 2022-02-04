from django.db import models
from acc.models import User

# Create your models here.
class Topic(models.Model):
    subject = models.CharField(max_length=100)
    writer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wri")
    content = models.TextField()
    voter = models.ManyToManyField(User, blank=True, related_name="voter")

    def __str__(self):
        return self.subject 


class Menu(models.Model):
    sub = models.ForeignKey(Topic, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    comment = models.TextField()
    choicer = models.ManyToManyField(User, blank=True)
    pic = models.ImageField(upload_to="vote/%y/%m")
    
    def __str__(self):
        return f"{self.sub} - {self.name}"
    
    def getpic(self):
        if self.pic:
            return self.pic.url
        return "/media/noimage.png"