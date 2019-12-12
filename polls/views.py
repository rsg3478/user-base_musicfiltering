from django.views import generic

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import *

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from textblob.classifiers import NaiveBayesClassifier
from eunjeon import Mecab
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import numpy as np



class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def index(request):
  # question 인스턴스들을 불러오는 코드
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    return render(request, 'polls/index.html', {'latest_question_list': latest_question_list})

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "결과를 선택해 주세요!",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def crawling(title, Singer, Songid, content, request, question_id):
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko"}
    html = requests.get("https://www.melon.com/chart/index.htm", headers = header).text
    bs  = BeautifulSoup(html, "html.parser")
     
    aa = []
    for link in bs.find_all("a", {"class": "btn button_icons type03 song_info"}):
        aa.append(link.get('href'))
         
    tr_value = []
    for num in bs.find_all("input", {"class": "input_check"}):
        tr_value.append(num.get('value'))
         
    titles = bs.find_all("div", {"class": "ellipsis rank01"})
    singers = bs.find_all("div", {"class": "ellipsis rank02"})
     
    title = []
    singer = []
    data = []
    
    for tit in titles:
        title.append(tit.find("a").text)
   
    for sing in singers:
        singer.append(sing.find("a").text)
         
    for con in range(100):
        html2 = requests.get("https://www.melon.com/song/detail.htm?songId=" + tr_value[con+1], headers = header).text
        bs2  = BeautifulSoup(html2, "html.parser")
 
        for tag in bs2.select('div[class=lyric]'):
            tag = tag.text.strip()
         
         
        for i in range(1):
            a = i+con+1
            b = title[con]
            c = singer[con]
            d = tr_value[con+1]
            e = tag
            
            songdata = Song(title=b, Singer=c, Songid=d, content=e)
            
            data.append("%3d위 : %s - %s / 곡 id : %s / 가사 : %s"%(a, b, c, d, e))
             
        print(data[con])
#     print(data)
    songdata.save()


# def userinsert(title, Singer, Songid, content, request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     
#     try:
#         selected_userinsert = question.userinsert_set.get(pk=request.POST['userin'])
#     except (KeyError, UserSong.DoesNotExist):
#         # Redisplay the question voting form.
#         return render(request, 'polls/detail.html', {
#             'question': question,
#             'error_message': "평소 즐겨 듣는곡을 골라주세요!",
#         })
#     else:
#         usersongdata = UserSong(title=b, Singer=c, Songid=d, content=e)
#         usersongdata.save()
#         # Always return an HttpResponseRedirect after successfully dealing
#         # with POST data. This prevents data from being posted twice if a
#         # user hits the Back button.
#         return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
#     
    
