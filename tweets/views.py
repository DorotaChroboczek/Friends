from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render

from .models import Tweet


def home_view(request, *args, **kwargs):
    return render(request, 'pages/home.html', context={}, status=200)


def tweet_list_view(request, *args, **kwargs):
    """
    REST API VIEW
    Consumed by JS or Swift/Java/iOS/Android
    return Json data
    """
    qs = Tweet.objects.all()
    tweets_list = [{'id': x.id, 'content': x.content} for x in qs]
    data = {
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