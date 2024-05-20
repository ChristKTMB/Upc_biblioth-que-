from django.urls import path
from ..views import views, book_views

urlpatterns = [
    path('', views.BASE, name='BASE'),
    path('books/', book_views.index, name='index_book'),
    path('books/<int:book_id>/', book_views.show, name='show_book'),
    path('create-book/', book_views.create, name='create_book'),
    path('books/delete/<int:book_id>', book_views.delete, name='delete_book'),
    path('book/edit/<int:book_id>', book_views.edit, name='edit_book')
]