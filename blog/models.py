from django.db import models
from django.urls import reverse

"""
Post = [title, slug, content, photo, created_at, views, is_published, categories, tags]

Category = [title, slug]

Tag = [title, slug]

Comment = [post, name, content, created_at]
"""


class Post(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, verbose_name='URL', unique=True)
    content = models.TextField(blank=True)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)
    is_published = models.BooleanField(default=True)
    categories = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='posts')
    tags = models.ManyToManyField('Tag', verbose_name='posts', blank=True)

    def get_absolute_url(self):
        return reverse('post', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class Category(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, verbose_name='URL', unique=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class Tag(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='comments')
    name = models.CharField(max_length=150)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.post.title, self.name)

    class Meta:
        ordering = ['-created_at']