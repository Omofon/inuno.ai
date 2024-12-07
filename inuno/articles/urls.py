from django.urls import path
from .views import (
    HomePageView,
    refresh_rss_view,
    ArticleListView,
    ArticleDetailView,
    ArticlesByCategoryView,
    ArticlesBySubCategoryView,
    TrendingArticlesView,
    EditorsPickArticlesView,
)

app_name = "news"

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("articles/", ArticleListView.as_view(), name="article_list"),
    path("articles/<slug:slug>/", ArticleDetailView.as_view(), name="article_detail"),
    path(
        "category/<slug:slug>/",
        ArticlesByCategoryView.as_view(),
        name="articles_by_category",
    ),
    path(
        "subcategory/<slug:slug>/",
        ArticlesBySubCategoryView.as_view(),
        name="articles_by_subcategory",
    ),
    path(
        "articles/trending/", TrendingArticlesView.as_view(), name="trending_articles"
    ),
    path(
        "articles/editors-pick/",
        EditorsPickArticlesView.as_view(),
        name="editors_pick_articles",
    ),
    path("refresh-rss/", refresh_rss_view, name="refresh_rss"),
]
