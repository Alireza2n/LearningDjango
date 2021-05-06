from django.db import models


class Post(models.Model):
    """
    Represents a single blog post
    """
    created_date = models.DateTimeField(verbose_name='تاریخ ایجاد', auto_now_add=True)
    creator = models.ForeignKey('auth.User', verbose_name='کاربر', on_delete=models.PROTECT)
    content = models.TextField(verbose_name='متن', null=True)
    title = models.CharField(max_length=100, verbose_name='عنوان پست')

    class Meta:
        ordering = ('title',)
        verbose_name = 'پست'
        verbose_name_plural = 'پست ها'

    def __str__(self):
        return f'{self.title}'
