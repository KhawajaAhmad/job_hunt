from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email: str, password: str, role="job_hunter", **extra_fields) -> object:
        """
        Creates and saves a User with the given email and password.
        :param email: email
        :param password: password
        :param extra_fields: extra fields
        :return: user
        """
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, role=role, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email: str, password: str, **extra_fields) -> object:
        """
        Creates and saves a user with the given email and password.
        :param email: email
        :param password: password
        :param extra_fields: extra fields
        :return: user
        """
        return self._create_user(email, password, **extra_fields)

    def createsuperuser(self, email: str, password: str, **extra_fields) -> object:
        """
        Creates and saves a superuser with the given email and password.
        :param email: email
        :param password: password
        :param extra_fields: extra fields
        :return: superuser
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(email, password, role="admin", **extra_fields)
