from django.shortcuts import render, get_object_or_404, redirect
# from pip._vendor.requests import request

from .models import Publisher, Book, Member, Order, Review
from django.http import HttpResponse, HttpResponseRedirect
from .forms import SearchForm, OrderForm, ReviewForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
import random
from datetime import datetime
from django.views import View


# Create your views here.
def index(request):
    last_login = "";
    if request.session.has_key('last_login'):
        last_login = request.session['last_login']
    bookdetail = Book.objects.all().order_by('id')[:10]
    return render(request, 'myapp/index.html', {'booklist': bookdetail, 'last_login': last_login})


class IndexView(View):
    template_name = 'myapp/index.html'
    last_login_cookie = 'last_login'

    def get(self, request):
        last_login = ''
        if self.last_login_cookie in request.session.keys():
            last_login = request.session.get(self.last_login_cookie)

        book_list = Book.objects.all().order_by('id')[:10]
        return render(request, self.template_name, {'booklist': book_list, 'last_login': last_login})


def about(request):
    if request.COOKIES.get('lucky_num'):
        mynum = request.COOKIES.get('lucky_num')
    else:
        mynum = random.randint(1, 100)
    response = render(request, 'myapp/about.html', {'mynum': mynum})
    response.set_cookie('lucky_num', mynum, expires=300)
    return response


class DetailView(View):
    template_name = 'myapp/detail.html'

    def get(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        return render(request, self.template_name, {'book': book})


def detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'myapp/detail.html', {'book': book})


def findbooks(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            category = form.cleaned_data['category']
            max_price = form.cleaned_data['max_price']
            if (category):
                booklist = Book.objects.filter(category=category, price__lte=max_price)
            else:
                booklist = Book.objects.filter(price__lte=max_price)
            return render(request, 'myapp/results.html', {'booklist': booklist, 'name': name, 'category': category})
        else:
            return HttpResponse('Invalid data')
    else:
        form = SearchForm()
        return render(request, 'myapp/findbooks.html', {'form': form})


@login_required(login_url='/myapp/login/')
def place_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            books = form.cleaned_data['books']
            order = form.save(commit=False)
            member = get_object_or_404(Member, id=request.user.id)
            order.member = member
            order.save()
            order.books.set(books)
            type = order.order_type
            if type == 1:
                for b in order.books.all():
                    member.borrowed_books.add(b)
            return render(request, 'myapp/order_response.html', {'books': books, 'order': order})
        else:
            return render(request, 'myapp/placeorder.html', {'form': form})
    else:
        form = OrderForm()
        return render(request, 'myapp/placeorder.html', {'form': form})


@login_required(login_url='/myapp/login/')
def review(request):
    member = get_object_or_404(Member, pk=request.user.pk)
    if member.status == 1 or member.status == 2:
        if request.method == 'POST':
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save()
                book = review.book
                book.num_reviews += 1
                book.save()
                review.save()
                return HttpResponseRedirect('/myapp')
        else:
            form = ReviewForm()
        return render(request, 'myapp/review.html', {'form': form})
    else:
        return HttpResponse('You are not eligible to view this page')


def user_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('myapp:index'))
    if request.method == 'POST':
        valuenext = request.POST.get('next')
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                request.session['last_login'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                request.session.set_expiry(3600)
                if valuenext == '':
                    return HttpResponseRedirect(reverse('myapp:index'))
                else:
                    return HttpResponseRedirect(valuenext)
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'myapp/login.html')


@login_required(login_url='/myapp/login/')
def user_logout(request):
    logout(request)
    # request.session['last_login'] = ""
    return HttpResponseRedirect(reverse(('myapp:index')))


@login_required(login_url='/myapp/login/')
def chk_reviews(request, book_id):
    if request.user.is_authenticated:
        book = get_object_or_404(Book, id=book_id)
        reviews = Review.objects.filter(book_id=book_id)
        tot_sum = 0
        tot = 0
        for r in reviews:
            tot_sum += r.rating
            tot += 1
        if tot > 0:
            tot_sum /= tot
            return render(request, 'myapp/chk_reviews.html', {'book': book, 'average_rating': tot_sum})
        else:
            return HttpResponse('No ratings available.')
    # else:
    #     return redirect('myapp/login.html', {'next':'chk_reviews.html/'+str(book_id)})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect('/myapp/login')
    else:
        form = RegisterForm()
    return render(request, 'myapp/register.html', {'form': form})


@login_required(login_url='/myapp/login/')
def my_orders(request):
    try:
        logged_in_user = Member.objects.get(pk=request.user.pk)
        orders = Order.objects.filter(member=logged_in_user)

        book_list = []
        for order in orders:
            books = order.books.all()
            book_title = ''
            for book in books:
                book_title = book_title + book.title + ', '
            book_list.append(book_title[:-2])

        new_list = zip(orders, book_list)

        return render(request, 'myapp/myorders.html', {'orders': orders, 'book_list': book_list, 'new_list': new_list})
    except Member.DoesNotExist:
        return HttpResponse('There are no available orders!')
