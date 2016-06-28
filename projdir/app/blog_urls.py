from django.conf.urls import url

from app.blog import blog,blog_post_edit,blog_post_remove,blog_post_details,search_user_blog_post_by_slug,search_all_blog_posts_by_slug,edit_blog_post_comment,remove_blog_post_comment,search_blog_post,get_all_blog_posts

urlpatterns = [
        url(r'^$',blog, name = 'write_blog'),
        url(r'^search/(?P<slug_str>[\w\-]+)/posts$',search_all_blog_posts_by_slug,name = 'search_all_blog_posts_by_slug'),
        url(r'^user/(?P<user_id>\d+)/slug/(?P<slug_str>[\w\-]+)/posts/$',search_user_blog_post_by_slug,name = 'search_user_blog_post_by_slug'),
        url(r'^post/(?P<post_id>\d+)/edit/$',blog_post_edit,name = 'edit_blog_post'),
        url(r'^post/(?P<post_id>\d+)/remove/$',blog_post_remove,name = 'remove_blog_post'),
        url(r'^post/(?P<post_id>\d+)/details/$',blog_post_details,name = 'blog_post_details'),
        url(r'^post/(?P<post_id>\d+)/comment/(?P<com_id>\d+)/edit/$',edit_blog_post_comment,name = 'edit_blog_post_comment'),
        url(r'^post/(?P<post_id>\d+)/comment/(?P<com_id>\d+)/remove/$',remove_blog_post_comment,name = 'remove_blog_post_comment'),
        url(r'^search_post/$',search_blog_post,name = 'search_blog_post'),
        url(r'^get_all_blog_posts/$',get_all_blog_posts,name = 'get_all_blog_posts'),
]
