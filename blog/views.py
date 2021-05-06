from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from . import models, forms


def show_all_posts(request):
    """
    This view will show all of the posts
    """
    my_posts = models.Post.objects.all()
    return render(
        request=request,
        context={
            'my_posts': my_posts,
            'page_title': 'Show all posts'
        },
        template_name='blog/all_posts.html'
    )


@login_required
def create_post(request):
    """
    Creates a post
    """
    form_instance = forms.PostForm()

    if request.method == 'POST':
        form_instance = forms.PostForm(data=request.POST)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('blog:show-all-posts')

    return render(request, 'blog/create_post.html', {
        'form': form_instance,
    })
