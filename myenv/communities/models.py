from django.db import models

# Create your models (python classes) here.

#type of fields, image, summary text

class Community(models.Model):

    image = models.ImageField(upload_to='images/')
    summary = models.CharField(max_length=200)
    name = models.CharField(max_length=200, default="null")
#    dataTypes = models.CharField(ma_length=400, default = "name,image,summary")

#builtin function
    def __str__(self):
        return self.summary

    def __str__(self):
        return self.name

#    def __str__(self):
#        return self.dataTypes
