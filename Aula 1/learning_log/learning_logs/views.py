from django.shortcuts import render
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    """Pg principal do learning_log"""

    return render(request, 'learning_logs/index.html')


@login_required
def topics(request):
   """mostra os topicos"""

   topics = Topic.objects.filter(owner=request.user).order_by('date_added')
   context = {'topics': topics}
   return render(request, 'learning_logs/topics.html', context)


@login_required
def topic(request, topic_id):
    """mostra os assuntos dos tópicos"""
    topic = Topic.objects.get(id = topic_id)
    
    #ve se o topico consta no usuário
    if topic.owner != request.user:
        raise Http404
    
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)


@login_required
def new_topic(request):
    """Adiciona um novo assunto"""
    if request.method != 'POST':
        # nenhum dado submetido = formulário em branco 
        form = TopicForm()
    else:
        # dados POST submetidos = processa-os
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('topics'))
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    
    topic = Topic.objects.get(id=topic_id)

    #ve se o topico consta no usuário
    if topic.owner != request.user:
        raise Http404

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


@login_required
def edit_entry(request, entry_id):
    """edita uma anotação existente"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    #ve se o topico consta no usuário
    if topic.owner != request.user:
        raise Http404

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
