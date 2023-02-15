from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Board(models.Model):
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='author_board')
