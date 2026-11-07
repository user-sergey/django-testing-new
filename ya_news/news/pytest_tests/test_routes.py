from http import HTTPStatus

import pytest


@pytest.mark.django_db
@pytest.mark.parametrize(
    ('url_fixture', 'client_name', 'response_code', 'method_name'),
    (
        ('home_url', 'client', HTTPStatus.OK, 'GET'),
        ('detail_url', 'client', HTTPStatus.OK, 'GET'),
        ('login_url', 'client', HTTPStatus.OK, 'GET'),
        ('signup_url', 'client', HTTPStatus.OK, 'GET'),
        ('edit_url', 'author_of_comment_client', HTTPStatus.OK, 'GET'),
        ('delete_url', 'author_of_comment_client', HTTPStatus.OK, 'GET'),
        ('edit_url', 'not_author_client', HTTPStatus.NOT_FOUND, 'GET'),
        ('delete_url', 'not_author_client', HTTPStatus.NOT_FOUND, 'GET'),
        ('logout_url', 'not_author_client', HTTPStatus.OK, 'POST'),
    )
)
def test_pages_availability(
    request,
    url_fixture,
    client_name,
    response_code,
    method_name
):
    url = request.getfixturevalue(url_fixture)
    current_client = request.getfixturevalue(client_name)
    response = current_client.generic(method_name, url)
    assert response.status_code == response_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    ('redirect_fixture_name', 'url_fixture_name', 'client_name'),
    (
        ('anonymous_redirect_urls', 'edit_url', 'client'),
        ('anonymous_redirect_urls', 'delete_url', 'client'),
    )
)
def test_user_is_redirected(
    request,
    redirect_fixture_name,
    url_fixture_name,
    client_name
):
    redirect_urls = request.getfixturevalue(redirect_fixture_name)
    url = request.getfixturevalue(url_fixture_name)
    current_client = request.getfixturevalue(client_name)
    response = current_client.get(url)
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == redirect_urls[url_fixture_name]
