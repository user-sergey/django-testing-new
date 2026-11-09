from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects

pytestmark = pytest.mark.django_db

OK = HTTPStatus.OK
FOUND = HTTPStatus.FOUND
NOT_FOUND = HTTPStatus.NOT_FOUND


def test_pages_availability(
    home_url,
    detail_url,
    login_url,
    signup_url,
    edit_url,
    delete_url,
    logout_url,
    client,
    author_client,
    not_author_client,
    subtests
):
    clients = {
        'client': client,
        'author_client': author_client,
        'not_author_client': not_author_client
    }
    cases = (
        (home_url, 'client', OK, 'get'),
        (detail_url, 'client', OK, 'get'),
        (login_url, 'client', OK, 'get'),
        (signup_url, 'client', OK, 'get'),
        (edit_url, 'author_client', OK, 'get'),
        (delete_url, 'author_client', OK, 'get'),
        (edit_url, 'not_author_client', NOT_FOUND, 'get'),
        (delete_url, 'not_author_client', NOT_FOUND, 'get'),
        (logout_url, 'not_author_client', OK, 'post'),
    )
    for url, client_name, response_code, method_name in cases:
        with subtests.test(msg=f'{method_name.upper()} {url} {client_name}'):
            http_method = getattr(clients[client_name], method_name)
            response = http_method(url)
            assert response.status_code == response_code


def test_anonymous_user_is_redirected(
    edit_url,
    delete_url,
    edit_redirect_url,
    delete_redirect_url,
    client,
    subtests
):
    cases = ((edit_url, edit_redirect_url), (delete_url, delete_redirect_url))
    for url, redirect_url in cases:
        with subtests.test(msg=f'Redirect from GET {url}'):
            response = client.get(url)
            assertRedirects(response, redirect_url)
