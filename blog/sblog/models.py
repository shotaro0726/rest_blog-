from django.db import models
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7, default='#000000')

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=40)
    thumbnail = models.ImageField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='カテゴリ')
    load_text = models.TextField()
    main_text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('-created_at',)
    
    def __str__(self):
        return self.title
