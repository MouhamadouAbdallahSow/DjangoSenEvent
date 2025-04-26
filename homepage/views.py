from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'home.html')


def pageAcceuil(request):
    return render(request, 'acceuil.html', {'user': request.user})