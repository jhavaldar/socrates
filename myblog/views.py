from django.shortcuts import render, redirect, get_object_or_404
from .models import Exercise, Entry
from django.utils import timezone
from .forms import PostForm

# Create your views here.

def post_list(request):
    posts = Entry.objects.filter(date__lte=timezone.now()).order_by('date')
    return render(request, 'post_list.html', {'posts': posts})

def post_new(request):
    form_class = PostForm(request.POST or None)

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            # Save the exercise data as an exercise object
            exercise = None

            if(cd['did_exercise']):
                description = cd['exercise_description']
                type = cd['exercise_type']
                if(cd['exercise_type']=='C'):
                    miles = cd['miles']
                    exercise = Exercise(description=description, miles=miles, exercise_type=type)
                else:
                    exercise = Exercise(description=description, exercise_type=type)

                exercise.save()

            # Add in meditation time
            meditation_time = 0.0

            if(cd['meditation']):
                meditation = cd['meditation_time']

            entry = Entry(date=timezone.now(), calories=cd['calories'], sleep=cd['sleep'], art=cd['art'], mood=cd['mood'],
                mood_number=cd['mood_number'], meditation=cd['meditation'], meditation_time=cd['meditation_time'], exercise=exercise)
            entry.save()
            return redirect('post_detail', pk=entry.pk)
        return render(request, 'post_edit.html', {'form': form_class})

    return render(request, 'post_edit.html', {
        'form': form_class,
    })

def post_detail(request, pk):
    post = get_object_or_404(Entry, pk=pk)
    return render(request, 'post_detail.html', {'post': post})