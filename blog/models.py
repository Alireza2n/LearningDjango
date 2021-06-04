from django.db import models


class Post(models.Model):
    """
    Represents a single blog post
    """
    created_date = models.DateTimeField(verbose_name='تاریخ ایجاد', auto_now_add=True)
    creator = models.ForeignKey('auth.User', verbose_name='کاربر', on_delete=models.PROTECT)
    content = models.TextField(verbose_name='متن', null=True)
    title = models.CharField(max_length=100, verbose_name='عنوان پست')
    intro_image = models.ImageField(verbose_name='عکس مقدمه پست', blank=True, null=True)
    likes = models.IntegerField(default=0)
    categories = models.ManyToManyField('blog.Category')

    class Meta:
        ordering = ('title',)
        verbose_name = 'پست'
        verbose_name_plural = 'پست ها'

    def __str__(self):
        return f'{self.title}'


class Category(models.Model):
    """
    Categories for posts
    """
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=20, unique=True, null=False, blank=False)

    class Meta:
        permissions = []
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    def __str__(self):
        return self.name
