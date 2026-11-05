from http import HTTPStatus

import pytest

from news.models import Comment
from .constants import FORM_DATA, NEW_FORM_DATA


def test_anonymous_user_cannot_create_comment(client, urls):
    comments_before = set(Comment.objects.values_list('pk', flat=True))
    response = client.post(urls['detail'], data=FORM_DATA)
    assert response.status_code == HTTPStatus.FOUND
    assert set(Comment.objects.values_list('pk', flat=True)) == comments_before


def test_authorized_user_can_create_comment(
    news,
    author_of_comment,
    author_of_comment_client,
    urls
):
    existing_ids = set(Comment.objects.values_list('pk', flat=True))
    author_of_comment_client.post(urls['detail'], data=FORM_DATA)
    created_comments = Comment.objects.exclude(pk__in=existing_ids)
    assert created_comments.count() == 1
    comment = created_comments.get()
    assert comment.news == news
    assert comment.author == author_of_comment
    assert comment.text == FORM_DATA['text']


@pytest.mark.parametrize('url_name', ('detail', 'edit', 'delete'))
def test_author_after_action_with_comment_redirect_to_news_detail(
    author_of_comment_client,
    urls,
    url_name
):
    url = urls[url_name]
    response = author_of_comment_client.post(url, data=FORM_DATA)
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == urls['detail'] + '#comments'


def test_authorized_user_cannot_create_comment_with_stop_words(
    author_of_comment_client,
    urls
):
    comments_before = set(Comment.objects.values_list('pk', flat=True))
    response = author_of_comment_client.post(
        urls['detail'],
        data={'text': 'Этот негодяй съев вся редиска!!!'}
    )
    assert response.status_code == HTTPStatus.OK
    form = response.context['form']
    assert 'text' in form.errors
    assert 'Не ругайтесь!' in form.errors['text']
    assert set(Comment.objects.values_list('pk', flat=True)) == comments_before


def test_author_of_comment_can_edit_comment(
    news,
    comment,
    author_of_comment,
    author_of_comment_client,
    urls
):
    author_of_comment_client.post(urls['edit'], data=NEW_FORM_DATA)
    updated_comment = Comment.objects.get(pk=comment.pk)
    assert updated_comment.news == news
    assert updated_comment.author == author_of_comment
    assert updated_comment.text == NEW_FORM_DATA['text']


def test_author_of_comment_can_delete_comment(
    comment,
    author_of_comment_client,
    urls
):
    author_of_comment_client.post(urls['delete'])
    assert not Comment.objects.filter(pk=comment.pk).exists()


def test_other_user_cannot_edit_comment(comment, other_user_client, urls):
    response = other_user_client.post(urls['edit'], data=NEW_FORM_DATA)
    saved_comment = Comment.objects.get(pk=comment.pk)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert saved_comment.news == comment.news
    assert saved_comment.author == comment.author
    assert saved_comment.text == comment.text


def test_other_user_cannot_delete_comment(comment, other_user_client, urls):
    response = other_user_client.post(urls['delete'])
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.filter(pk=comment.pk).exists()
