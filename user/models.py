from django.db import models


class User(models.Model):
    kakao_token = models.CharField(max_length=200, unique=True, null=True)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=300)
    mobile_number = models.CharField(max_length=11)
    first_name = models.CharField(max_length=15, null=True)
    last_name = models.CharField(max_length=15, null=True)
    introduction = models.CharField(max_length=1000, null=True)
    website_url = models.URLField(max_length=2500, null=True)
    location = models.CharField(max_length=500, null=True)
    twitter = models.CharField(max_length=100, null=True)
    profile_image_url = models.URLField(max_length=2500, null=True)
    regist_datetime = models.DateTimeField(null=True)
    update_datetime = models.DateTimeField(null=True)
    is_use = models.BooleanField()

    class Meta:
        db_table = 'USER'
