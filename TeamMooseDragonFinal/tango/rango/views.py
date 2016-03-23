from django.shortcuts import render, render_to_response, get_object_or_404
from rango.forms import UserForm, UserProfileForm
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from rango.models import User, Er_Room
from rango.models import *
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.context_processors import csrf
from rango.parser import Parse

import logging
import os

LOGGER = logging.getLogger(name='profile')
DEFAULT_RETURNTO_PATH = getattr(settings, 'DEFAULT_RETURNTO_PATH', '/')

def index(request):

    return render(request, 'rango/index.html', {})

# from Tango with Django tutorial
def register(request):
    registered = False
    
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
    
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            
            registered = True
            
        else:
            print user_form.errors, profile_form.errors
            
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
        
    return render(request,
            'rango/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered}) 
  
    
def user_login(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)
        
        if user:
            
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/rango/map/')
            else:
                return HttpResponse("Your account is disabled.")
        else:

            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login information.")

    else:
        return render(request,'rango/login.html', {})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/rango/')


def ER_view(request):
    ER_list = Er_Room.objects.all()
    context_dict = {'ERs': ER_list}
    return render(request,'rango/map.html', context_dict)


class ProfileView(TemplateView):
    
    template_name = 'rango/profile_view.html'
    
    http_method_names = {'get'}
    
    def get_context_data(self, **kwargs):
        LOGGER.debug("rango.views.ProfileView.get_context_data")
        username = self.kwargs.get('username')
        if username:
            user = get_object_or_404(User, username=username)
        elif self.request.user.is_authenticated():
            user = self.request.user
        else:
            raise Http404
        
        return_to = self.request.GET.get('returnTo', DEFAULT_RETURNTO_PATH )
        
        p_form = UserProfileForm(instance=user.userprofile)
        user_form = UserForm(instance=user)
        userprofile=user.userprofile
        
        posts = Post.objects.all()
        
        userposts = []
        for post in posts:
            if str(post.creator) == str(username):
                userposts.append(post)
                
        show_email = user.userprofile.show_email
        
                
        p_form.initial['returnTo'] = return_to
        
        return {'userposts' : userposts, 'p_form': p_form, 
                'user_form' : user_form, 'show_email' : show_email, 
                'posts' : posts, 'userprofile' : userprofile}
    
    
    
@login_required
def profile_edit(request):
    
    if request.POST:
        user = request.user
        user.username=request.POST.get('user')
        user.first_name=request.POST.get('first')
        user.last_name=request.POST.get('last')
        user.email=request.POST.get('email')
        user.save()
        
        profile = request.user.userprofile
        profile.website=request.POST.get('website')
        profile.show_email=request.POST.get('show_email')
        
        print profile.show_email
        profile.save()

        return HttpResponseRedirect('/rango/')
    else:
        return render(request,'rango/profile_edit.html', {})   


# Modified code for a forum (http://lightbird.net/dbe/forum1.html) for review system
def mk_paginator(request, items, num_items):
    """Create and return a paginator."""
    paginator = Paginator(items, num_items)
    try: page = int(request.GET.get("page", '1'))
    except ValueError: page = 1

    try:
        items = paginator.page(page)
    except (InvalidPage, EmptyPage):
        items = paginator.page(paginator.num_pages)
    return items


def list(request):
    """Main listing of ER."""
    reviews = Review.objects.all()
    return render_to_response("rango/list.html", dict(reviews=reviews, user=request.user))


def review(request, pk):
    """Listing of reviews in a given ER."""
    posts = Post.objects.filter(review=pk).order_by("created")
    posts = mk_paginator(request, posts, 15)
    t = Review.objects.get(pk=pk)
    
    return render_to_response("rango/review.html", add_csrf(request, posts=posts, pk=pk, title=t.title))

@login_required
def post(request, ptype, pk):
    """Display a post form."""
    action = reverse("rango.views.%s" % ptype, args=[pk])

    if ptype == "reply":
        title = "Write a review"
        subject = "Review: " + Review.objects.get(pk=pk).title
        location = "Enter the address or city of " + Review.objects.get(pk=pk).title
    
    return render_to_response("rango/post.html", add_csrf(request, subject=subject, action=action,
                                                          title=title, location=location))

def increment_post_counter(request):
    profile = request.user.userprofile
    profile.posts += 1
    profile.save()


@login_required
def reply(request, pk):
    """Post to a review to an ERs."""
    p = request.POST
    if p["body"]:
        review = Review.objects.get(pk=pk)
        post = Post.objects.create(review=review, title=p["subject"], body=p["body"], 
                                   creator=request.user, showemail = request.user.userprofile.show_email,
                                   busyness=p["busyness"], 
                                   bedside=p["bedside"], cleanliness=p['cleanliness'], location=p['location'])
        increment_post_counter(request)
    
    return HttpResponseRedirect(reverse("rango.views.review", args=[pk]) + "?page=last")


def add_csrf(request, **kwargs):
    """Add CSRF to dictionary."""
    d = dict(user=request.user, **kwargs)
    d.update(csrf(request))
    return d

