from django.db import models



class Userip(models.Model):
    userip = models.TextField(default=None)
    def __str__(self):
        return self.userip