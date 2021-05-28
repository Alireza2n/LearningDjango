from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

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
        form_instance = forms.PostForm(data=request.POST, files=request.FILES)
        if form_instance.is_valid():
            form_instance.instance.creator = request.user
            form_instance.save()
            return redirect('blog:show-all-posts')

    return render(request, 'blog/post_form.html', {
        'form': form_instance,
        'page_title': 'Create a new post'
    })


def edit_post(request, pk):
    """
    Edit a single post
    """
    post_instance = get_object_or_404(klass=models.Post, pk=pk)
    if request.method == 'POST':
        form_instance = forms.PostForm(
            instance=post_instance,
            data=request.POST,
            files=request.FILES
        )
        if form_instance.is_valid():
            form_instance.save()
            messages.success(request, 'Saved successfully.')
            return redirect('blog:show-all-posts')
    else:
        # The GET method
        form_instance = forms.PostForm(instance=post_instance)
        return render(
            request,
            context={
                'form': form_instance,
                'page_title': f'Edit post #{post_instance.pk}'
            },
            template_name='blog/post_form.html'
        )


@require_POST
@csrf_exempt
def like_post(request, id):
    """
    Increments post's like field
    """
    result = False

    # Main logic
    post_obj = get_object_or_404(klass=models.Post, pk=id)
    post_obj.likes += 1
    post_obj.save()
    result = True

    # Response
    return JsonResponse({'result': result, 'likes': post_obj.likes})
