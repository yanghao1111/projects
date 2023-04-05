"""图书管理系统 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from app01 import views

urlpatterns = [
    path('login/index', views.index),
    path('login/reader', views.reader),
    path('index/student_manage', views.student_manage),
    path('index/reader_info', views.reader_info),
    path('index/borrow', views.borrow),
    path('index/borrow_info', views.borrow_info),
    path('index/<int:nid>/borrow', views.borrow1),
    path('index/<int:nid>/borrow_delete', views.borrow_delete),
    path('login/', views.login),
    path('index/reader_add', views.reader_add),
    path('index/student_manage/reader_add', views.reader_add),
    path('index/reader_list', views.reader_list),
    path('index/<int:nid>/reader_delete', views.reader_delete),
    path('index/<int:nid>/reader_edit', views.reader_edit),
    path('index/<int:nid>/book_delete', views.book_delete),
    path('index/<int:nid>/book_edit', views.book_edit),
    path('index/book_add', views.book_add),
    path('index/borrow_manage', views.borrow_manage),
    path('index/book_manage', views.book_manage)
]
