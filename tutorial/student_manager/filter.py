from django_filters.rest_framework import FilterSet

from student_manager.models import Student


class StudentFilter(FilterSet):
    class Meta:
        model = Student
        fields = {
            # ...\site-packages\django_filters\conf.py 该文件中看到可选项
            # student_name 不区分大小写的包含关系
            "student_name": ["icontains"],

            # student_birthday 大于等于 小于等于 大于 小于
            'student_birthday': ["gte", "lte", 'gt', 'lt'],

            # student_sex 完全相等
            'student_sex': ['exact'],
        }
        # https://zhuanlan.zhihu.com/p/110060840
