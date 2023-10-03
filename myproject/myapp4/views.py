import logging
from datetime import datetime

from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from .forms import UserForm, ManyFieldsForm, ManyFieldsFormWidget, ImageForm
from .models import User

# Create your views here.

logger = logging.getLogger(__name__)


def user_form(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            age = form.cleaned_data['age']
            # Что делаем с данными
            logger.info(f'Получили {name=}, {email=}, {age=}.')
    else:
        form = UserForm()
    return render(request, 'myapp4/user_form.html', {'form': form})


def many_fields_form(request):
    if request.method == "POST":
        form = ManyFieldsFormWidget(request.POST)
        if form.is_valid():
            # Делаем что-то с данными
            logger.info(f'Получили {form.cleaned_data=}.')
    else:
        form = ManyFieldsFormWidget()
    return render(request, 'myapp4/many_fields_form.html', {'form': form})


def add_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        message = 'Ошибка в данных'
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            age = form.cleaned_data['age']
            logger.info(f'Получили {name=}, {email=}, {age=}.')
            user = User(name=name, email=email, age=age)
            user.save()
            message = 'Пользователь сохранён'
    else:
        form = UserForm()
        message = 'Заполните форму'
    return render(request, 'myapp4/user_form.html', {'form': form, 'message': message})


def upload_image(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            fs = FileSystemStorage()
            fs.save(image.name, image)
    else:
        form = ImageForm()
    return render(request, 'myapp4/upload_image.html', {'form':
                                                        form})


def product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    products = Product.objects.all()
    return render(request, 'detail.html', {'product': product, 'products': products})


def products(request):
    logger.info(f'{request} request received')
    products = Product.objects.all()
    return render(request, 'catalog.html', {'products': products})


def prod_edit(request):
    logger.info(f'{request} request received')
    if request.method == 'POST':
        form = Form6(request.POST, request.FILES)
        if form.is_valid():
            name = form.data['name']
            description = form.data['description']
            price = form.data['price']
            prod_quant = form.data['prod_quant']
            product_id = form.data['product']
            product = Product.objects.filter(id=product_id).first()
            img = request.FILES['img']
            fs = FileSystemStorage()
            fs.save(img.name, img)
            product.img = img.name
            product.name = name
            product.description = description
            product.price = price
            product.prod_quant = prod_quant
            product.save()
            return render(request, 'prod_edit.html', {'answer': "Обновлено!"})
    else:
        form = Form6()
    return render(request, 'prod_edit.html', {'form': form})


def upload_image(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            fs = FileSystemStorage()
            fs.save(image.name, image)
            return render(request, 'upload_image.html', {'answer': "Uploaded!"})
    else:
        form = ImageForm()
    return render(request, 'upload_image.html', {'form': form})


def united(request, n):
    context = {'ht': [],
               'd': [],
               'r': []}
    while n > 0:
        context['ht'].append(random.choice(['Орел', 'Решка']))
        context['d'].append(random.randint(1, 6))
        context['r'].append(random.randint(1, 100))
        n -= 1
    return render(request, 'united.html', context)


def heads_tails(request, n):
    context = {'res': []}
    while n > 0:
        context['res'].append(random.choice(['Орел', 'Решка']))
        n -= 1
    return render(request, 'playya.html', context)


def dice(request, n):
    context = {'res': []}
    while n > 0:
        context['res'].append(random.randint(1, 6))
        n -= 1
    return render(request, 'playya.html', context)


def rand(request, n):
    context = {'res': []}
    while n > 0:
        context['res'].append(random.randint(1, 100))
        n -= 1
    return render(request, 'playya.html', context)


def home(request):
    context = {'home': 'Homepage'}
    logger.info(f'{request} request received')
    return render(request, 'homepage.html', context)


def about(request):
    context = {'about': 'About me'}
    logger.info(f'{request} request received')
    return render(request, 'about.html', context)


def author_posts(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    posts = Post.objects.filter(author=author).order_by('-id')[:10]
    return render(request, 'author_posts.html', {'author': author, 'posts': posts})


def post_full(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.showed += 1
    post.save()
    return render(request, 'post_full.html', {'post': post, 'counter': post.showed})


def post_comm(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = Comment.objects.filter(post=post).all()
    post.showed += 1
    post.save()
    return render(request, 'post_comment.html', {'post': post, 'comments': comments, 'counter': post.showed})


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
    return render(request, 'sorted_basket.html', {'user': user, 'orders': orders, 'products': products})