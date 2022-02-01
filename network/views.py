from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models.fields import json
from django.http import HttpResponseRedirect
from django.http.response import HttpResponse
from django.shortcuts import render
from django.urls import reverse
import json
from .models import User, Post, Follower, Follow, Like
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

def index(request):
    #Get text input from user after log in to create new post
    if request.user.is_authenticated and request.method == "POST":
        content = request.POST.get("textinput")
        
        if content != "":
            user = User.objects.get(username=request.user.username)
            Post.objects.create(postedby=user, content=content, likes=0)
            results = Post.objects.all().order_by("-datetime")
            for r in results:
                r.likes = Like.objects.filter(likepostid=r.id).count()
                r.save()

            paginator = Paginator(results,5)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            
            return render(request, "network/index.html", {
                "user" : user,
                "page_obj" : page_obj,  
            })

        else:
            return render(request, "network/index.html",{
                "alert": "content is required to post",
            })
    #if new post is not created, display all posts in order of new posts first
    elif request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)
        results = Post.objects.all().order_by("-datetime")
        likeobj = Like.objects.filter(likedby=user.id).values_list('likepostid', flat=True)
        # For counting total likes of particular post (id) and save in Post
        for r in results:
            r.likes = Like.objects.filter(likepostid=r.id).count()
            r.save()
            
        paginator = Paginator(results,5) 
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        return render(request,"network/index.html", {
            "heart" : "\u2764\ufe0f", 
            "user"  : user, 
            "page_obj" : page_obj, 
            "likeobj" : likeobj,
            
        })
    #show error message is someone try to post without login
    elif not request.user.is_authenticated and request.method == "POST":  
         return render(request,"network/index.html", {
             "alert" :"log in required to post",
         })

   # elif request.user.is_authenticated and request.GET.get("edit")== "edit" :  
         #return render(request,"network/editpost.html") 

    else:
        return render(request,"network/index.html")

   
         

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        
        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")



def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))



def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")




def profile(request,id):
        user = User.objects.get(id=id)
        logger = User.objects.get(username=request.user.username)
        results = Post.objects.filter(postedby=id).order_by("-datetime")
        # Gives a list of post ids liked by current user
        likeobj = Like.objects.filter(likedby=logger.id).values_list('likepostid', flat=True)
        for r in results:
            r.likes = Like.objects.filter(likepostid=r.id).count()
            r.save()

        paginator = Paginator(results,5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        # Gives number of followers and number of follows and all posts of current user.
        if request.method == "GET":
            followers = Follower.objects.filter(user=user)
            follows = Follow.objects.filter(user=user)
            # Check if current user follow the clicked profile
            obj = Follow.objects.filter(user=logger, follow=user)
            return render(request, "network/profile.html",{
            'user': user,
            'followers': followers.count(),
            'follows': follows.count(),
            'logger': logger,
            'page_obj': page_obj,
            'obj': obj,
            "heart" : "\u2764\ufe0f",
            "likeobj" : likeobj,
            })

        if request.method == "POST":
            if request.POST.get("btn") == "Follow":
                Follow.objects.create(user=logger, follow=user)
                Follower.objects.create(user=user, follower=logger)
                obj = Follow.objects.filter(user=logger, follow=user)
                follows = Follow.objects.filter(user=user).count()
                followers = Follower.objects.filter(user=user).count()
           
                return render(request, "network/profile.html",{
                'user': user,
                'follows': follows,
                'followers': followers,
                'logger': logger,
                'page_obj': page_obj,
                'obj': obj,
                "heart" : "\u2764\ufe0f",
                "likeobj" : likeobj,
                })
            
           
            else:
                # If "Unfollow" button is clicked delete profiles of (clicked) user from follow model where (current) user is logger
                Follow.objects.filter(user=logger, follow=user).delete()
                # Delete logger profile as follower where user is clicked user.
                Follower.objects.filter(user=user,follower=logger).delete()
                obj = Follow.objects.filter(user=logger, follow=user)
                followers = Follower.objects.filter(user=user)
                follows = Follow.objects.filter(user=user)

                return render(request, "network/profile.html",{
                'user': user,
                'followers': followers.count(),
                'follows': follows.count(),
                'logger': logger,
                'page_obj': page_obj,
                'obj': obj,
                "heart" : "\u2764\ufe0f",
                "likeobj" : likeobj,
                })


        

def following(request):
    
    if request.method == "GET":
        
        logger = User.objects.get(id=request.user.id)
        follows = Follow.objects.filter(user=logger).values_list('follow_id')
        # Gives all posts postedby users whom current user (logger) follow
        results = Post.objects.filter(postedby__in=follows).order_by("-datetime")
        likeobj = Like.objects.filter(likedby=logger).values_list('likepostid', flat=True)         
        for r in results:
            r.likes = Like.objects.filter(likepostid=r.id).count()
            r.save()
        
        paginator = Paginator(results,5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, "network/following.html",{
            'user' : logger,
            'page_obj': page_obj,
            'heart' : "\u2764\ufe0f",
            'likeobj' : likeobj,
            })


@csrf_exempt
def edit(request,num):
    p = Post.objects.get(id=num)
    if request.method == "PUT":
        # Get edited content from user (through script) and save in post object
        data=json.loads(request.body)
        if data.get("content") is not None:
            p.content = data["content"]
        p.save()
        return HttpResponse(status=204)

@csrf_exempt
def likepst(request, num1):
    # Add or delete like based on "content" received from script and save in like model
    likedby = User.objects.get(id=request.user.id)
    post = Post.objects.get(id=num1)
    
    if request.method == "PUT":
        data=json.loads(request.body)
        if data.get("content") == "addlike":
            newobj = Like.objects.create(likedby=likedby, likepostid=post)
            newobj.save()
            

        else:
            Like.objects.filter(likedby=likedby, likepostid=post.id).delete()
            
        post.save       
        return HttpResponse(status=204)
                
               
        