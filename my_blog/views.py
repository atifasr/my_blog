from django.core.checks import messages
from django.shortcuts import render
from my_blog.models import *
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator
from django.contrib import messages
# Create your views here.

# home page of my_blog


def home(request):
    if request.method == 'GET':

        entry = Entry.objects.all().order_by('date_added')
        # top_rated = Entry.objects.annotate(
        #     no_of_likes=Count('likes')).order_by('-no_of_likes')[:2]
        pages = Paginator(entry, 6)

        if request.GET.get('page'):
            print('executed')
            page_num = request.GET.get('page')
            page = pages.page(page_num)
        else:
            page = pages.page(1)

        entries = page.object_list

        print(len(entries))
        return render(request, 'base/base.html', {'entries': entries,
                                                  'pages': pages})


def get_article(request):
    if request.method == 'GET':
        filter_ = request.GET.get('id')
        article = Entry.objects.get(id=filter_)
        context = {
            'entry': article}
    return render(request, 'my_blog/article.html', context)


@csrf_exempt
def add_post(request):
    if request.user.is_authenticated:

        if request.method == 'GET':
            context = {
                'choices': Category.objects.all(),
            }

        if request.method == 'POST':
            name = request.POST.get('article_name')
            topic_name = request.POST.get('topic_name')
            category = Category.objects.get(name=topic_name)
            detail = request.POST.get('text')
            picture = request.FILES.get('picture')

            topic = Topic(name=name,
                          user=request.user, article_name=category)
            topic.save()
            entry = Entry.objects.create(
                user=request.user, topic=topic, text=detail, picture=picture)

            entry.save()
            return redirect('/')

        return render(request, 'my_blog/add_post.html', context)
    else:
        return redirect('/login')


@csrf_exempt
def login_admin(request):
    # login form
    if request.method == 'POST':
        username = request.POST.get('username')
        pass_ = request.POST.get('password')
        user = authenticate(request, username=username, password=pass_)
        if user is not None:
            login(request, user)
            # user is authenticated
            return redirect('/')
        else:
            # add a message code here
            messages.add_message(request, messages.INFO, 'wrong credentials')
    return render(request, 'my_blog/login_form.html')


@csrf_exempt
def update_post(request, topic_id):

    # getting topic text and updating
    if request.method == "GET":
        topic_ini = Topic.objects.get(id=topic_id)
        topic_text = Entry.objects.get(topic=topic_ini).text
        context = {
            'topic': topic_ini,
            'text': topic_text
        }
        return render(request, 'my_blog/add_page.html', context)

    else:
        topic_ini = Topic.objects.get(id=topic_id)
        new_entry = Entry.objects.get(topic__id=topic_id)
        topic_ini.article_name = request.POST['topic_name']
        topic_ini.save()
        new_entry.text = request.POST['text']
        new_entry.save()
    return redirect('/dashboard')


def get_categories(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        context = {
            'categories': categories,
        }
        return render(request, 'my_blog/display_categories.html', context)


def get_specifics(request):
    if request.method == 'GET':
        filter_ = request.GET.get('category')
        print(filter_)
        topics = Topic.objects.filter(
            article_name__name__iexact=filter_).order_by('-date_added')

        print(topics)
        context = {
            'specifics': True,
            'topics': topics
        }
        return render(request, 'learning_logs/display_categories.html', context)
