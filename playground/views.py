from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def calculate():
  x = 12 
  return x + 1
def hello_world(request):
  x = 12 
  y = 21
  z = calculate()
  return render(request, 'index.html', {'name':'Hello world','age':21})