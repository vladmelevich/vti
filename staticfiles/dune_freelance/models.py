from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class Projects_men(models.Model):
    us_manager = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name='user')
    name = models.CharField(max_length=45)
    pay = models.IntegerField()
    men_email = models.EmailField(null=True, blank=True)
    url_reklam = models.URLField()
    date_start = models.DateField()
    date_finish = models.DateField()
    social_category = models.CharField(max_length=255)
    pay_category = models.CharField(max_length=10)
    stat = models.CharField(max_length=15)
    nums = models.IntegerField()

class spec(models.Model):
    us_cpec = models.OneToOneField(User, on_delete=models.CASCADE)
    tel_number = models.CharField(max_length=255)
    rol = models.CharField(max_length=45)

class connect(models.Model):
    user1 = models.OneToOneField(User, on_delete=models.CASCADE, related_name='connections_as_user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='connections_as_user2')

class Bloger(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number_photo = models.IntegerField()
    name_first = models.CharField(max_length=255)
    social_net = models.CharField(max_length=45)
    subs = models.CharField(max_length=45)
    tem = models.CharField(max_length=45)
    url_social_net = models.URLField()

class pay(models.Model):
    bloger = models.ForeignKey(Bloger, on_delete=models.CASCADE)
    summ = models.IntegerField(default=0)


class Applications(models.Model):
    pr = models.ForeignKey(Projects_men, on_delete=models.CASCADE, related_name='pr')
    blog = models.ManyToManyField(Bloger,related_name='blog')
    applicat = models.CharField(max_length=45, default='Отправлено')
    kol = models.IntegerField(default=0)



class Posts(models.Model):
    projects_post = models.OneToOneField(Applications, on_delete=models.CASCADE,related_name='apl_blog_us')
    data_konec = models.DateField(default='2024-12-31')
    format = models.CharField(max_length=500, default='Н/Д')
    work_url = models.URLField()
    kol_p = models.IntegerField(default=0)
    photo = models.ImageField(upload_to='imag/', default='imag/5244856793513975742.jpg')
    name_url = models.CharField(max_length=255)

class date_post_start(models.Model):
     date_nach = models.DateField()
     apl_date = models.ForeignKey(Posts, on_delete=models.CASCADE)


class result(models.Model):
    pst = models.OneToOneField(Posts, on_delete=models.CASCADE)
    id_res = models.IntegerField()
    id_off = models.IntegerField()
    name_off = models.CharField(max_length=255)
    status_off = models.CharField(max_length=255)
    date_off = models.DateField()
    summ_off = models.IntegerField()
