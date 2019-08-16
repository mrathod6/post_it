from __future__ import unicode_literals
from django.db import models
from django.contrib import messages
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['f_name']) < 2:
            errors['f_name'] = "First Name should be at least 2 characters"
        if len(postData['l_name']) < 2:
            errors['l_name'] = "Last Name should be at least 2 characters"
        if len(postData['e_mail']) < 1:
            errors['e_mail'] = "Email cannot be empty"
        if not EMAIL_REGEX.match(postData['e_mail']):
            errors['e_mail'] = 'Invalid Email Address!'
        if len(postData['pwrd']) < 8:
            errors['pwrd'] = 'Password should be at least 8 characters!'
        if postData['pwrd'] != postData['c_pwrd']:
            errors['pwrd'] = 'Passwords do not match'
        user = User.objects.filter(email=postData['e_mail']) # This is setting the variable user to the user from the email...
        if len(user) != 0:
           errors['user'] = "This email has already been registered"
        return errors

class MessageManager(models.Manager):
    def message_validator(self, postData):
        errors = {}
        if len(postData['message']) < 5:
            errors['message'] = "Posts have to be atleast 5 characters"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    def __repr__(self):
        return f"<first_name: {self.first_name} last_name: {self.last_name} email: {self.email} password: {self. password}  created_at: {self.created_at} updated_at: {self.updated_at} ({self.id})>"

class PostIt(models.Model):
    messages = models.TextField()
    author = models.ForeignKey(User, related_name="messages", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name="liked_messages")
    objects = MessageManager()
    def __repr__(self):
        return f"<message: {self.message} author: {self.author} created_at: {self.created_at} updated_at: {self.updated_at} likes: {self.likes} ({self.id})>"