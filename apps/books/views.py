from django.shortcuts import render, redirect, HttpResponse
from django.core.urlresolvers import reverse
from .models import Book, Review, User
# Create your views here.


def index(request):
  books = Review.objects.all()
  last_three = Review.objects.all().order_by('-id')[:3][::-1]
  user_id = request.session['user_id']
  user = User.objects.get(id=user_id)
  context = {
    "books": books,
    "user": user,
    "last_three_books": reversed(last_three)
  }
  return render(request, 'books/index.html', context)


def add(request):
  user_id = request.session['user_id']
  user = User.objects.get(id=user_id)
  context = {
    "user": user
  }
  return render(request, 'books/add_book.html', context)


def create_book(request):
  print(request.POST)
  user_id = request.session['user_id']
  review_id = Review.objects.easy_create(request.POST, user_id)
  print("REVIEW ID: ", review_id)

  return redirect(reverse('books:show_review',  kwargs={"review_id": review_id}))

def show_review(request, review_id):
  print("Review ID: ", review_id)
  review = Review.objects.get(id=review_id)

  book = review.review_to.id
  print("BOOK ID: ", book)

  context = {
    "reviews": Review.objects.filter(review_to=book),
    "book": book
  }
  return render(request, 'books/show_book.html', context)

def show(request, book_id):
  print("Book ID: ", book_id)
  
  book = Book.objects.filter(id=book_id).first()
  if not book:
    review = Review.objects.get(id=book_id)
    book_id = review.review_to.id
    book=Book.objects.get(id=book_id)

  user_id = request.session['user_id']
  user = User.objects.get(id=user_id)
  context = {
    "reviews": Review.objects.filter(review_to=book),
    "book": book,
    "user": user
  }
  return render(request, 'books/show_book.html', context)


def add_review(request, book_id):
  print("Book id: ", book_id)
  user_id = request.session['user_id']
  one_review_id = Review.objects.easy_review_create(request.POST, user_id, book_id)
  return redirect(reverse('books:show_review', kwargs={"review_id": one_review_id} ))


def delete_review(request, review_id):
  review = Review.objects.get(id=review_id)

  review.review = ''
  review.rating = 0
  review.save() 
  return redirect(reverse('books:show_review', kwargs={"review_id": review_id} ))
