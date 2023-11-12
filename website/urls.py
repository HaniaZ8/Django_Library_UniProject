from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    #path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('record/<int:pk>', views.customer_record, name='record'),
    path('delete-record/<int:pk>', views.delete_record, name='delete_record'),
    path('update-record/<int:pk>', views.update_record, name='update_record'),
    path('authors/', views.author_list, name='author_list'),
    path('categories/', views.category_list, name='category_list'),
    path('borrow-book/<int:pk>', views.borrow_book, name='borrow_book'),
    
]
#<a href="{% url 'home' %}" class="btn btn-primary"> Back </a>
#<button type="submit" class="btn" style="background-color: #32a852; color: #ffffff;">Borrow</button>