from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='ivan', password='secret123')

    def test_profile_created_for_user(self):
        """У созданного пользователя есть профиль."""
        self.assertIsNotNone(self.user.profile)

    def test_str_returns_username(self):
        """__str__ профиля возвращает имя пользователя."""
        self.assertEqual(str(self.user.profile), 'ivan')


class SignUpViewTest(TestCase):
    def setUp(self):
        self.url = reverse('accounts:signup')

    def test_get_returns_signup_page(self):
        """GET-запрос отдаёт страницу регистрации с формой."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup.html')
        self.assertIn('form', response.context)

    def test_valid_signup_creates_user_and_redirects(self):
        """Валидная форма создаёт пользователя и редиректит на список постов."""
        response = self.client.post(
            self.url,
            {
                'username': 'newuser',
                'email': 'new@example.com',
                'password1': 'ComplexPass123',
                'password2': 'ComplexPass123',
            },
        )
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertRedirects(response, reverse('blog:post_list'))

    def test_authenticated_user_is_redirected(self):
        """Залогиненного юзера сразу редиректит, регистрация недоступна."""
        User.objects.create_user(username='ivan', password='secret123')
        self.client.login(username='ivan', password='secret123')
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('blog:post_list'))


class ProfileViewTest(TestCase):
    def setUp(self):
        self.url = reverse('accounts:profile')
        self.user = User.objects.create_user(username='ivan', password='secret123')

    def test_login_required(self):
        """Неавторизованного юзера редиректит на логин."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_profile_page_for_logged_in_user(self):
        """Авторизованный юзер видит страницу профиля с двумя формами."""
        self.client.login(username='ivan', password='secret123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/profile.html')
        self.assertIn('user_form', response.context)
        self.assertIn('profile_form', response.context)
