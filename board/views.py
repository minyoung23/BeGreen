from django.core.checks import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import CreateView, DeleteView, UpdateView

from board.models import Board

def board_list(request):
    boards=Board.objects.all()
    return render(request, 'board/list.html', {'boards':boards})

class BoardUploadView(CreateView):
    model=Board
    fields=['title', 'photo', 'text']
    template_name = 'board/upload.html'

    def form_valid(self, form):
        form.instance.author_id=self.request.user.id
        if form.is_valid():
            form.instance.save()
            return redirect('board:board_list')
        else:
            return self.render_to_response({'form':form})

class BoardDeleteView(DeleteView):
    model=Board
    success_url='/'
    template_name='board/delete.html'

class BoardUpdateView(UpdateView):
    model=Board
    fields=['title','photo', 'text']
    template_name='board/update.html'