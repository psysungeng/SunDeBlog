from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.utils.html import strip_tags
import markdown

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length = 100)

    class Meta:
        verbose_name = "文章分类"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length = 100)

    class Meta:
        verbose_name = "文章标签"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField('标题',max_length = 70)
    # 博客正文
    body = models.TextField('正文')
    # 文字摘要
    excerpt = models.CharField('摘要',max_length = 200, blank=True)
    creat_time = models.DateTimeField('创建时间', default=timezone.now)
    modified_time = models.DateTimeField('修改时间')
    def save(self, *args, **kwargs):
        self.modified_time = timezone.now()
        md = markdown.Markdown(
            extensions = [
                'markdown.extensions.extra',
                'markdown.extensions.codehilite'
            ]
        )
        self.excerpt = strip_tags(md.convert(self.body))[:50]
        super().save(*args, **kwargs)

    
    views = models.PositiveIntegerField(default=0, editable=False)
    def increase_views(self):
        self.views+=1
        self.save(update_fields=['views'])
    category = models.ForeignKey(Category, verbose_name = '分类' ,on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, verbose_name = '标签' ,blank=True)
    # 这里 User 是从 django.contrib.auth.models 导入的
    author = models.ForeignKey(User, verbose_name = '作者' ,on_delete=models.CASCADE)

    class Meta:
        verbose_name = "文章"
        verbose_name_plural = verbose_name
        ordering = ['-creat_time']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blogs:detail', kwargs={'pk': self.pk})
