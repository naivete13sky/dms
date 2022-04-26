from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,r'../templates/index.html')

def dashboard(request):
    return render(request,r'dashboard.html')