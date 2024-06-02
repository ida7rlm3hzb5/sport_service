from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView

from mainapp.forms import CommentForm, EditArticleForm, ArticleForm
from mainapp.models import Article, Comment


class ArticleListView(ListView):
    model = Article
    template_name = 'mainapp/index.html'
    context_object_name = 'articles'
    paginate_by = 5

    def get_queryset(self):
        return Article.objects.all().order_by('-created_at')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slider'] = True
        return context


class EditArticleView(View):
    def get(self, request, pk):
        article = get_object_or_404(Article, id=pk)
        form = EditArticleForm(instance=article)
        return render(request, 'mainapp/edit_article.html', {'article': article, 'form': form})

    def post(self, request, pk):
        article = get_object_or_404(Article, id=pk)
        article.title = request.POST['title']
        article.content = request.POST['content']
        article.save()
        return redirect(article.get_absolute_url())


class CreateArticleView(View):
    def get(self, request):
        form = ArticleForm()
        return render(request, 'mainapp/create_article.html', {'form': form})

    def post(self, request):
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)  # Создаем статью, не сохраняя ее в базу данных
            article.author = request.user  # Устанавливаем текущего пользователя как автора статьи
            article.save()  # Теперь сохраняем статью в базу данных с установленным автором
            return redirect('home')  # Предположим, что у вас есть URL с именем 'article_list' для списка статей
        return render(request, 'mainapp/create_article.html', {'form': form})


class DeleteArticleView(View):
    def post(self, request, pk):
        article = get_object_or_404(Article, id=pk)
        article.delete()
        return redirect('home')


class ContactView(View):

    def get(self, request):
        return render(request, 'mainapp/contact.html', {'slider': True})


class AboutView(View):

    def get(self, request):
        return render(request, 'mainapp/about.html', {'slider': True})


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'mainapp/article.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['comments'] = Comment.objects.filter(article=self.get_object()).order_by('-created_at')
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = self.object
            comment.author = request.user
            comment.save()
            return redirect('article', pk=self.object.pk)
        return self.render_to_response(self.get_context_data(comment_form=form))


class CommentDeleteView(View):
    def post(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=kwargs['pk'])
        if request.user == comment.author or request.user.is_superuser:
            comment.delete()
            return redirect('article', pk=comment.article.pk)
        return HttpResponseForbidden()


class NotFoundView(TemplateView):
    template_name = '404_template.html'

    def get(self):
        return render(self.request, self.template_name, status=404)
