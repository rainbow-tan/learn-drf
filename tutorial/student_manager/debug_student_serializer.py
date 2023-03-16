import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tutorial.settings')
import django

django.setup()
from student_manager.serializers import StudentSerializer
from student_manager.models import Student
from rest_framework.renderers import JSONRenderer


def add_student():
    data = dict(student_id="1001",
                student_name="小红",
                student_sex=1,
                student_birthday="2020-1-1")
    serializer = StudentSerializer(data=data)
    print(f"serializer:{serializer}")

    serializer.is_valid(True)  # 判断数据是否合法
    serializer.save()  # 调用save方法, 会调用到序列化类中的create方法(未传递instance参数时)


def list_student():
    instance = Student.objects.get(student_id="1001")
    serializer = StudentSerializer(instance=instance)
    data = serializer.data
    print(f'data:{data}')
    content = JSONRenderer().render(serializer.data)
    print(f'content:{content}')


def list_all_students():
    instance = Student.objects.all()
    serializer = StudentSerializer(instance=instance, many=True)
    data = serializer.data
    print(f'data:{data}')
    content = JSONRenderer().render(serializer.data)
    print(f'content:{content.decode("utf-8")}')


def update_student():
    data = dict(student_id="1009",
                student_name="小红rename",
                student_sex=1,
                student_birthday="2020-1-19")
    instance = Student.objects.get(student_id="1001")
    serializer = StudentSerializer(instance=instance, data=data)
    serializer.is_valid(True)
    serializer.save()  # 调用save方法, 会调用到序列化类中的update方法(传递instance参数时)


def show_serializer():
    serializer = StudentSerializer()
    print(f"serializer:{serializer}")



if __name__ == '__main__':
    # add_student()
    # list_student()
    # list_all_students()
    # update_student()
    show_serializer()
