from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertFormError, assertRedirects

from news.models import Comment
from news.forms import BAD_WORDS, WARNING

@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(news, client, form_data):
    url = reverse('news:detail', kwargs ={'pk':news.id})
    client.post(url, data=form_data)
    comments_count = Comment.objects.count()
    assert comments_count == 0

@pytest.mark.django_db
def test_user_can_create_comment(news, author_client, author, form_data):
    url = reverse('news:detail', kwargs ={'pk':news.id})
    response = author_client.post(url, data=form_data)
    comments_count = Comment.objects.count()
    assert comments_count == 1
    comment = Comment.objects.get()
    assert comment.text== form_data['text']
    assert comment.news == news
    assert comment.author == author

@pytest.mark.django_db
def test_user_cant_use_bad_words(news, author_client, form_data):
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    url = reverse('news:detail', kwargs={'pk': news.id})
    response = author_client.post(url, data=bad_words_data)
    url = reverse('news:detail', kwargs={'pk': news.id})
    assertFormError(response, 'form','text', errors=WARNING)
    comments_count = Comment.objects.count()
    assert comments_count == 0

@pytest.mark.django_db
def test_author_can_delete_comment(news, author_client, comment):
    news_url = reverse('news:detail', kwargs={'pk': news.id})
    url_to_comments = news_url + '#comments'
    delete_url = reverse('news:delete', args=(comment.id,))
    response = author_client.delete(delete_url)
    assertRedirects(response, url_to_comments)

@pytest.mark.django_db
def test_user_cant_delete_comment_of_another_user(news, not_author_client, comment):
    delete_url = reverse('news:delete', args=(comment.id,))
    news_url = reverse('news:detail', kwargs={'pk': news.id})
    url_to_comments = news_url + '#comments'
    response = not_author_client.delete(delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comments_count = Comment.objects.count()
    assert comments_count == 1

@pytest.mark.django_db
def test_author_can_edit_comment(news, comment, author_client, new_form_data):
    edit_url = reverse('news:edit', args=(comment.id,))
    news_url = reverse('news:detail', args=(news.id,))
    url_to_comments = news_url + '#comments'
    response = author_client.post(edit_url, data=new_form_data)
    assertRedirects(response, url_to_comments)
    comment.refresh_from_db()
    assert comment.text == new_form_data['text']









