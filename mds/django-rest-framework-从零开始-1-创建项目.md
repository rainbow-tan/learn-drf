django-rest-framework-从零开始-1-创建项目

## 1、下载模块

```shell
python -m pip install django 
python -m pip install djangorestframework 
```

本次学习基于python3.9，python安装的绝对路径为`F:\Python3.9.12`，安装完django后，默认在python的安装路径下的Scripts文件夹(即`F:\Python3.9.12\Scripts`)中会包含一个名为django-admin.exe的可执行文件，即F:\Python3.9.12\Scripts\django-admin.exe

- python路径

![image-20230315184055374](https://img2023.cnblogs.com/blog/1768648/202303/1768648-20230321151840468-158967557.png)

- django-admin.exe路径![image-20230315184206598](https://img2023.cnblogs.com/blog/1768648/202303/1768648-20230321151840975-1443118861.png)

## 2、创建项目

启动一个cmd,输入以下命令，创建项目和模型

```shell
‪F:\Python3.9.12\Scripts\django-admin.exe startproject tutorial
cd tutorial
python manage.py startapp student_manager
```

![image-20230316094129491](https://img2023.cnblogs.com/blog/1768648/202303/1768648-20230321151841346-118833467.png)

创建后的项目目录

![image-20230316094425745](https://img2023.cnblogs.com/blog/1768648/202303/1768648-20230321151841667-608731279.png)

## 3、添加模型

1. 在`tutorial/settings.py`中注册`student_manager`模型和`rest_framework`模型

   ![image-20230316102048543](https://img2023.cnblogs.com/blog/1768648/202303/1768648-20230321151841971-1745401962.png)

2. 在`student_manager/models.py`中添加Student的模型代码

```python
class Student(models.Model):
    student_id = models.CharField(verbose_name="学号", max_length=30, unique=True, null=False, blank=False, db_index=True, help_text="学号最大长度为30")
    student_name = models.CharField("姓名", max_length=30, unique=False, null=False, blank=False, db_index=True, help_text="学号最大长度为30")
    student_sex = models.SmallIntegerField("性别", choices=[(1, '男'), (0, '女')], null=False, blank=False, help_text="1->男,0->女")
    student_birthday = models.DateField("生日", null=False, blank=False, help_text="学生生日")

    id = models.AutoField(primary_key=True)
    created = models.DateTimeField("创建时间", auto_now_add=True)
    updated = models.DateTimeField("修改时间", auto_now=True)

    class Meta:
        db_table = 't_student'

    def __str__(self):
        return f"Student({self.student_id}->{self.student_name})"

    def __repr__(self):
        return self.__str__()

    """
    学习链接
    https://blog.csdn.net/Mikowoo007/article/details/98203653
    官网 https://docs.djangoproject.com/zh-hans/4.1/ref/models/fields/
    """
```

图示

![image-20230316101732047](https://img2023.cnblogs.com/blog/1768648/202303/1768648-20230321151842305-2118568959.png)

3. 同步数据库

   运行以下命令，同步模型到数据库，默认使用sqlite

   ```python
   python manage.py makemigrations 
   python manage.py migrate
   ```

4. 添加一个超级用户

   ```python
   python manage.py createsuperuser
   ```

   根据提示输入用户名，密码，邮箱即可

   ![image-20230316103121432](https://img2023.cnblogs.com/blog/1768648/202303/1768648-20230321151842647-1115233899.png)

github：https://github.com/rainbow-tan/learn-drf
