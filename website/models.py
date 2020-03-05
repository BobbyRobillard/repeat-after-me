from django.db import models

from django.contrib.auth.models import User

class MouseEvent(models.Model):
    x_pos = models.IntegerField()
    y_pos = models.IntegerField()

# class LenseInQueue(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     lense = models.ForeignKey(Lense, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return "Lense Queue for " + str(self.user)
#
