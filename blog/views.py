from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, DetailView, UpdateView, ListView

from . import models, forms


def show_all_posts(request):
    """
    This view will show all of the posts
    """
    if request.user.is_authenticated:
        my_posts = models.Post.objects.filter(creator=request.user)
        other_posts = models.Post.objects.exclude(creator=request.user)
    else:
        my_posts = models.Post.objects.all()
        other_posts = []
    return render(
        request=request,
        context={
            'object_list': my_posts,
            'object_list_2': other_posts,
            'page_title': 'Show all posts'
        },
        template_name='blog/all_posts.html'
    )


@login_required
def create_post(request):
    """
    Creates a post
    """

    if not request.user.has_perm('blog.add_post'):
        raise PermissionDenied('Access denied.')

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

    if not post_instance.creator == request.user:
        return HttpResponseForbidden('Access denied.')
    if not request.user.has_perm('blog.change_post'):
        raise PermissionDenied()

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


class CreateCategory(PermissionRequiredMixin, CreateView):
    model = models.Category
    fields = (
        'name',
        'slug'
    )
    success_url = reverse_lazy('blog:show-all-posts')
    extra_context = {
        'page_title': 'Create a category'
    }
    permission_required = 'blog.add_category'


class UpdateCategory(PermissionRequiredMixin, UpdateView):
    model = models.Category
    fields = (
        'name', 'slug'
    )
    success_url = reverse_lazy('blog:show-all-posts')
    permission_required = 'blog.change_category'


class ViewPost(DetailView):
    model = models.Post


class FilterPostByCategory(ListView):
    model = models.Post
    template_name = 'blog/all_posts.html'

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug', None)
        qs = super().get_queryset()
        qs = qs.filter(categories__slug=category_slug)
        return qs
