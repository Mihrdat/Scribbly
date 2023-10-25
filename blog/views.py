from django.shortcuts import get_object_or_404
from django.db import transaction
from django.db.models.aggregates import Count

from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
)
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import Author, Category, Article, ArticleImage, ArticleLike
from .serializers import (
    AuthorSerializer,
    CategorySerializer,
    ArticleSerializer,
    ArticleCreateUpdateSerializer,
    ArticleImageSerializer,
    ArticleLikeSerializer,
)
from .permissions import IsOwnerOrReadOnly


class AuthorViewSet(
    ListModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet
):
    queryset = Author.objects.select_related("user").all()
    serializer_class = AuthorSerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.annotate(articles_count=Count("articles")).all()
    serializer_class = CategorySerializer


class ArticleViewSet(ModelViewSet):
    queryset = (
        Article.objects.select_related("category").prefetch_related("images").all()
    )
    serializer_class = ArticleSerializer

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            self.serializer_class = ArticleCreateUpdateSerializer
        return super().get_serializer_class()


class ArticleImageViewSet(ModelViewSet):
    queryset = ArticleImage.objects.all()
    serializer_class = ArticleImageSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["article_id"] = self.kwargs["article_pk"]
        return context

    def get_queryset(self):
        return super().get_queryset().filter(article_id=self.kwargs["article_pk"])


class ArticleLikeViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    queryset = ArticleLike.objects.select_related("author").all()
    serializer_class = ArticleLikeSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return super().get_queryset().filter(article_id=self.kwargs["article_pk"]).all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["article_id"] = self.kwargs["article_pk"]
        return context

    @transaction.atomic
    def perform_create(self, serializer):
        article = get_object_or_404(Article, pk=self.kwargs["article_pk"])
        article.likes_count += 1
        article.save(update_fields=["likes_count"])
        return super().perform_create(serializer)

    @transaction.atomic
    def perform_destroy(self, serializer):
        article = get_object_or_404(Article, pk=self.kwargs["article_pk"])
        article.likes_count -= 1
        article.save(update_fields=["likes_count"])
        return super().perform_create(serializer)
