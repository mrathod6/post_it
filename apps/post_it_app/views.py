from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt


# Home page takes you to the regisration page
def index(request):
    return render(request,"post_it_app/register.html")

# Registration route with redirects incase of validation errors
# Successsful registration takes you to the home page
def registration(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
                        messages.error(request, value)
        return redirect('/')
    else:
        User.objects.create(first_name=request.POST['f_name'],last_name=request.POST['l_name'],email=request.POST['e_mail'],password=bcrypt.hashpw(request.POST['pwrd'].encode(), bcrypt.gensalt()))
        user = User.objects.filter(email=request.POST['e_mail'])
        request.session['id'] = user[0].id
    return redirect('/home')

# Login form display page
def loginview(request):
    return render(request,"post_it_app/loginview.html")

# Login route with validation redirect
# Successful login takes you to the home page
def login(request):
    email = request.POST['e_mail']
    password = request.POST['pwrd']
    user = User.objects.filter(email=request.POST['e_mail'])
    if len(user) == 0:
        messages.error(request,"User not registered")
        return redirect('/loginview')
    else:
        if  bcrypt.checkpw(request.POST['pwrd'].encode(), user[0].password.encode()):
            print(password)
            request.session['id'] = user[0].id
            return redirect('/home')
        else:
            messages.error(request,'Invalid password')
            return redirect('/loginview')

# Home page that displays the users information and all of the post it messages
def home(request):
    context = {
    'user' : User.objects.get(id =request.session['id']),
    'all_the_postits' : PostIt.objects.all(),
    }
    return render(request, 'post_it_app/all_postits.html', context)

# Route to add message to the database
# Success redirects you to home page with new message added to display
def add_postit(request):
    errors = PostIt.objects.message_validator(request.POST)
    if len(errors)>0:
            for key, value in errors.items():
                messages.error(request, value)
    else:
        user = User.objects.get(id=request.session['id'])
        PostIt.objects.create(messages=request.POST['message'], author = user)
    return redirect('/home')

# Details page that shows that particular message and users that liked that message
def details(request, id):
    context = {
        'particular_postit' : PostIt.objects.get(id=id),
        'likes': PostIt.objects.get(id=id).likes.all()
    }
    return render(request, 'post_it_app/details.html', context)

# Delete route that deletes the message if you created it
def delete(request, id):
    id=id
    delete_thought = PostIt.objects.filter(id=id)
    delete_thought.delete()
    return redirect('/home')

# Like message route, adds user that liked the post to the database
def like_message(request, id):
    print("Trying to like a message")
    current_user = User.objects.get(id=request.session['id'])
    current_postit = PostIt.objects.get(id=id)
    current_postit.likes.add(current_user)
    return redirect('/home')

# Logout clears user in session and redirects to registration page
def logout(request):
    request.session.clear()
    return redirect('/')
