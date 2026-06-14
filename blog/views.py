from django.conf import settings
from django.contrib import messages
from django.contrib.postgres.search import TrigramWordSimilarity
from django.core.mail import send_mail
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from taggit.models import Tag

from .forms import CommentForm, EmailPostForm, SearchForm
from .models import Post


class PostListView(ListView):
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/list.html'

    def get_queryset(self):
        queryset = Post.published.prefetch_related('tags')
        self.tag = None

        tag_slug = self.kwargs.get('tag_slug')
        if tag_slug:
            self.tag = get_object_or_404(Tag, slug=tag_slug)
            queryset = queryset.filter(tags=self.tag)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        return context


def post_detail(request, year, month, day, slug):
    post = get_object_or_404(
        Post.published,
        publish__year=year,
        publish__month=month,
        publish__day=day,
        slug=slug,
    )
    comments = post.comments.filter(active=True)
    form = CommentForm()
    post_tags_ids = post.tags.values_list('pk', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(pk=post.pk)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
    return render(
        request, 'blog/detail.html', {'post': post, 'comments': comments, 'form': form, 'similar_posts': similar_posts}
    )


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
    return render(request, 'blog/share.html', {'post': post, 'form': form})


@require_POST
def post_comment(request, pk):
    post = get_object_or_404(Post.published, pk=pk)
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        messages.success(request, 'Комментарий добавлен!')
        return redirect(post.get_absolute_url())
    return render(request, 'blog/comment.html', {'post': post, 'form': form, 'comment': comment})


def post_search(request):
    form = SearchForm()
    results = []
    query = request.GET.get('query')

    if query:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.published.annotate(
                similarity=TrigramWordSimilarity(query, 'title'),
            ).filter(similarity__gt=0.1).order_by('-similarity')

    return render(request, 'blog/search.html', {'form': form, 'query': query, 'results': results})
