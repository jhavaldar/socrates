from django.shortcuts import render, redirect, get_object_or_404
from .models import Exercise, Entry, SScore
from django.utils import timezone
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from .lsa import LSA
import os.path
import sys
from django.http import JsonResponse

@login_required
def graph(request):
    entries = Entry.objects.filter(user_name=request.user).all()
    exercise_streak = 0
    meditation_streak = 0
    # Calculate longest exercise streak!
    i = len(entries) - 1
    while (entries[i].exercise is not None):
        i -=1
        exercise_streak += 1
    j = len(entries) - 1
    while (entries[i].meditation):
        j -=1
        meditation_streak += 1
    print >> sys.stderr, exercise_streak
    print >> sys.stderr, meditation_streak
    return render(request, 'graph.html', {'e_streak': exercise_streak, 'm_streak': meditation_streak})

@login_required
def get_data(request, num_items=21):
    entries = Entry.objects.filter(user_name=request.user).all()[:num_items]
    data = []
    for entry in entries:
        dict = {}
        score = entry.score
        dict['angry'] = score.angry
        dict['sad'] = score.sad
        dict['date'] = entry.date
        data.append(dict)
    # Calculate the longest streak of exercise
    i = len(entries)
    return JsonResponse(data, safe=False)

@login_required
def post_list(request):
    user_name = request.user.username
    posts = Entry.objects.filter(date__lte=timezone.now()).filter(user_name=user_name).order_by('date')
    return render(request, 'post_list.html', {'posts': posts})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user_name = request.user.username
            # Save the exercise data as an exercise object
            exercise = None
            if(cd['did_exercise']):
                exercise = Exercise(description = cd['exercise_description'], exercise_type=cd['exercise_type'])
            else:
                exercise = Exercise(description = cd['exercise_description'])
            exercise.save()

            # Add in meditation time
            meditation_time = 0.0
            if(cd['meditation']):
                meditation = cd['meditation_time']

            BASE = os.path.dirname(os.path.abspath(__file__))
            model = LSA(BASE+'/test/', BASE+'/emotions.json')
            scores = model.get_sentiment(cd['mood'])

            score_entry = SScore(angry=scores['angry'], sad=scores['sad'])
            score_entry.save()
            entry = Entry(date=timezone.now(), sleep=cd['sleep'], mood=cd['mood'],
                mood_number=cd['mood_number'], meditation=cd['meditation'], meditation_time=cd['meditation_time'], exercise=exercise,
                score=score_entry)
            entry.user_name = user_name
            entry.save()
            # Redirect to corresponding entry detail page
            return redirect('socrates:post_detail', pk=entry.pk)
    else:
        form = PostForm()
    return render(request, 'post_edit.html', {'form': form})

@login_required
def post_detail(request, pk):
    post = get_object_or_404(Entry, pk=pk)
    return render(request, 'post_detail.html', {'post': post})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Entry, pk=pk)
    if post:
        post.delete()
    user_name = request.user.username
    posts = Entry.objects.filter(date__lte=timezone.now()).filter(user_name=user_name).order_by('date')
    return render(request, 'post_list.html', {'posts': posts})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Entry, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user_name = request.user.username

            exercise = post.exercise
            if(cd['did_exercise']):
                if not exercise:
                    exercise = Exercise(description=cd['exercise_description'], exercise_type=cd['exercise_type'])
                exercise.description = cd['exercise_description']
                exercise.exercise_type = cd['exercise_type']
                exercise.save()
                post.exercise = exercise
            else:
                if post.exercise:
                    post.exercise = None
                    exercise.delete()

            # Add in meditation time
            meditation_time = 0.0
            if(cd['meditation']):
                meditation = cd['meditation_time']

            BASE = os.path.dirname(os.path.abspath(__file__))
            model = LSA(BASE+'/test/', BASE+'/emotions.json')
            scores = model.get_sentiment(cd['mood'])

            score_entry = post.score
            score_entry.angry = scores['angry']
            score_entry.sad = scores['sad']
            score_entry.save()

            entry = post
            entry.sleep = cd['sleep']
            entry.mood = cd['mood']
            entry.mood_number = cd['mood_number']
            entry.meditation = cd['meditation']
            if cd['meditation']:
                entry.meditation_time = cd['meditation_time']
            entry.score = score_entry
            entry.save()
            return redirect('socrates:post_detail', pk=post.pk)
    else:
        post = get_object_or_404(Entry, pk=pk)
        print >> sys.stderr, post.mood
        data = {}

        data['did_exercise'] = post.exercise
        exercise = post.exercise
        if exercise:
            data['exercise_type'] = exercise.exercise_type
            data['exercise_description'] = exercise.description

        data['sleep'] = post.sleep
        data['meditation'] = post.meditation
        if post.meditation:
            data['meditation_time'] = post.meditation_time

        data['mood'] = post.mood
        data['mood_number'] = post.mood_number

        form = PostForm(data)
    return render(request, 'post_edit.html', {'form': form})
