from django.conf import settings

from news.forms import CommentForm

NEWS_ON_PAGE = settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_count_on_page_is_limited(news_set, client, home_url):
    response = client.get(home_url)
    news_items = response.context['object_list']
    assert len(news_items) == NEWS_ON_PAGE


def test_news_are_sorted_newest_first(news_set, client, home_url):
    response = client.get(home_url)
    all_dates = [news.date for news in response.context['object_list']]
    assert all_dates == sorted(all_dates, reverse=True)


def test_comments_are_sorted_oldest_first(comments, client, detail_url):
    response = client.get(detail_url)
    comment_timestamps = [
        comment.created
        for comment in response.context['news'].comment_set.all()
    ]
    assert comment_timestamps == sorted(comment_timestamps)


def test_anonymous_user_has_no_comment_form(client, detail_url):
    response = client.get(detail_url)
    assert 'form' not in response.context


def test_authorized_user_has_comment_form(not_author_client, detail_url):
    response = not_author_client.get(detail_url)
    assert isinstance(response.context.get('form'), CommentForm)
