from django.shortcuts import render, get_object_or_404, redirect
from ..models import Author

def index(request):
    authors = Author.objects.all().order_by('-id')
    return render(request, 'author/index.html', {'authors': authors, 'active_page': 'index_author'})

def create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        Author.objects.create(name=name)
        return redirect('GestionRH:index_author') 

def delete(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    author.delete()
    return redirect('GestionRH:index_author')

def edit(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    if request.method == 'POST':
        author.name = request.POST.get('name')
        author.save()

        return redirect('GestionRH:index_author')
    
    return render(request, 'author/edit.html', {'author': author })