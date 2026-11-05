from datetime import timedelta

import pytest
from django.test import Client
from django.urls import reverse
from django.utils import timezone

from news.models import Comment, News
from .constants import NEWS_ON_PAGE


@pytest.fixture
def author_of_comment(django_user_model, db):
    return django_user_model.objects.create(username='Автор комментария')


@pytest.fixture
def other_user(django_user_model, db):
    return django_user_model.objects.create(username='Другой пользователь')


@pytest.fixture
def author_of_comment_client(author_of_comment, db):
    client = Client()
    client.force_login(author_of_comment)
    return client


@pytest.fixture
def other_user_client(other_user, db):
    client = Client()
    client.force_login(other_user)
    return client


@pytest.fixture
def news(db):
    return News.objects.create(
        title='Тестовая новость',
        text='Содержание тестовой новости'
    )


@pytest.fixture
def comment(news, author_of_comment, db):
    return Comment.objects.create(
        news=news,
        author=author_of_comment,
        text='Тестовый комментарий'
    )


@pytest.fixture
def news_set(db):
    return News.objects.bulk_create(
        [
            News(
                title=f'Новость №{index + 1}',
                text=f'Содержание тестовой новости №{index + 1}',
                date=timezone.now() + timedelta(days=index)
            )
            for index in range(NEWS_ON_PAGE + 1)
        ]
    )


@pytest.fixture
def comments(news, author_of_comment, db):
    return Comment.objects.bulk_create(
        [
            Comment(
                news=news,
                author=author_of_comment,
                text=f'Тестовый комментарий №{index + 1}',
                created=timezone.now() + timedelta(minutes=index),
            )
            for index in range(3)
        ]
    )


@pytest.fixture
def urls(news, comment):
    return {
        'home': reverse('news:home'),
        'detail': reverse('news:detail', args=[news.id]),
        'delete': reverse('news:delete', args=[comment.id]),
        'edit': reverse('news:edit', args=[comment.id]),
        'login': reverse('users:login'),
        'logout': reverse('users:logout'),
        'signup': reverse('users:signup'),
    }
