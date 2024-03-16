from django.shortcuts import render
from django.views.generic import View
from .models import Post

class PostListView(View):
    #Вывод записей
    def get(self, request):
        posts = Post.objects.all()
        return render(request, 'blog/blog.html', {'post_list': posts})



