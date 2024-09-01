from django.core.paginator import Paginator
from django.shortcuts import render

from .models import Book


def books_list(request):
    books = Book.objects.all()
    context = {'books': books}
    return render(request, 'books/books_list.html', context)


def books_view(request, pub_date):
    books = Book.objects.filter(pub_date=pub_date)
    dates = Book.objects.all().values_list('pub_date', flat=True).distinct().order_by('pub_date')
    prev_date = None
    next_date = None
    for idx, date in enumerate(dates.iterator()):
        print(str(pub_date), date)
        if str(date) == str(pub_date):
            prev_date = dates[idx - 1] if idx > 0 else None
            next_date = dates[idx + 1] if idx < len(dates) - 1 else None
            break
    context = {
        'books': books,
        'prev_date': prev_date,
        'next_date': next_date,
    }
    return render(request, 'books/books_list.html', context)
