from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User

from .forms import BlogPostForm
from .models import BlogPostModel
from .views import loginRequired


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
            new_blog = BlogPostModel(
                user = request.user,
                title = form.cleaned_data['title'],
                body = form.cleaned_data['body'],
            )
            new_blog.save()
            new_blog.tags.add(*tags)
            #flash message
            return redirect('/blog')
    else:
        form = BlogPostForm()
    all_tags = BlogPostModel.tags.all().distinct()
    blog_posts = BlogPostModel.objects.all().order_by('-created')
    return render(request,'blog/index.html',{'form':form,'blog_posts':blog_posts,'all_tags':all_tags})


@loginRequired
@check_user_access_for_blog_post_edit_delete
def blog_post_edit(request,post_id):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            post_details = get_object_or_404(BlogPostModel,id = post_id)
            form = BlogPostForm(request.POST,instance = post_details)
            form.save()
            return redirect('/blog')
    else:
        post_details = get_object_or_404(BlogPostModel,id = post_id)
        tagArr = []
        for tag in post_details.tags.all():
            tagArr.append(tag.name)
        tags = ",".join(tagArr)
        blog_post_data = {'title':post_details.title,'body':post_details.body,'tags':tags}
        form = BlogPostForm(initial = blog_post_data)
    return render(request,'blog/edit_blog_post.html',{'form':form})


@loginRequired
@check_user_access_for_blog_post_edit_delete
def blog_post_remove(request,post_id):
    post_details = get_object_or_404(BlogPostModel,id = post_id)
    post_details.delete()
    return redirect('/blog')


@loginRequired
def blog_post_details(request,post_id):
    post_details = get_object_or_404(BlogPostModel,id = post_id)
    return render(request,'blog/blog_post_details.html',{'post_details':post_details})

#searches blog posts of a particular user for a particular tag
@loginRequired
def search_user_blog_post_by_slug(request,user_id,slug_str):
    username = get_object_or_404(User,id = user_id).username
    posts = BlogPostModel.objects.filter(user_id = user_id,tags__slug = slug_str).distinct()
    return render(request,'blog/user_blog_posts_by_slug.html',{'posts':posts,'username':username,'tag_str':slug_str})


#searches all posts according to slug string
def search_all_blog_posts_by_slug(request,slug_str):
    posts = BlogPostModel.objects.filter(tags__slug = slug_str).distinct()
    return render(request,'blog/search_all_blog_posts_by_slug.html',{'tag_str':slug_str,'posts':posts})
