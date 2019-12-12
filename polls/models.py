import datetime

from django.db import models
from django.utils import timezone

import requests
from bs4 import BeautifulSoup


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text
    
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text
    
class Song(models.Model):
#     author = models.ForeignKey('auth.User')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    emotion = models.CharField(max_length=50)
    ranking = models.CharField(max_length=10)
    title = models.CharField(max_length=100) # 길이 제한이 있는 문자열
    Singer = models.CharField(max_length=50)
    Songid = models.TextField(max_length=50)
    content = models.TextField()     # 길이 제한이 없는 문자열
    created_at = models.DateTimeField(auto_now_add=True) # 해당 레코드 생성시 현재 시간 자동저장
    updated_at = models.DateTimeField(auto_now=True) # 해당 레코드 갱신시 현재 시간 자동저장
    # DB에서는 길이제한 유무에 따라서 문자열 필드타입이 다른다.
    # 길이 제한이 없는 문자열을 많이 쓰면 성능이 좋지 않다.
    
    def __str__(self):
        return self.title
    
class UserSong(models.Model):
#     author = models.ForeignKey('auth.User')
    emotion = models.CharField(max_length=50)
    ranking = models.CharField(max_length=10)
    title = models.CharField(max_length=100) # 길이 제한이 있는 문자열
    Singer = models.CharField(max_length=50)
    Songid = models.TextField(max_length=50)
    content = models.TextField()     # 길이 제한이 없는 문자열
    created_at = models.DateTimeField(auto_now_add=True) # 해당 레코드 생성시 현재 시간 자동저장
    updated_at = models.DateTimeField(auto_now=True) # 해당 레코드 갱신시 현재 시간 자동저장
    # DB에서는 길이제한 유무에 따라서 문자열 필드타입이 다른다.
    # 길이 제한이 없는 문자열을 많이 쓰면 성능이 좋지 않다.
    
    def __str__(self):
        return self.title
    
    