import datetime
from datetime import timedelta

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import render, get_object_or_404
from myproject.myapp2.models import Order, User,


from .models import Author, Post

# Create your views here.

def hello(request):
    return HttpResponse('Hellow world from function')

class HelloView(View):
    def get(self, request):
        return HttpResponse('Hello world from class')

def year_post(request, year):
    text =""
    ... # формируем статься за год
    return HttpResponse(f'Posts from {year}<br>{text}')

class MonthPost(View):
    def get(self, request, year, month):
        text = ''
        ... # формируем статьи за месяц или за год
        return HttpResponse(f'Posts from {month} / {year} <br> {text}')

def post_detail(request, year, month, slug):
    ...# формируем статьи за год и месяц по индентификатору
    # пока обойдемся без запросов к бд

    post = {
        "year":year,
        "month":month,
        "slug": slug,
        "title": "что быстрее созадет списки в Python: list() или []",
        "content": "Задумались какой способ создания списков работает быстрее..."
    }
    return JsonResponse(post, json_dumps_params={"ensure_ascii": False})

def my_view(request):
    context = {"name": "John"}
    return render(request, "myapp3/my_template.html", context)

class TemplIf(TemplateView):
    template_name = "myapp3/templ_if.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'Привет Мир'
        context['number'] = 5
        return context

def view_for(request):
    my_list = ['apple', 'banana', 'orange']
    my_dict = {
    'каждый': 'красный',
    'охотник': 'оранжевый',
    'желает': 'жёлтый',
    'знать': 'зелёный',
    'где': 'голубой',
    'сидит': 'синий',
    'фазан': 'фиолетовый',
}
    context = {'my_list': my_list, 'my_dict': my_dict}
    return render(request, 'myapp3/templ_for.html', context)

def index(request):
    return render(request, "myapp3/index.html")

def about(request):
    return render(request, "myapp3/about.html")


def author_posts(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    posts =Post.objects.filter(author=author).order_by('-id')[:5]
    return render(request, 'myapp3/author_posts.html', {'author':author, 'posts': posts})

def post_full(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'myapp3/post_full.html', {'post':post})

# Домашнее задание

def basket(request, user_id):
    products = []
    user = User.objects.filter(pk=user_id).first()
    orders = Order.objects.filter(customer=user).all()
    for order in orders:
        products.append(order.products.all())
    products.reverse()
    return render(request, 'basket.html', {'user': user, 'orders': orders, 'products': products})


def sorted_basket(request, user_id, days_ago):
    products = []
    now = datetime.now()
    before = now - timedelta(days=days_ago)
    user = User.objects.filter(pk=user_id).first()
    orders = Order.objects.filter(customer=user, date_ordered__range=(before, now)).all()
    for order in orders:
        products.append(order.products.all())
    products.reverse()
    return render(request, 'basket.html', {'user': user, 'orders': orders, 'products': products})
