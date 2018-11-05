from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

import sys
import pdb

def index(request):
    return render(request, './userData.html')
    # return HttpResponse("Hello, world. You're at prediction app.")

@csrf_exempt
def predict(request):
    print(request.POST)
    # print(request.POST.get("age"))
    for key,value in request.POST.iteritems():
        
        print(key)
        print(value)
    # print >> sys.stderr, request.data
    # return render(request, './pred.html')
    return HttpResponse("Hello, world. You're at prediction app.")