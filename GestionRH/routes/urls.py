from django.urls import path
from ..views import views, book_views, author_views

app_name = "GestionRH"

urlpatterns = [
    path('', views.BASE, name='BASE'),
    path('user/edit_profile/<int:user_id>', views.edit_profile, name='edit_profile'),
    path('user/change_password/', views.change_password, name='change_password'),
    path('books/', book_views.index, name='index_book'),
    path('books/<int:book_id>/', book_views.show, name='show_book'),
    path('create-book/', book_views.create, name='create_book'),
    path('books/delete/<int:book_id>', book_views.delete, name='delete_book'),
    path('book/edit/<int:book_id>', book_views.edit, name='edit_book'),
    path('authors/', author_views.index, name='index_author'),
    path('create-author/', author_views.create, name='create_author'),
    path('authors/delete/<int:author_id>', author_views.delete, name='delete_author'),
    path('author/edit/<int:author_id>', author_views.edit, name='edit_author'),
]