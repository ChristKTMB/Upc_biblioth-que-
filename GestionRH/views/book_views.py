from django.shortcuts import render, get_object_or_404, redirect
from ..models import Book, Author

def index(request):
    books = Book.objects.all().order_by('-id')
    return render(request, 'book/index.html', {'books': books, 'authors': Author.objects.all()})

def show(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'book/show.html', {'book': book})

def create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author_id = request.POST.get('author')
        quantity = request.POST.get('quantity')
        book = Book.objects.create(title=title, author_id=author_id, quantity=quantity)
        return redirect('index') 

def delete(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return redirect('index_book')

def edit(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.title = request.POST.get('title')
        book.quantity = request.POST.get('quantity')
        book.author = request.POST.get('author')
        book.save()

        return redirect('index_book')
    
    return render(request, 'book/edit.html', {'book': book, 'authors': Author.objects.all()})