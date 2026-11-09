from http import HTTPStatus

from pytest_django.asserts import assertRedirects

from news.models import Comment

FORM_DATA = {'text': 'Новый комментарий'}
STOP_WORDS = ('редиска', 'негодяй')
BAD_WORDS_FORM_DATA = {'text': f'Проверка стоп-слова: {STOP_WORDS[0]}'}
WARNING = 'Не ругайтесь!'


def test_anonymous_user_cannot_create_comment(client, detail_url):
    response = client.post(detail_url, data=FORM_DATA)
    assert response.status_code == HTTPStatus.FOUND
    assert Comment.objects.count() == 0


def test_authorized_user_can_create_comment(
    news,
    author,
    author_client,
    detail_url,
    comments_url
):
    response = author_client.post(detail_url, data=FORM_DATA)
    assertRedirects(response, comments_url)
    assert Comment.objects.count() == 1
    comment = Comment.objects.get()
    assert comment.news == news
    assert comment.author == author
    assert comment.text == FORM_DATA['text']


def test_authorized_user_cannot_create_comment_with_stop_words(
    author_client,
    detail_url
):
    response = author_client.post(
        detail_url,
        data=BAD_WORDS_FORM_DATA
    )
    assert response.status_code == HTTPStatus.OK
    form = response.context.get('form')
    assert 'text' in form.errors
    assert WARNING in form.errors['text']
    assert Comment.objects.count() == 0


def test_author_can_edit_comment(
    comment,
    author_client,
    edit_url,
    comments_url
):
    response = author_client.post(edit_url, data=FORM_DATA)
    assertRedirects(response, comments_url)
    updated_comment = Comment.objects.get(pk=comment.pk)
    assert updated_comment.news == comment.news
    assert updated_comment.author == comment.author
    assert updated_comment.text == FORM_DATA['text']


def test_author_can_delete_comment(
    comment,
    author_client,
    delete_url,
    comments_url
):
    response = author_client.post(delete_url)
    assertRedirects(response, comments_url)
    assert Comment.objects.count() == 0


def test_not_author_cannot_edit_comment(comment, not_author_client, edit_url):
    response = not_author_client.post(edit_url, data=FORM_DATA)
    assert response.status_code == HTTPStatus.NOT_FOUND
    saved_comment = Comment.objects.get(pk=comment.pk)
    assert saved_comment.news == comment.news
    assert saved_comment.author == comment.author
    assert saved_comment.text == comment.text


def test_not_author_cannot_delete_comment(
    comment,
    not_author_client,
    delete_url
):
    response = not_author_client.post(delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.filter(pk=comment.pk).exists()
    comment_from_db = Comment.objects.get(pk=comment.pk)
    assert comment_from_db.news == comment.news
    assert comment_from_db.author == comment.author
    assert comment_from_db.text == comment.text
