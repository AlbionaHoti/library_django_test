from django.db import models
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your models here.

class UserManager(models.Manager):
  def validate(self, form):
    errors = []

    if len(form['first_name']) < 5:
      errors.append("First name must be longer than 5 characters!")
    
    if len(form['last_name']) < 5:
      errors.append("Last name must be longer than 5 characters!")
    
    if not EMAIL_REGEX.match(form['email']):
      errors.append("Must be a valid email address!")

    if len(form['password']) < 8:
      errors.append("Password must be longer than 8 characters!")

    if form['password'] != form['confirm_password']:
      errors.append("You must confirm the password!")

    existing_email = User.objects.filter(email=form['email'])
    if existing_email:
      errors.append("Email already in use.")
      print(existing_email)

    return errors

  
  def easy_create(self, form):
    hashed_pw = bcrypt.hashpw(form['password'].encode(), bcrypt.gensalt())

    user = User.objects.create(
      first_name = form['first_name'],
      last_name = form['last_name'],
      email = form['email'],
      password_hash = hashed_pw
    )
    
    return user.id

  def login(self, form):
    existing_email = User.objects.filter(email=form['email'])

    if existing_email:
      user = existing_email[0]
      if bcrypt.checkpw(form['password'].encode(), user.password_hash.encode()):
        return(True, user.id)
    return(False, "Email or password incorrect!")


class User(models.Model):
  first_name = models.CharField(max_length=255)
  last_name = models.CharField(max_length=255)
  email = models.CharField(max_length=255)
  password_hash = models.CharField(max_length=255)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects = UserManager()

  # def __repr__(self):
  #   return "<User object: {} {}>".format(self.first_name, self.last_name)
  
  # def __str__(self):
  #   return "<User object: %s %s" % self.first_name, self.last_name
