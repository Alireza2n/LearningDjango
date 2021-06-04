from django.db import models


class ProductTypes(models.TextChoices):
    """
    Different types of products
    """
    JPEG = 'JPEG', 'عکس با کیفیت معمولی'
    PSD = 'PSD', 'فایل فوتوشاپ'
    AI = 'AI', 'فایل ایلوستریتور'
    TEXT = 'TEXT', 'فایل ورد'
    PRINT = 'PRINT', 'چاپ روی کاغذ'
