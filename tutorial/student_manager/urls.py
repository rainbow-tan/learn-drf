from django.urls import path, re_path

# from student_manager.views import student_list, student_detail
from student_manager.views import StudentList, StudentDetail

urlpatterns = [
    # path('list/', student_list),
    # re_path(r'detail/([0-9]+)/', student_detail),
    path('list/', StudentList.as_view()),
    # re_path(r'detail/([0-9]+)/', StudentDetail.as_view()),
    re_path(r'detail/(?P<pk>[0-9]+)/', StudentDetail.as_view()),
]
