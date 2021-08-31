from django.db import models


class User(models.Model):
    name           = models.CharField(max_length=45)
    email          = models.EmailField()
    password       = models.CharField(max_length=200)
    is_sms_agree   = models.BooleanField(default=False)
    is_email_agree = models.BooleanField(default=False)
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.name
