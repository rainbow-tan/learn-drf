import django_filters.rest_framework.filters as filters
from django_filters.rest_framework import FilterSet

from student_manager.models import Student


class StudentFilter(FilterSet):
    year_is_even_number = filters.BooleanFilter('student_birthday', label='生日年份是偶数', method='filter_student_birthday')

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
        # https://zhuanlan.zhihu.com/p/113328475

    @staticmethod
    def filter_student_birthday(qs, field_name, value):
        print(f'qs:{qs}')  # 未过滤前的数据
        print(f'field_name:{field_name}')  # 过滤的字段
        print(f'value:{value}')  # 前端传递的参数
        if not value:
            return qs
        all_id = []

        for student in qs:
            year = student.student_birthday.strftime("%Y")
            print(f'year:{year}')
            if int(year) % 2 == 0:
                all_id.append(student.id)
        print(f'new:{all_id}')
        students = Student.objects.filter(id__in=all_id)
        print(f"students:{students}")
        return students
