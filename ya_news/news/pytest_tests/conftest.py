from datetime import timedelta

import pytest
from django.conf import settings
from django.test import Client
from django.urls import reverse
from django.utils import timezone

from news.models import Comment, News


@pytest.fixture
def author_of_comment(django_user_model, db):
    return django_user_model.objects.create(username='Автор комментария')


@pytest.fixture
def not_author(django_user_model, db):
    return django_user_model.objects.create(username='Не-автор')


@pytest.fixture
def author_of_comment_client(author_of_comment, db):
    client = Client()
    client.force_login(author_of_comment)
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
def comment(news, author_of_comment, db):
    return Comment.objects.create(
        news=news,
        author=author_of_comment,
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
def comments(news, author_of_comment, db):
    created_comments = Comment.objects.bulk_create(
        [
            Comment(
                news=news,
                author=author_of_comment,
                text=f'Тестовый комментарий №{index + 1}',
            )
            for index in range(3)
        ]
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
    return detail_url + '#comments'


@pytest.fixture
def delete_url(comment):
    return reverse('news:delete', args=[comment.id])


@pytest.fixture
def edit_url(comment):
    return reverse('news:edit', args=[comment.id])


@pytest.fixture
def login_url():
    return reverse('users:login')


@pytest.fixture
def anonymous_redirect_urls(delete_url, edit_url, login_url):
    return {
        'edit_url': f'{login_url}?next={edit_url}',
        'delete_url': f'{login_url}?next={delete_url}'
    }


@pytest.fixture
def logout_url():
    return reverse('users:logout')


@pytest.fixture
def signup_url():
    return reverse('users:signup')
