import datetime

from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.contrib.postgres.fields import ArrayField,JSONField
from django_jsonforms.forms import JSONSchemaField

# Create your models (python classes) here.

#type of fields, image, summary text

class Community(models.Model):

    image = models.ImageField(upload_to='images/')
    summary = models.CharField(max_length=200, default="summary")
    name = models.CharField(max_length=200, default="name")
#    dataTypes = models.CharField(max_length=400, default = "name,image,summary")
#    created_date = models.DateField(default=timezone.now)
#builtin function

    def __str__(self):
        return self.name

    def __int__(self):
        return self.id


class Post(models.Model):
    author = models.CharField(default ="bengi", max_length = 200)
    communityId = models.ForeignKey(Community, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
#    created_date = models.DateTimeField(default=timezone.now)
#    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Post2(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=100)
    content = models.TextField()
    communityId = models.ForeignKey(Community, on_delete=models.CASCADE, default=1)
    created_date = models.DateTimeField(default=timezone.now)
    draft = models.BooleanField(default = False)
    created = models.DateTimeField(editable = False)
    modified = models.DateTimeField()
    slug = models.SlugField(unique=True, max_length=150, editable= False)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='modified_by')

    def get_slug(self):
        slug = slugify(self.title.replace("ı", "i"))
        unique = slug
        number = 1

        while Post2.objects.filter(slug=unique).exists():
            unique = '{}-{}'.format(slug, number)
            number += 1

        return unique

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        self.slug = self.get_slug()
        return super(Post2, self).save(*args, **kwargs)


class DataType(models.Model):
    name = models.CharField(max_length=200)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    extra_fields = JSONField(blank=True, default=dict)


    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        return super(DataType, self).save(*args, **kwargs)

class Field(models.Model):
    name = models.CharField(max_length=200)
    field_type = models.CharField(max_length=200)
    required = models.CharField(max_length=200)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    data_type = models.ForeignKey(DataType, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        return super(Field, self).save(*args, **kwargs)

class DataTypeObject(models.Model):
    data_type = models.ForeignKey(DataType, on_delete=models.CASCADE)
    fields = JSONField(blank=True)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)

    # def __str__(self):
    #         return self.title


