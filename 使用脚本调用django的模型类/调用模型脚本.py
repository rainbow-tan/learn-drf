import os
import sys

sys.path.append(r"E:\github_code\learn-drf\tutorial")  # 这里是django项目的绝对路径,即django项目中manage.py所在的文件夹路径
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tutorial.settings')  # 这里直接从django项目中manage.py进行拷贝
import django

django.setup()
# 导入django项目中的模型类  要是不知道该怎么导入 可以先去django项目中 根目录下创建一个py文件,然后输入模型类名让编辑器自动导入 或者找一找django项目中 使用模型类是怎么导入的 然后拷贝过来即可
# 也可以直接放在django项目的根目录下使用 这样导入就通过编辑器自动提示, 更方便了
from student_manager.models import Student

students = Student.objects.all()  # 后面就是直接使用模型类了
for s in students:
    print(s)
