import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tutorial.settings')
import django

django.setup()
from student_manager.serializers import StudentSerializer


def add_student():
    data = dict(student_id="1002",
                student_name="小红",
                student_sex=1,
                student_birthday="2020-1-1")
    serializer = StudentSerializer(data=data)
    print(f"serializer:{serializer}")

    serializer.is_valid(True)  # 判断数据是否合法
    serializer.save()  # 调用save方法, 会调用到序列化类中的create方法


if __name__ == '__main__':
    add_student()
