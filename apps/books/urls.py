from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^(?P<book_id>\d+)$', views.show, name="show_book"),
    url(r'^(?P<review_id>\d+)$', views.show_review, name="show_review"),
    url(r'^add/$', views.add, name="add"),
    url(r'^create_book/$', views.create_book, name="create_book"),
    url(r'^add_review/(?P<book_id>\d+)$', views.add_review, name="add_review"),
    url(r'^delete_review/(?P<review_id>\d+)$', views.delete_review, name="delete_review")
]