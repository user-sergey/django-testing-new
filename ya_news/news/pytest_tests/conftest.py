from datetime import timedelta

import pytest
from django.conf import settings
from django.test import Client
from django.urls import reverse
from django.utils import timezone

from news.models import Comment, News


@pytest.fixture
def author(django_user_model, db):
    return django_user_model.objects.create(username='Автор комментария')


@pytest.fixture
def not_author(django_user_model, db):
    return django_user_model.objects.create(username='Не-автор')


@pytest.fixture
def author_client(author, db):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author, db):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def news(db):
    return News.objects.create(
        title='Тестовая новость',
        text='Содержание тестовой новости'
    )


@pytest.fixture
def comment(news, author, db):
    return Comment.objects.create(
        news=news,
        author=author,
        text='Тестовый комментарий'
    )


@pytest.fixture
def news_set(db):
    News.objects.bulk_create(
        [
            News(
                title=f'Новость №{index + 1}',
                text=f'Содержание тестовой новости №{index + 1}',
                date=timezone.now() - timedelta(days=index)
            )
            for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
        ]
    )


@pytest.fixture
def comments(news, author, db):
    created_comments = Comment.objects.bulk_create(
        Comment(
            news=news,
            author=author,
            text=f'Тестовый комментарий №{index + 1}',
        )
        for index in range(3)
    )
    for index, single_comment in enumerate(created_comments):
        single_comment.created = timezone.now() + timedelta(minutes=index)
        single_comment.save(update_fields=['created'])


@pytest.fixture
def home_url():
    return reverse('news:home')


@pytest.fixture
def detail_url(news):
    return reverse('news:detail', args=[news.id])


@pytest.fixture
def comments_url(detail_url):
    return f'{detail_url}#comments'


@pytest.fixture
def edit_url(comment):
    return reverse('news:edit', args=[comment.id])


@pytest.fixture
def delete_url(comment):
    return reverse('news:delete', args=[comment.id])


@pytest.fixture
def login_url():
    return reverse('users:login')


@pytest.fixture
def edit_redirect_url(edit_url, login_url):
    return f'{login_url}?next={edit_url}'


@pytest.fixture
def delete_redirect_url(delete_url, login_url):
    return f'{login_url}?next={delete_url}'


@pytest.fixture
def logout_url():
    return reverse('users:logout')


@pytest.fixture
def signup_url():
    return reverse('users:signup')
