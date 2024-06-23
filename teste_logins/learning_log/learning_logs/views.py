from django.shortcuts import render
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.
def index(request):
    """Pg principal do learning_log"""

    return render(request, 'learning_logs/index.html')


def topics(request):
   """mostra os topicos"""

   topics = Topic.objects.order_by('date_added')
   context = {'topics': topics}
   return render(request, 'learning_logs/topics.html', context)


def topic(request, topic_id):
    """mostra os assuntos dos tópicos"""

    topic = Topic.objects.get(id = topic_id)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)


def new_topic(request):
    """Adiciona um novo assunto"""
    if request.method != 'POST':
        # nenhum dado submetido = formulário em branco 
        form = TopicForm()
    else:
        # dados POST submetidos = processa-os
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('topics'))
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


def new_entry(request, topic_id):
    
    topic = Topic.objects.get(id=topic_id)

    """adiciona novo assunto ao topico"""
    if request.method != 'POST':
        # nenhum dado submetido = formulário em branco 
        form = EntryForm()
    else:
        # dados POST submetidos = processa-os
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('topic', args=[topic_id]))
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)


def edit_entry(request, entry_id):
    """edita uma anotação existente"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    if request.method != 'POST':
        # nenhum dado submetido = formulário preenchido com a anotação anterior 
        form = EntryForm(instance=entry)
    else:
        # dados POST submetidos = processa-os
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('topic', args=[topic.id]))
        
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)
