from django.shortcuts import render
from shop.models import Item
from django.db.models import Q

def searchResult(request):
    items=None
    query=None
    if 'q' in request.GET:
        query=request.GET.get('q')
        items=Item.objects.all().filter(Q(item_name__contains=query)|Q(description__contains=query))

    return render(request, 'search_app/search.html', {'query':query, 'items':items})
# Create your views here.
