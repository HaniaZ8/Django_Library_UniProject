from django.contrib import admin
from .models import Borrow, Record, Author, Category

admin.site.register(Record)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Borrow)