from django.contrib.auth import get_user_model
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
