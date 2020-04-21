from rest_framework import generics, pagination, response
from django.db.models import Q
from .models import Post, Category
from .serializers import CategorySerializer, SimplePostSerializer, PostSerializer


class StanderdResultsSetPagination(pagination.PageNumberPagination):
    page_size = 1

    def get_paginated_response(self, data):
        return response.Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'results': data,
            'page_size': self.page_size,
            'range_first': (self.page.number * self.page_size) - (self.page_size) + 1,
            'range_last': min((self.page.number * self.page_size), self.page.paginator.count),
        })


class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class PostList(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = SimplePostSerializer
    pagination_class = StanderdResultsSetPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        
        keyword = self.request.query_params('keyword',None)
        if keyword:
            queryset = queryset.filter(Q(title__icontains=keyword) | Q(load_text__icontains=keyword) | Q(main_text__icontains=keyword))
        
        cateogry = self.request.query_params.get('category',None)
        if cateogry:
            queryset = queryset.filter(cateogry=cateogry)
        return queryset


class PostDetail(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
