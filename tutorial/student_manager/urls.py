from django.urls import path, re_path

from student_manager.views import student_list, student_detail

urlpatterns = [
    path('list/', student_list),
    re_path(r'detail/([0-9]+)/', student_detail),
]
