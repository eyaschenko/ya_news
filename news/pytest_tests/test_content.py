import pytest
from django.conf import settings
from django.template import response
from django.urls import reverse

from news.forms import CommentForm


@pytest.mark.django_db
def test_news_count(all_news, author_client):
    url = reverse('news:home')
    response = author_client.get(url)
    object_list = response.context['object_list']
    news_count = object_list.count()
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE

@pytest.mark.django_db
def test_news_order(all_news, client):
    url = reverse('news:home')
    response = client.get(url)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert sorted_dates == all_dates

@pytest.mark.django_db
def test_comments_order(news, client, all_comments):
    detail_url = reverse('news:detail', kwargs={'pk':news.id})
    response = client.get(detail_url)
    assert 'news' in response.context
    news = response.context['news']
    all_comments = news.comment_set.all()
    all_timestamps = [comment.created for comment in all_comments]
    sorted_timestamps = sorted(all_timestamps)
    assert sorted_timestamps == all_timestamps

@pytest.mark.django_db
def test_anonymous_client_has_no_form(news, client):
    detail_url = reverse('news:detail', kwargs={'pk':news.id})
    response = client.get(detail_url)
    assert 'form' not in response.context

@pytest.mark.django_db
def test_authorized_client_has_form(news, author_client):
    detail_url = reverse('news:detail', kwargs={'pk':news.id})
    response = author_client.get(detail_url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)










