from django.shortcuts import render
from .models import Topic, Entry
from  django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
# Create your views here.
def index(request):

  return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
  topics = Topic.objects.filter(owner=request.user).order_by('date_added')
  context = {'topics': topics}
  return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, id):
  topic = Topic.objects.get(id=id)
  if topic.owner != request.user:
    raise Http404
  entries = topic.entry_set.order_by('-date_added')
  context = {'topic': topic, 'entries': entries}
  return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
  if request.method != 'POST':
    form = TopicForm()
  else:
    form = TopicForm(request.POST)
    if form.is_valid():
      new_topic = form.save(commit=False)
      new_topic.owner = request.user
      new_topic.save()
      return HttpResponseRedirect(reverse('topics'))
  context = {'form': form}
  return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, id):
  topic = Topic.objects.get(id=id)
  if request.method == 'POST':
    form = EntryForm(data=request.POST)
    if form.is_valid():
      new_entry = form.save(commit=False)
      new_entry.topic = topic
      new_entry.save()
      return HttpResponseRedirect(reverse('topic', args=[id]))
  else:
    form = EntryForm()
    
  context = {'topic': topic, 'form': form}
  return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, id):
  entry = Entry.objects.get(id=id)
  topic = entry.topic
  if topic.owner != request.user:
    raise Http404
  if request.method == 'POST':
    form = EntryForm(instance=entry, data=request.POST)
    if form.is_valid():
      form.save()
      return HttpResponseRedirect(reverse('topic', args=[topic.id]))
  else:
    form = EntryForm(instance=entry)
  context = {'form': form, 'entry': entry, 'topic':topic}
  return render(request, 'learning_logs/edit_entry.html', context)