from django.http import HttpResponse
from .models import Publisher, Book, Member, Order

# Create your views here.
def index(request):
    response = HttpResponse()
    booklist = Book.objects.all().order_by('id')[:10]
    heading1 = '<p>' + 'List of available books: ' + '</p>'
    response.write(heading1)
    for book in booklist:
        para = '<p>'+ str(book.id) + ': ' + str(book) + '</p>'
        response.write(para)

    publisherlist = Publisher.objects.all().order_by('-city')
    heading2 = '<br><p>' + 'List of Publishers: ' + '</p>'
    response.write(heading2)
    for publisher in publisherlist:
        para = '<p>'+ str(publisher.name) + ' ' + str(publisher.city) + '</p>'
        response.write(para)

    return response

def about(request):
    return HttpResponse("This is an eBook APP.")

def detail(request, book_id):
    book = Book.objects.get(id=book_id)
    response = HttpResponse()
    title = '<p>' + book.title.upper() + '</p>'
    price = '<p>$' + str(book.price)+ '</p>'
    publisher = '<p>' + book.publisher.name + '</p>'
    response.write(title)
    response.write(price)
    response.write(publisher)
    return response

