from django.urls import path

from student_manager.views import students_list

urlpatterns = [
    path('list/', students_list),
]
