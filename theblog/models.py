from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from unidecode import unidecode
from datetime import datetime


def get_next_or_prev(models: object, item, direction: str = 'next') -> object:
    getit = False
    if direction == 'prev':
        models = models.reverse()
    for m in models:
        if getit:
            return m
        if item == m:
            getit = True
    if getit:
        # This would happen when the last
        # item made getit True
        return models[0]
    return False


def get_object_with_view_highest(objects):
    result = None
    view = 0
    for __object in objects:
        view_tem = __object.view
        if view_tem > view:
            result = __object
    return result


class Tag(models.Model):
    tag_name = models.CharField(max_length=50)
    tag_full_name = models.CharField(max_length=100, default='Fullname is none')
    pub_date = models.DateTimeField('Public date')
    description = models.TextField()
    view = models.IntegerField(default=0)

    def __str__(self):
        return self.tag_name

    def get_raw_name(self):
        return unidecode(self.tag_full_name)

    def get_number_article(self):
        return len(self.article_set.all())


class Article(models.Model):
    tags = models.ManyToManyField(Tag)
    title = models.CharField(max_length=200)
    thumbnail_image = models.ImageField(upload_to='thumbs', editable=True, blank=True, null=True)
    pub_date = models.DateTimeField('Public date', auto_now_add=True)
    content = RichTextUploadingField(blank=False)
    view = models.IntegerField(default=0)
    last_modify = models.DateTimeField(null=True, auto_now_add=True)
    slug = models.SlugField(max_length=200, default='this-is-slug')

    def __str__(self):
        return self.title

    def get_number(self):
        return len(self.objects.all())

    def get_number_comment(self):
        return len(self.comments.all())

    def get_comment_latest(self):
        return self.comments.all().order_by('-date')

    def save(self, *args, **kwargs):
        self.slug = slugify(unidecode(self.title))
        self.last_modify = datetime.now()
        super().save(*args, **kwargs)


class Comment(models.Model):

    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Article: {} {}'.format(self.article.title, self.author.username)
