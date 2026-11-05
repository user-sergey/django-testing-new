from http import HTTPStatus

import pytest


@pytest.mark.parametrize('page', ('home', 'detail', 'login', 'signup'))
def test_public_pages_are_available(client, urls, page):
    response = client.get(urls[page])
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize('page', ('edit', 'delete'))
def test_comment_pages_are_available_to_author(
    author_of_comment_client,
    urls,
    page
):
    response = author_of_comment_client.get(urls[page])
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize('page', ('edit', 'delete'))
def test_comment_pages_are_unavailable_to_other_user(
    other_user_client,
    urls,
    page
):
    response = other_user_client.get(urls[page])
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.parametrize('page', ('edit', 'delete'))
def test_anonymous_user_is_redirected_to_login(client, urls, page):
    url = urls[page]
    response = client.get(url)
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == f'{urls["login"]}?next={url}'


def test_logout_accepts_post_request(other_user_client, urls):
    response = other_user_client.post(urls['logout'])
    assert response.status_code == HTTPStatus.OK
    assert '_auth_user_id' not in other_user_client.session
