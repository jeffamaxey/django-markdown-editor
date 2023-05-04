from django.conf import settings
from django.shortcuts import (render, redirect)
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from app.forms import (SimpleForm, PostForm)
from app.models import Post


def home_redirect_view(request):
    return redirect('simple_form')


def simple_form_view(request):
    form = SimpleForm()
    context = {'form': form, 'title': 'Simple Form'}
    theme = getattr(settings, 'MARTOR_THEME', 'bootstrap')
    return render(request, f'{theme}/form.html', context)


@login_required
def post_form_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, f'{post.title} successfully saved.')
            return redirect('test_markdownify')
    else:
        form = PostForm()
        context = {'form': form, 'title': 'Post Form'}
    theme = getattr(settings, 'MARTOR_THEME', 'bootstrap')
    return render(request, f'{theme}/form.html', context)


def test_markdownify(request):
    post = Post.objects.last()
    context = {'post': post}
    if post is None:
        context = {
            'post': {
                'title': 'Fake Post',
                'description': """It **working**! :heart: [Python Learning](https://python.web.id)"""
            }
        }
    theme = getattr(settings, 'MARTOR_THEME', 'bootstrap')
    return render(request, f'{theme}/test_markdownify.html', context)
