from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
from ..books.models import Review
# Create your views here.

def index(request):
  if 'user_id' in request.session:
    return redirect('books:index')
  return render(request, 'users/index.html')


def create(request):
  print(request.POST)

  errors = User.objects.validate(request.POST)

  if errors:
    for error in errors:
      messages.error(request, error)

    return redirect('users:index')

  user_id = User.objects.easy_create(request.POST)

  request.session['user_id'] = user_id
  
  print('SESSION USER ID: ', request.session['user_id'])
  return redirect('books:index')


def login(request):

  valid, result = User.objects.login(request.POST)

  if not valid:
    messages.error(request, result)
    return redirect('users:index')
  
  request.session['user_id'] = result
  return redirect('books:index')


def logout(request):
    request.session.clear()
    return redirect('users:index')


def show(request, user_id):
  print("USER ID: ", user_id)
  user = User.objects.get(id=user_id)

  reviews = Review.objects.filter(review_by=user).order_by('-id')
  # last_three_in_ascending_order = reversed(last_three)
  print("user object", user)
  context = {
    "user": user,
    "reviews": reviews,
    "count_reviews": reviews.count()
  }

  return render(request, 'users/show.html', context)