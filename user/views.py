from django.shortcuts import render
from rest_framework.decorators import api_view


@api_view(['GET', ])
def intro(request):
    return render(request, 'intro.html', {
    })
