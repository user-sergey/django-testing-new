from http import HTTPStatus

from news.forms import CommentForm
from .constants import NEWS_ON_PAGE


def test_news_count_on_page_is_limited(news_set, client, urls):
    response = client.get(urls['home'])
    object_list = response.context['object_list']
    assert len(object_list) == NEWS_ON_PAGE


def test_news_are_sorted_newest_first(news_set, client, urls):
    response = client.get(urls['home'])
    object_list = list(response.context['object_list'])
    expected_news_set = list(reversed(news_set))[:NEWS_ON_PAGE]
    assert object_list == expected_news_set


def test_comments_are_sorted_oldest_first(comments, client, urls):
    response = client.get(urls['detail'])
    object_list = list(response.context['news'].comment_set.all())
    dates_of_comments = [comment.created for comment in object_list]
    assert dates_of_comments == sorted(dates_of_comments)


def test_anonymous_user_has_no_comment_form(client, urls):
    response = client.get(urls['detail'])
    assert response.status_code == HTTPStatus.OK
    assert 'form' not in response.context


def test_authorized_user_has_comment_form(other_user_client, urls):
    response = other_user_client.get(urls['detail'])
    assert response.status_code == HTTPStatus.OK
    assert isinstance(response.context['form'], CommentForm)
