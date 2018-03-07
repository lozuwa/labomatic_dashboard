# General purpose
import os
import sys
# Django libraries
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.conf import settings
# Controllers
from . import mController

# Routes to "/"
def index(request):
  return HttpResponse("<html> Labomatic! </html>")

def classifyParasites(request):
  if request.method == "POST":
    myfile = request.FILES["myfile"]
    fs = FileSystemStorage()
    filename = fs.save(myfile.name, myfile)
    paths = mController.classify_file(os.path.join(os.getcwd(), "media", filename))
    return render(request, "ObjectDetection/showImageResult.html", 
    				{"paths": paths})
  elif request.method == "GET":
    return render(request, "ObjectDetection/index.html")
  else:
    return HttpResponse("Method not supported")

def classifyTuberculosis(request):
  if request.method == "POST":
    myfile = request.FILES["myfile"]
    fs = FileSystemStorage()
    filename = fs.save(myfile.name, myfile)
    # classify_file(filename)
    return HttpResponse("Image was uploaded at " + fs.url(filename))
  elif request.method == "GET":
    return render(request, "ObjectDetection/index.html")
  else:
    return HttpResponse("Method not supported")
