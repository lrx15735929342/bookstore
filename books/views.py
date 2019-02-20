from django.shortcuts import render,redirect,reverse
from books.models import Books
from books.enums import *
# from django.core.urlresolvers import reverse
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_page
from django_redis import get_redis_connection
import logging
logger = logging.getLogger('django.request')
# Create your views here.


# @cache_page(60*15)
def index(request):
    python_new = Books.objects.get_books_by_type(PYTHON,limit=3,sort='new')
    python_hot = Books.objects.get_books_by_type(PYTHON,limit=4,sort='hot')
    javascript_new = Books.objects.get_books_by_type(JAVASCRIPT,limit=3,sort='new')
    javascript_hot = Books.objects.get_books_by_type(JAVASCRIPT,limit=4,sort='hot')
    algorithms_new = Books.objects.get_books_by_type(ALGORITHMS,3,sort='new')
    algorithms_hot = Books.objects.get_books_by_type(ALGORITHMS,4,sort='hot')
    machinelearning_new = Books.objects.get_books_by_type(MACHINELEARNING,3,sort='new')
    machinelearning_hot = Books.objects.get_books_by_type(MACHINELEARNING,4,sort='hot')
    operatingsystem_new = Books.objects.get_books_by_type(OPERATINGSYSTEM,3,sort='new')
    operatingsystem_hot = Books.objects.get_books_by_type(OPERATINGSYSTEM,4,sort='hot')
    database_new = Books.objects.get_books_by_type(DATABASE,3,sort='new')
    database_hot = Books.objects.get_books_by_type(DATABASE,4,sort='hot')

    context = {
        'python_new':python_new,
        'python_hot':python_hot,
        'javascript_new':javascript_new,
        'javascript_hot':javascript_hot,
        'algorithms_new':algorithms_new,
        'algorithms_hot':algorithms_hot,
        'machinelearning_new':machinelearning_new,
        'machinelearning_hot':machinelearning_hot,
        'operatingsystem_new':operatingsystem_new,
        'operatingsystem_hot':operatingsystem_hot,
        'database_new':database_new,
        'database_hot':database_hot,

    }

    logger.info(request.body)

    return render(request,'books/index.html',context)


def detail(request,books_id):
    books = Books.objects.get_books_by_id(books_id=books_id)

    if books is None:
        return redirect(reverse('books:index'))

    books_li = Books.objects.get_books_by_type(type_id=books.type_id,limit=2,sort='new')

    type_title = BOOKS_TYPE[books.type_id]

    if request.session.has_key('islogin'):
        con = get_redis_connection('default')
        key = 'history_%d' % request.session.get('passport_id')
        con.lrem(key,0,books.id)
        con.lpush(key,books.id)
        con.ltrim(key,0,4)

    context = {'books':books, 'books_li':books_li, 'type_title':type_title}

    return render(request,'books/detail.html',context)


def list(request,type_id,page):
    sort = request.GET.get('sort','default')

    if int(type_id) not in BOOKS_TYPE.keys():
        return redirect(reverse('books:index'))

    books_li = Books.objects.get_books_by_type(type_id=type_id,sort=sort)

    paginator = Paginator(books_li,1)
    num_pages = paginator.num_pages
    if page == '' or int(page)>num_pages:
        page = 1
    else:
        page = int(page)

    books_li = paginator.page(page)

    if num_pages < 5:
        pages = range(1,num_pages+1)
    elif page <= 3:
        pages = range(1,6)
    elif num_pages - page <= 2:
        pages = range(num_pages-4,num_pages+1)
    else:
        pages = range(page-2,page+3)

    books_new = Books.objects.get_books_by_type(type_id=type_id,limit=2,sort='new')

    type_title = BOOKS_TYPE[int(type_id)]
    context = {
        'books_li':books_li,
        'books_new':books_new,
        'type_id':type_id,
        'sort':sort,
        'type_title':type_title,
        'pages':pages
    }

    return render(request,'books/list.html',context)


















