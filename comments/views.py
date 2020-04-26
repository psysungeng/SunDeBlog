from django.shortcuts import render, get_object_or_404, redirect
from blogs.models import Post
from django.views.decorators.http import require_POST
from .forms import CommentForm
from django.contrib import messages


# Create your views here.
@require_POST
def comment(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)

    form = CommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        messages.add_message(request, messages.SUCCESS, '成功提交评论!', extra_tags='success')

        return redirect(post)
    
    context = {
        'post': post,
        'form': form
    }
    messages.add_message(request, messages.ERROR, '提交失败，请重新提交!', extra_tags='danger')
    return render(request, 'comments/preview.html', context=context)

