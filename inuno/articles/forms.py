from django import forms
from .models import Article, Category


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = [
            "title",
            "content",
            "source_url",
            "image_url",
            "published_date",
            "category",
            "trending",
            "editors_pick",
        ]
