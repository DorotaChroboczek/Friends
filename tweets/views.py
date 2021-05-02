import random

from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

from .forms import TweetFrom
from .models import Tweet

ALLOWED_HOSTS = settings.ALLOWED_HOSTS


def home_view(request, *args, **kwargs):
    return render(request, 'pages/home.html', context={}, status=200)


def tweet_create_view(request, *args, **kwargs):
    # print('ajax', request.is_ajax())
    form = TweetFrom(request.POST or None)
    next_url = request.POST.get('next') or None
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()

        if request.is_ajax():
            return JsonResponse({}, status=201)

        if next_url is not None and is_safe_url(next_url, ALLOWED_HOSTS):
            return redirect(next_url)
        form = TweetFrom()
    return render(request, 'components/form.html', context={'form': form})


def tweet_list_view(request, *args, **kwargs):
    """
    REST API VIEW
    Consumed by JS or Swift/Java/iOS/Android
    return Json data
    """
    qs = Tweet.objects.all().order_by('-id')
    tweets_list = [{'id': x.id, 'content': x.content, 'likes': random.randint(0, 999)} for x in qs]
    data = {
        'isUser': False,
        'response': tweets_list
    }
    return JsonResponse(data)


def tweet_detail_view(request, tweet_id, *args, **kwargs):
    """
    REST API VIEW
    Consumed by JavaScript / Swift / iOS / Android
    return Json data
    """
    data = {
        'id': tweet_id,
    }
    status = 200
    try:
        tweet = Tweet.objects.get(id=tweet_id)
        data.update({'content': tweet.content})
    except:
        data.update({'message': 'Not found'})
        status = 404

    return JsonResponse(data, status=status)
