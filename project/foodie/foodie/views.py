from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import RegisterForm
import numpy as np
import nltk
import pandas as pd
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('wordnet')
stop = set(stopwords.words('english'))
stop.update(['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}',''])
from nltk.stem import WordNetLemmatizer
from django.shortcuts import render
food_data = pd.read_csv('food_choices.csv')
def search_comfort(mood):
  lemmatizer = WordNetLemmatizer()
  foodcount = {}
  for i in range(124):
    temp = [temps.strip().replace('.','').replace(',','').lower() for temps in str(food_data["comfort_food_reasons"][i]).split(' ') if temps.strip() not in stop ]
    if mood in temp:
      foodtemp = [lemmatizer.lemmatize(temps.strip().replace('.','').replace(',','').lower()) for temps in str(food_data["comfort_food"][i]).split(',') if temps.strip() not in stop ]
      for a in foodtemp:
        if a not in foodcount.keys():
          foodcount[a] = 1
        else:
          foodcount[a] += 1
  sorted_food = []
  sorted_food = sorted(foodcount, key=foodcount.get, reverse=True)
  return sorted_food
def find_my_comfort_food(mood):
  topn = []
  topn = search_comfort(mood) #function create dictionary only for particular mood
  return topn[:3]
def find_restaurant(mood,request):

  result1, result2, result3 = find_my_comfort_food(mood)
  print(result1)
  return(render(request,'ans.html',{'result1':result1, 'result2':result2, 'result3': result3}))




# Create your views here.
from django.http import HttpResponse




def home_view(request):
    return render(request,'index.html')
def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'signup.html', {'form': form})
def test_view(request):
    return render(request, 'MainPage.html')
def happy(request):
    mood = request.GET.get('mood', '')
    return find_restaurant(mood, request)