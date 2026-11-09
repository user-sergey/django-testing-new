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
    cases = (
        (home_url, client.get, OK),
        (detail_url, client.get, OK),
        (login_url, client.get, OK),
        (signup_url, client.get, OK),
        (edit_url, author_client.get, OK),
        (delete_url, author_client.get, OK),
        (edit_url, not_author_client.get, NOT_FOUND),
        (delete_url, not_author_client.get, NOT_FOUND),
        (logout_url, not_author_client.post, OK),
        (edit_url, client.get, FOUND),
        (delete_url, client.get, FOUND),
    )
    for url, client_method, response_code in cases:
        with subtests.test(url=url, client_method=client_method):
            response = client_method(url)
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
        with subtests.test(url=url):
            response = client.get(url)
            assertRedirects(response, redirect_url)
