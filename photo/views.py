from django.core.checks import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, DeleteView, UpdateView, DetailView

import photo
from photo.models import Photo, Comment


def photo_list(request):
    photos=Photo.objects.all()
    return render(request, 'photo/list.html', {'photos':photos})

class PhotoDetailView(DetailView):
    model = Photo
    template_name = 'photo/detail.html'

class PhotoUploadView(CreateView):
    model=Photo
    fields=['title', 'photo', 'text']
    template_name = 'photo/upload.html'
    def form_valid(self, form):
        form.instance.author_id=self.request.user.id
        if form.is_valid():
            form.instance.save()
            return redirect('photo:photo_list')
        else:
            return self.render_to_response({'form':form})

class PhotoDeleteView(DeleteView):
    model=Photo
    success_url='/'
    template_name='photo/delete.html'


class PhotoUpdateView(UpdateView):
    model=Photo
    fields=['title','photo', 'text']
    template_name='photo/update.html'


