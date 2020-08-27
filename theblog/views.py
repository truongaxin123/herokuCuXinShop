from django.shortcuts import HttpResponse, render, get_object_or_404, Http404, HttpResponseRedirect
from django.urls import reverse
from .models import Article, Tag, get_object_with_view_highest, get_next_or_prev
from .forms import CommentForm


def detail_article(request, slug):
    article = get_object_or_404(Article, slug=slug)
    article.view += 1
    article.save()
    models = Article.objects.all()

    tag_with_view_highest = get_object_with_view_highest(article.tags.all())
    next_article = get_next_or_prev(models, article)
    previous_article = get_next_or_prev(models, article, 'prev')

    comment_form = CommentForm()
    if request.method == 'POST':
        comment_form = CommentForm(request.POST, author=request.user, article=article)
        if comment_form.is_valid():
            comment_form.save()
            return HttpResponseRedirect(request.path)

    context = {'article': article,
               'next_article': next_article,
               'previous_article': previous_article,
               'tag_with_view_highest': tag_with_view_highest,
               'comment_form': comment_form}

    return render(request, 'theblog/view_detail_article.html', context=context)


def detail_tag(request, tag_name):
    tag = get_object_or_404(Tag, tag_name=tag_name)
    tag.view += 1
    tag.save()
    return render(request, 'theblog/view_detail_tag.html', context={'tag': tag})


def list_article(request):
    articles = Article.objects.all()
    if articles.count() == 0:
        return Http404()

    class AllTag:
        tag_name = 'all'
        tag_full_name = 'Tất cả'
    tag = AllTag()
    return render(request, 'theblog/view_list_article.html', context={'tag': tag, 'articles': articles})


def list_tag(request):
    tags = Tag.objects.all()
    return render(request, 'theblog/view_all_tag.html', context={'tags': tags})


def list_article_with_tag(request, tag_name):
    tag = get_object_or_404(Tag, tag_name=tag_name)
    articles = tag.article_set.all()
    return render(request, 'theblog/view_list_article.html', context={'tag': tag, 'articles': articles})


def profile(request):
    return render(request, 'theblog/profile.html')


def joke(request):
    return render(request, 'theblog/joke.html')