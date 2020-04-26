import markdown
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category, Tag
import re
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.db.models import Q

# 覆写类函数
class IndexView(ListView):
    model = Post
    template_name = 'blogs/index.html'
    context_object_name = 'post_list'
    paginate_by = 5

# 创建日期归档视图
class ArchiveView(IndexView):
    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(ArchiveView, self).get_queryset().filter(creat_time__year = year,creat_time__month=month)

# 创建分类视图
class CategoryView(IndexView):
    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)


# 创建标签视图
class TagView(IndexView):
    def get_queryset(self):
        t = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tag=t)


class PostDetailView(DetailView):
    model = Post
    template_name = 'blogs/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        self.object.increase_views()
        return response
    
    def get_object(self, queryset=None):
        post = super().get_object(queryset=None)
        md = markdown.Markdown(
            extensions = [
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                TocExtension(slugify=slugify)
        ])
        post.body = md.convert(post.body)
        m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
        post.toc = m.group(1) if m is not None else ''
        # post.toc=md.toc
        return post


def search(request):
    q = request.GET.get('q')
    if not q:
        error_msg="请输入搜索关键词"
        messages.add_message(request, messages.ERROR, error_msg, extra_tags='danger')
        return redirect('blogs:index')

    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render(
        request, 'blogs/index.html', {'post_list': post_list})