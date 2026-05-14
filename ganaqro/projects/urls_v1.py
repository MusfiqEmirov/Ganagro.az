from django.urls import path

from projects.views.views_v1 import (
    HomePageView,
    ProductPageView,
    ProductDetailPageView,
    AboutPageView,
    ContactPageView,
    BlogPageView,
    BlogDetailPageView,
)


app_name = 'projects'

urlpatterns = [
    path(
        '',
        HomePageView.as_view(),
        name='home-page'
    ),
    path(
        'products/',
        ProductPageView.as_view(),
        name='product-page'
    ),
    path(
        'products/<slug:slug>/',
        ProductDetailPageView.as_view(),
        name='product-detail'
    ),
    path(
        'about/',
        AboutPageView.as_view(),
        name='about-page'
    ),
    path(
        'contact/',
        ContactPageView.as_view(),
        name='contact-page'
    ),
    path(
        'blog/',
        BlogPageView.as_view(),
        name='blog-page'
    ),
    path(
        'blog/<int:blog_id>/',
        BlogDetailPageView.as_view(),
        name='blog-detail'
    ),
]
