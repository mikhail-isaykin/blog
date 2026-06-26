from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from blog.models import Post

User = get_user_model()


class PostListAPITest(APITestCase):
    def setUp(self):
        self.author = User.objects.create_user(username='ivan', password='secret123')
        self.url = reverse('blog_api:post_list')
        Post.objects.create(
            author=self.author,
            title='Post 1',
            slug='post-1',
            body='text',
            status=Post.Status.PUBLISHED,
        )

    def test_list_posts_anonymous_allowed(self):
        """GET доступен всем (ReadOnly)."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_requires_authentication(self):
        """Аноним не может создать пост."""
        response = self.client.post(
            self.url,
            {
                'title': 'New',
                'slug': 'new',
                'body': 'text',
            },
        )
        self.assertIn(
            response.status_code,
            (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN),
        )
        self.assertEqual(Post.objects.count(), 1)

    def test_create_post_authenticated(self):
        """Авторизованный создаёт пост."""
        self.client.force_authenticate(user=self.author)
        response = self.client.post(
            self.url,
            {
                'title': 'New Post',
                'slug': 'new-post',
                'body': 'text',
                'author': self.author.id,
                'status': Post.Status.PUBLISHED,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)

    def test_filter_by_author(self):
        other = User.objects.create_user(username='petr', password='x')
        Post.objects.create(
            author=other,
            title='Other',
            slug='other',
            body='text',
            status=Post.Status.PUBLISHED,
        )
        response = self.client.get(self.url, {'author': self.author.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class PostDetailAPITest(APITestCase):
    def setUp(self):
        self.author = User.objects.create_user(username='ivan', password='secret123')
        self.other = User.objects.create_user(username='petr', password='secret123')
        self.post = Post.objects.create(
            author=self.author,
            title='Test',
            slug='test',
            body='text',
            status=Post.Status.PUBLISHED,
        )
        self.url = reverse('blog_api:post_detail', kwargs={'pk': self.post.pk})

    def test_retrieve_post(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test')

    def test_author_can_update(self):
        self.client.force_authenticate(user=self.author)
        response = self.client.patch(self.url, {'title': 'Updated'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated')

    def test_non_author_cannot_update(self):
        """Не автор не может редактировать чужой пост."""
        self.client.force_authenticate(user=self.other)
        response = self.client.patch(self.url, {'title': 'Hacked'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_author_can_delete(self):
        self.client.force_authenticate(user=self.author)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 0)

    def test_non_author_cannot_delete(self):
        self.client.force_authenticate(user=self.other)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Post.objects.count(), 1)


class UserPostListAPITest(APITestCase):
    def setUp(self):
        self.author = User.objects.create_user(username='ivan', password='secret123')
        self.other = User.objects.create_user(username='petr', password='secret123')
        Post.objects.create(
            author=self.author,
            title='Mine',
            slug='mine',
            body='text',
            status=Post.Status.PUBLISHED,
        )
        Post.objects.create(
            author=self.other,
            title='Other',
            slug='other',
            body='text',
            status=Post.Status.PUBLISHED,
        )

    def test_returns_only_user_posts(self):
        url = reverse('blog_api:user_post_list', kwargs={'id': self.author.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Mine')
