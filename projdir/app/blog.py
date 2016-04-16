from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User

from .forms import BlogPostForm
from .models import BlogPostModel,BlogPostCommentModel
from .views import loginRequired

from django.utils.datastructures import MultiValueDictKeyError
from .forms import BlogPostCommentForm,SearchForm

from os.path import join as isfile
from django.conf import settings
import os

from itertools import chain
from sets import Set

from .codehub import do_pagination

#decorators comes here
def check_user_access_for_blog_post_edit_delete(func):
    def wrapper(request,post_id,*args,**kwargs):
        post_details = get_object_or_404(BlogPostModel,id = post_id)
        if post_details.user.username  != request.user.username:
            return redirect('/')
        else:
            return func(request,post_id,*args,**kwargs)
    return wrapper


@loginRequired
def blog(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            tags = form.cleaned_data['tags']
            try:
                file = request.FILES['image_file']
            except MultiValueDictKeyError:
                file = ''
            new_blog = BlogPostModel(
                user = request.user,
                title = form.cleaned_data['title'],
                body = form.cleaned_data['body'],
                image_file = file,
            )
            new_blog.save()
            new_blog.tags.add(*tags)
            #flash message
            return redirect('/blog')
    else:
        form = BlogPostForm()
    search_form = SearchForm()
    # all_tags = BlogPostModel.tags.all().distinct()
    blog_posts = BlogPostModel.objects.all().order_by('-created')[:3]
    # blog_posts = do_pagination(request,blog_posts_list,3)
    return render(request,'blog/index.html',{'form':form,'blog_posts':blog_posts,'search_form':search_form})


@loginRequired
@check_user_access_for_blog_post_edit_delete
def blog_post_edit(request,post_id):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            post_details = get_object_or_404(BlogPostModel,id = post_id)
            try:
                file = request.FILES['image_file']
            except:
                file = ''
            if post_details.image_file != file:
                if post_details.image_file:
                    file_path = os.path.join(settings.MEDIA_ROOT,post_details.image_file.name)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
            post_details.image_file = file
            form = BlogPostForm(request.POST,instance = post_details)
            form.save()
            return redirect('/blog')
    else:
        post_details = get_object_or_404(BlogPostModel,id = post_id)
        tagArr = []
        for tag in post_details.tags.all():
            tagArr.append(tag.name)
        tags = ",".join(tagArr)
        blog_post_data = {'title':post_details.title,'body':post_details.body,'tags':tags,'image_file':post_details.image_file}
        form = BlogPostForm(initial = blog_post_data)
    return render(request,'blog/edit_blog_post.html',{'form':form,'blog_post_title':post_details.title})


@loginRequired
@check_user_access_for_blog_post_edit_delete
def blog_post_remove(request,post_id):
    post_details = get_object_or_404(BlogPostModel,id = post_id)
    post_details.delete()
    return redirect('/blog')


@loginRequired
def blog_post_details(request,post_id):
    if request.method == 'POST':
        form = BlogPostCommentForm(request.POST)
        if form.is_valid():
            blog_post = get_object_or_404(BlogPostModel,id = post_id)
            new_comment = BlogPostCommentModel(
                user = request.user,
                blog_post = blog_post,
                comment_text = form.cleaned_data['comment_text']
            )
            new_comment.save()
            return redirect('/blog/post/'+str(post_id)+'/details')
    else:
        form = BlogPostCommentForm()
    post_comments = BlogPostCommentModel.objects.filter(blog_post_id = post_id).order_by('-created')
    post_details = get_object_or_404(BlogPostModel,id = post_id)
    return render(request,'blog/blog_post_details.html',{'post_details':post_details,'form':form,'comments':post_comments})


#decorators here
def check_user_access_for_blog_post_comment_edit(func):
    def wrapper(request,post_id,com_id,*args,**kwargs):
        comment_details = get_object_or_404(BlogPostCommentModel,id = com_id)
        if comment_details.user.username != request.user.username:
            return redirect('/')
        return func(request,post_id,com_id,*args,**kwargs)
    return wrapper


@loginRequired
@check_user_access_for_blog_post_comment_edit
def edit_blog_post_comment(request,post_id,com_id):    #com_id is comment_id
    if request.method == 'POST':
        form = BlogPostCommentForm(request.POST)
        if form.is_valid():
            comment_details = get_object_or_404(BlogPostCommentModel,id = com_id)
            form = BlogPostCommentForm(request.POST,instance = comment_details)
            form.save()
            return redirect('/blog/post/'+str(post_id)+'/details')
    else:
        comment_details = get_object_or_404(BlogPostCommentModel,id = com_id)
        comment_data = {'comment_text':comment_details.comment_text}
        form = BlogPostCommentForm(initial = comment_data)
    return render(request,'blog/edit_blog_post_comment.html',{'form':form})


@loginRequired
@check_user_access_for_blog_post_comment_edit
def remove_blog_post_comment(request,post_id,com_id):
    comment_obj = get_object_or_404(BlogPostCommentModel,id = com_id)
    comment_obj.delete()
    return redirect('/blog/post/'+str(post_id)+'/details')



#searches blog posts of a particular user for a particular tag
@loginRequired
def search_user_blog_post_by_slug(request,user_id,slug_str):
    username = get_object_or_404(User,id = user_id).username
    posts = BlogPostModel.objects.filter(user_id = user_id,tags__slug = slug_str).order_by('-created').distinct()
    return render(request,'blog/user_blog_posts_by_slug.html',{'posts':posts,'username':username,'tag_str':slug_str})


#searches all posts according to slug string
@loginRequired
def search_all_blog_posts_by_slug(request,slug_str):
    posts = BlogPostModel.objects.filter(tags__slug = slug_str).distinct()
    return render(request,'blog/search_all_blog_posts_by_slug.html',{'tag_str':slug_str,'posts':posts})



def search_blog_post(request):
    if request.method == 'POST':
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            search_str = search_form.cleaned_data['search_str']
            blog_post_list = BlogPostModel.objects.filter(title__contains = search_str)
            blog_post_slug = BlogPostModel.objects.filter(tags__name__in = [search_str])
            result_list = list(chain(blog_post_list,blog_post_slug))
            result_list = Set(result_list)
            search_form = SearchForm()
            return render(request,'blog/search_blog_post.html',{'search_form':search_form,'results':result_list,'search_str':search_str})
    else:
        search_form = SearchForm()
    return render(request,'blog/search_blog_post.html',{'search_form':search_form})



def get_all_blog_posts(request):
    blog_post_list = BlogPostModel.objects.all().order_by('-created')
    form = SearchForm()
    blog_posts = do_pagination(request,blog_post_list,4)
    return render(request,'blog/get_all_blog_posts.html',{'blog_posts':blog_posts,'form':SearchForm})
