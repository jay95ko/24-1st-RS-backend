from django.db import models


class User(models.Model):
    name        = models.CharField(max_length=45)
    email       = models.EmailField()
    password    = models.CharField(max_length=200)
    sms_agree   = models.BooleanField(default=False)
    email_agree = models.BooleanField(default=False)

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.name
