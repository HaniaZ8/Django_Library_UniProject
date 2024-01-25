from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('book/<int:pk>', views.book_record, name='record'),
    path('delete_record/<int:pk>', views.delete_record, name='delete_record'),
    path('update_record/<int:pk>', views.update_record, name='update_record'),
    path('unapproved_records/', views.list_unapproved_records, name='list_unapproved_records'),
    path('management/', views.management, name='management'),
    path('authors/', views.author_list, name='author_list'),
    path('categories/', views.category_list, name='category_list'),
    path('borrow_book/<int:pk>', views.borrow_book, name='borrow_book'),
    path('borrowed_books/', views.borrowed_books, name='borrowed_books'),

    
]