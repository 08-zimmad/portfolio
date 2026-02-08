from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    USER_TYPES = (("admin", "Admin"), ("me", "Me"), ("visitor", "Visitor"))

    user_type = models.CharField(max_length=20, choices=USER_TYPES, default="visitor")



class Portfolio(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, blank=False, null=False)
    last_name = models.CharField(max_length=30, blank=False, null=False)
    full_name = models.CharField(max_length=40, blank=False, null=False)
    email = models.EmailField(null=False, blank=False)

    # @property
    # def full_name(self):
    #     return self.first_name + ' ' + self.last_name


    def __str__(self):
        return str(self.full_name)



class Experience(models.Model):
    portfolio = models.ForeignKey(
        'Portfolio',
        on_delete=models.CASCADE,
        related_name="experiences"
    )
    company_name = models.CharField(max_length=30, null=False, blank=False)
    years_of_experiece = models.IntegerField(default=0)
    description = models.TextField(null=False)
    join_date = models.DateField(null=False, blank=False)
    is_current_working = models.BooleanField(default=False)
    end_date = models.DateField(null=False, blank=False)

    def __str__(self):
        return str(self.company_name)
    

class Education(models.Model):

    portfolio = models.ForeignKey(
        'Portfolio',
        on_delete=models.CASCADE,
        related_name="educations"
    )
    school_name = models.CharField(max_length=30, null=False, blank=False)
    description = models.TextField(blank=True)
    join_date = models.DateField(null=False, blank=False)
    end_date = models.DateField(null=False, blank=False)

    def __str__(self):
        return str(self.school_name)


class Certificates(models.Model):
    portfolio = models.ForeignKey(
        'Portfolio',
        on_delete=models.CASCADE,
        related_name="certificates"
    )
    name = models.CharField(max_length=30, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    certificate_link = models.URLField(blank=False, null=False)
    course_duration = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return str(self.name)