from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView

from .forms import EmailPostForm
from .models import Post


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/list.html'


def post_detail(request, year, month, day, slug):
    post = get_object_or_404(
        Post.published,
        publish__year=year,
        publish__month=month,
        publish__day=day,
        slug=slug,
    )
    return render(request, 'blog/detail.html', {'post': post})


def post_share(request, pk):
    post = get_object_or_404(
        Post.published,
        pk=pk,
    )
    form = EmailPostForm()
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f'{cd["name"]} recommends you read {post.title}'
            message = f"Read {post.title} at {post_url}\n\n{cd['name']}'s comments ({cd['email']}):\n{cd['comments']}"
            send_mail(subject, message, settings.EMAIL_HOST_USER, [cd['to']])
            messages.success(request, 'Письмо отправлено!')
            return redirect('blog:post_share', pk=pk)
    return render(
        request,
        'blog/share.html',
        {
            'post': post,
            'form': form,
        },
    )
