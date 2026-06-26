from django.contrib.auth import get_user_model
from django.test import TestCase

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
