from django.db import models
from datetime import datetime  
from ..users.models import User
# Create your models here.


class BookManager(models.Manager):
    # def easy_create(self, form, user_id):
    #     if 'book_author1' in form:
    #         if form['book_author1'] != '':
    #             book_author = 'book_author1'
    #     elif 'book_author2' in form:
    #         if form['book_author2'] != '':
    #             book_author = 'book_author2'

    #     user = User.objects.get(id=user_id)
    #     print(user)
    #     book = Book.objects.create(
    #         title=form['book_title'],
    #         author=book_author,
    #         review=form['review'],
    #         # review_by = User.objects.get(id=user_id),
    #         rating=form['rating']
    #     )

    #     return book.id
    pass

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # objects = BookManager()

    # def __str__(self):
    #   return "<Book object: %s %s>" % self.title, self.author

    # def __repr__(self):
    #   return "<Book object: {} {}".format(self.title, self.author)


class ReviewManager(models.Manager):
    def easy_create(self, form, user_id):
        if 'book_author1' in form:
            if form['book_author1'] != '':
                book_author = 'book_author1'
        elif 'book_author2' in form:
            if form['book_author2'] != '':
                book_author = 'book_author2'

        user = User.objects.get(id=user_id)
        book = Book.objects.create(
            title=form['book_title'],
            author=form[book_author]
        )

        print(user)
        review = Review.objects.create(
            review=form['review'],
            rating=form['rating'],
            review_by=user,
            review_to=book
        )

        return review.id

    def easy_review_create(self, form, user_id, book_id):
        user = User.objects.get(id=user_id)
        book = Book.objects.get(id=book_id)
        print("BOOK" , book)
        review = Review.objects.create(
            review = form['review'],
            rating = form['rating'],
            review_by = user,
            review_to = book
        )
        return review.id


class Review(models.Model):
    review = models.TextField()
    rating = models.IntegerField()
    review_by = models.ForeignKey(User, related_name="user_reviews")
    review_to = models.ForeignKey(Book, related_name="book_reviews")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ReviewManager()

    # def __repr__(self):
    #   return "<Review object: {} {}>".format(self.review_by.first_name, self.review_to.title)

    # def __str__(self):
    #   return "<Review object: %s %s" % self.review_by.first_name, self.review_to.title
