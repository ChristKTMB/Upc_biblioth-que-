from django.shortcuts import render

def BASE(request):
    return render(request, 'home.html')