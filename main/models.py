import json

from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

import clearbit
from pyhunter import PyHunter

clearbit.key = '8bfcbf3331348694393f83d01f1cbb19'
hunter = PyHunter('75731996db659b854ca82e51934e92ce39a8f603')


class CustomUser(User):
    clearbit_info = models.TextField()
    email_info = models.TextField()

    def save(self, *args, **kwargs):
        # TODO can be separated in different fields from json etc
        self.clearbit_info = json.dumps(clearbit.Enrichment.find(email=self.email, stream=True))
        # TODO create field validator or collect additional information about user
        self.email_info = json.dumps(hunter.email_verifier(self.email))
        super().save(*args, **kwargs)


class Post(models.Model):
    title = models.CharField(max_length=20, default='')
    text = models.TextField()
    author = models.ForeignKey(CustomUser, editable=False, on_delete=models.CASCADE)
    likes = models.IntegerField(editable=False, default=0)
    slug = models.SlugField(unique=True, default='')

    def __str__(self):
        return '{}: {}...'.format(self.author.username, self.text[:5])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
