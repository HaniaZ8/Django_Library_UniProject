from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - Approved: {self.is_approved}"
    
class Author(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100, default='None')
    birth_year = models.IntegerField(null=True, blank=True)
    death_year = models.IntegerField(null=True, blank=True)
    def __str__(self):
        return f"{self.name} {self.surname}"

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300, default="brak")
    
    def __str__(self):
        return self.name
    
class Record(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, default="Default Title")
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    release_year = models.IntegerField(null=True, blank=True, default=None)
    is_approved = models.BooleanField(default=False)
    is_available = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title


class Borrow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    record = models.ForeignKey('Record', on_delete=models.CASCADE)
    borrow_date = models.DateTimeField(null=True, blank=True)
    return_date = models.DateTimeField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.record.title}"