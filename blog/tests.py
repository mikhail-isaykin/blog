from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase
from django.urls import reverse

from .models import Comment, Post

User = get_user_model()


class PostModelTest(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(username='ivan', password='secret123')
        self.post = Post.objects.create(
            author=self.author,
            title='Test Post',
            slug='test-post',
            body='Some body text',
            status=Post.Status.PUBLISHED,
        )

    def test_str_returns_title(self):
        self.assertEqual(str(self.post), 'Test Post')

    def test_get_absolute_url(self):
        """URL строится из даты публикации и слага."""
        expected = reverse(
            'blog:post_detail',
            kwargs={
                'year': self.post.publish.year,
                'month': self.post.publish.month,
                'day': self.post.publish.day,
                'slug': self.post.slug,
            },
        )
        self.assertEqual(self.post.get_absolute_url(), expected)

    def test_default_status_is_draft(self):
        """Без явного статуса пост создаётся черновиком."""
        draft = Post.objects.create(
            author=self.author,
            title='Draft Post',
            slug='draft-post',
            body='text',
        )
        self.assertEqual(draft.status, Post.Status.DRAFT)


class PublishedManagerTest(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(username='ivan', password='secret123')
        Post.objects.create(
            author=self.author,
            title='Published',
            slug='published',
            body='text',
            status=Post.Status.PUBLISHED,
        )
        Post.objects.create(
            author=self.author,
            title='Draft',
            slug='draft',
            body='text',
            status=Post.Status.DRAFT,
        )

    def test_published_manager_returns_only_published(self):
        """published отдаёт только опубликованные посты."""
        self.assertEqual(Post.published.count(), 1)
        self.assertEqual(Post.published.first().title, 'Published')

    def test_default_manager_returns_all(self):
        """objects отдаёт все посты, включая черновики."""
        self.assertEqual(Post.objects.count(), 2)


class CommentModelTest(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(username='ivan', password='secret123')
        self.post = Post.objects.create(
            author=self.author,
            title='Test Post',
            slug='test-post',
            body='text',
            status=Post.Status.PUBLISHED,
        )
        self.comment = Comment.objects.create(
            post=self.post,
            name='Petr',
            email='petr@example.com',
            body='Nice post',
        )

    def test_str(self):
        self.assertEqual(str(self.comment), 'Comment by Petr on Test Post')

    def test_comment_linked_to_post(self):
        """Комментарий доступен через related_name 'comments'."""
        self.assertIn(self.comment, self.post.comments.all())

    def test_comment_active_by_default(self):
        self.assertTrue(self.comment.active)


class PostListViewTest(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(username='ivan', password='secret123')
        # 4 опубликованных + 1 черновик
        for i in range(4):
            Post.objects.create(
                author=self.author,
                title=f'Post {i}',
                slug=f'post-{i}',
                body='text',
                status=Post.Status.PUBLISHED,
            )
        Post.objects.create(
            author=self.author,
            title='Draft',
            slug='draft',
            body='text',
            status=Post.Status.DRAFT,
        )

    def test_list_shows_only_published(self):
        response = self.client.get(reverse('blog:post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/list.html')
        # paginate_by=3 → на первой странице 3 поста
        self.assertEqual(len(response.context['posts']), 3)

    def test_pagination_second_page(self):
        response = self.client.get(reverse('blog:post_list') + '?page=2')
        self.assertEqual(response.status_code, 200)
        # 4 опубликованных всего → на 2-й странице 1 пост
        self.assertEqual(len(response.context['posts']), 1)

    def test_filter_by_tag(self):
        post = Post.objects.first()
        post.tags.add('django')
        response = self.client.get(reverse('blog:post_list_by_tag', kwargs={'tag_slug': 'django'}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['posts']), 1)
        self.assertIsNotNone(response.context['tag'])


class PostDetailViewTest(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(username='ivan', password='secret123')
        self.post = Post.objects.create(
            author=self.author,
            title='Test Post',
            slug='test-post',
            body='text',
            status=Post.Status.PUBLISHED,
        )

    def test_detail_returns_post(self):
        response = self.client.get(self.post.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/detail.html')
        self.assertEqual(response.context['post'], self.post)

    def test_detail_shows_only_active_comments(self):
        Comment.objects.create(
            post=self.post,
            name='A',
            email='a@x.com',
            body='visible',
            active=True,
        )
        Comment.objects.create(
            post=self.post,
            name='B',
            email='b@x.com',
            body='hidden',
            active=False,
        )
        response = self.client.get(self.post.get_absolute_url())
        self.assertEqual(len(response.context['comments']), 1)

    def test_draft_returns_404(self):
        draft = Post.objects.create(
            author=self.author,
            title='Draft',
            slug='draft',
            body='text',
            status=Post.Status.DRAFT,
        )
        response = self.client.get(draft.get_absolute_url())
        self.assertEqual(response.status_code, 404)


class PostShareViewTest(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(username='ivan', password='secret123')
        self.post = Post.objects.create(
            author=self.author,
            title='Test Post',
            slug='test-post',
            body='text',
            status=Post.Status.PUBLISHED,
        )
        self.url = reverse('blog:post_share', kwargs={'pk': self.post.pk})

    def test_get_share_form(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/share.html')

    def test_valid_share_sends_email(self):
        response = self.client.post(
            self.url,
            {
                'name': 'Ivan',
                'email': 'ivan@example.com',
                'to': 'friend@example.com',
                'comments': 'Check this out',
            },
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(self.post.title, mail.outbox[0].subject)
        self.assertRedirects(response, self.url)


class PostCommentViewTest(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(username='ivan', password='secret123')
        self.post = Post.objects.create(
            author=self.author,
            title='Test Post',
            slug='test-post',
            body='text',
            status=Post.Status.PUBLISHED,
        )
        self.url = reverse('blog:post_comment', kwargs={'pk': self.post.pk})

    def test_valid_comment_is_created(self):
        response = self.client.post(
            self.url,
            {
                'name': 'Petr',
                'email': 'petr@example.com',
                'body': 'Great article',
            },
        )
        self.assertEqual(self.post.comments.count(), 1)
        self.assertRedirects(response, self.post.get_absolute_url())

    def test_get_not_allowed(self):
        """View помечен @require_POST — GET запрещён."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)
