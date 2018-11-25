from django.db import models

# Create your models here.
class Blog(models.Model):
    header = models.CharField(max_length=50)
    content = models.TextField()
    cover = models.TextField()
    markdownContent = models.TextField()#保存markdown语法内容
    time = models.CharField(max_length=50)
    readTimes = models.IntegerField()
    def __str__(self):
        return self.header