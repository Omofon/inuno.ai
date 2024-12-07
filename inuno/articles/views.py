from django.views.generic import ListView, DetailView, TemplateView
from django.shortcuts import get_object_or_404, render
from django.db.models import Q
from django.http import JsonResponse
from .models import Article, Category, SubCategory
from .utils.rss_refresh import refresh_articles


# Home Page
class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["trending_articles"] = Article.objects.filter(trending=True).order_by(
            "-published_date"
        )[:6]
        context["categories"] = Category.objects.all()[:8]
        context["editors_pick"] = Article.objects.filter(editors_pick=True).order_by(
            "-published_date"
        )[:4]
        context["major_categories"] = Category.objects.all()[:5]
        return context


# Refresh RSS Articles
def refresh_rss_view(request):
    return refresh_articles(request)


# Articles
class ArticleListView(ListView):
    model = Article
    template_name = "news/article_list.html"
    context_object_name = "articles"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        category_slug = self.request.GET.get("category")
        subcategory_slug = self.request.GET.get("subcategory")
        trending = self.request.GET.get("trending")
        editors_pick = self.request.GET.get("editors_pick")
        search_query = self.request.GET.get("search")

        # Filter by category
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        # Filter by subcategory
        if subcategory_slug:
            queryset = queryset.filter(sub_category__slug=subcategory_slug)

        # Filter by trending
        if trending:
            queryset = queryset.filter(trending=True)

        # Filter by editor's pick
        if editors_pick:
            queryset = queryset.filter(editors_pick=True)

        # Search
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query)
                | Q(content__icontains=search_query)
                | Q(category__name__icontains=search_query)
                | Q(sub_category__name__icontains=search_query)
            )

        return queryset


class ArticleDetailView(DetailView):
    model = Article
    template_name = "news/article_detail.html"
    context_object_name = "article"


# Categories
class ArticlesByCategoryView(ListView):
    model = Article
    template_name = "news/articles_by_category.html"
    context_object_name = "articles"
    paginate_by = 9

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs["slug"])
        return Article.objects.filter(category=self.category).order_by(
            "-published_date"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.category
        return context


class ArticlesBySubCategoryView(ListView):
    model = Article
    template_name = "news/articles_by_subcategory.html"
    context_object_name = "articles"
    paginate_by = 10

    def get_queryset(self):
        subcategory = get_object_or_404(SubCategory, slug=self.kwargs["slug"])
        return Article.objects.filter(sub_category=subcategory)


class TrendingArticlesView(ListView):
    model = Article
    template_name = "news/trending_articles.html"
    context_object_name = "articles"
    queryset = Article.objects.filter(trending=True)
    paginate_by = 10


class EditorsPickArticlesView(ListView):
    model = Article
    template_name = "news/editors_pick_articles.html"
    context_object_name = "articles"
    queryset = Article.objects.filter(editors_pick=True)
    paginate_by = 10
