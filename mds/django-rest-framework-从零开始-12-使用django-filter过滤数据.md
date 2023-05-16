django-rest-framework-从零开始-12-使用django-filter过滤数据

## 1、前言

前端可能根据用户的选择来过滤数据，我们需要支持一下，可以使用django-filter这个库来过滤。[官网](https://pypi.org/project/django-filter/) 和 [API文档](https://django-filter.readthedocs.io/en/stable/guide/rest_framework.html)

## 2、下载

```python
python -m pip install django-filter
```

## 3、简单过滤

### 3.1、注册到APP中

在文件`tutorial/settings.py`中添加`django_filters`

![image-20230515144239719](C:\Users\dell\AppData\Roaming\Typora\typora-user-images\image-20230515144239719.png)

### 3.2、视图类添加过滤类

在文件`student_manager/views.py`中添加过滤类和条件

简单的过滤只需添加`DjangoFilterBackend`类和过滤的列名即可

![image-20230515144318826](C:\Users\dell\AppData\Roaming\Typora\typora-user-images\image-20230515144318826.png)

```python
class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    filter_backends = [DjangoFilterBackend]  # 仅使用该类过滤
    filterset_fields = ['student_name', 'student_sex', 'student_birthday']  # 过滤的字段
```

### 3.3、验证简单过滤

通过API文档测试:http://127.0.0.1:9000/api-ui/#/student/student_list

![image-20230515144808181](C:\Users\dell\AppData\Roaming\Typora\typora-user-images\image-20230515144808181.png)

通过浏览器页面测试：http://127.0.0.1:9000/student/?student_name=%E5%A2%A8%E7%8E%89%E9%BA%92%E9%BA%9F

![image-20230515144933733](C:\Users\dell\AppData\Roaming\Typora\typora-user-images\image-20230515144933733.png)

通过apipost测试：

![image-20230515145334753](C:\Users\dell\AppData\Roaming\Typora\typora-user-images\image-20230515145334753.png)

### 3.4、默认使用DjangoFilterBackend的写法

上面的写法，如果有多个视图类，则每个视图类都需要添加一行`filter_backends = [DjangoFilterBackend]`

可以抽出去，默认就支持检查的字段过滤。

只需要在`tutorial/tutorial/settings.py`的中`REST_FRAMEWORK`设置即可

![image-20230515160759028](C:\Users\dell\AppData\Roaming\Typora\typora-user-images\image-20230515160759028.png)

```python
REST_FRAMEWORK = {
    ...
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',)
}
```

然后视图类中，只需要过滤的字段即可

![image-20230515160942492](C:\Users\dell\AppData\Roaming\Typora\typora-user-images\image-20230515160942492.png)

### 备注：

**上述的查询条件是与的关系，且查询的内容是完全等于的关系**

e.g.

原数据为 墨玉麒麟	男	2023-03-23

| student_name | student_sex | student_birthday | 能查询出来吗 |
| ------------ | ----------- | ---------------- | ------------ |
| 墨玉麒麟     |             |                  | 能           |
|              | 男          | 2023-03-23       | 能           |
| 墨玉麒麟     | 男          | 2023-03-23       | 能           |
| 墨玉         |             |                  | 不能         |
| 麒麟         |             |                  | 不能         |
| 墨玉麒麟     | 女          | 2023             | 不能         |
| 墨玉麒麟     |             | 2023             | 不能         |
| 墨玉麒麟     |             | 2023-03          | 不能         |
| ...          | ...         | ...              | 不能         |

## 4、自定义过滤器

### 4.1、自定义过滤类

编写一个新文件，名字为`student_manager/filter.py`添加以下内容

```python
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
```

![image-20230515172644560](C:\Users\dell\AppData\Roaming\Typora\typora-user-images\image-20230515172644560.png)

#### 说明：

步骤如下：

- 继承FilterSet

- 指定过滤的模型类

- 指定过滤的字段和过滤的方式

### 4.2、视图类指定过滤类

在视图类中指定刚才的过滤类

在`student_manager/views.py`中指定过滤类

![image-20230516095639401](C:\Users\dell\AppData\Roaming\Typora\typora-user-images\image-20230516095639401.png)

```python
class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    # filter_backends = [DjangoFilterBackend]  # 仅使用该类过滤
    # filterset_fields = ['student_name', 'student_sex', 'student_birthday']  # 过滤的字段
    filter_class = StudentFilter
```

### 4.3、测试过滤类

![image-20230516095821807](C:\Users\dell\AppData\Roaming\Typora\typora-user-images\image-20230516095821807.png)

### 备注：

视图类中同时使用`filterset_fields`和`filter_class`，测试后发现`filterset_fields`不起作用

## 5、自定义过滤器之自定义过滤函数

上述的过滤器都是基于字段名称和ORM的过滤，这里举一个例子，通过自定义过滤函数实现过滤效果的例子

过滤功能：获取生日的年份是偶数的学生

直接修改过滤器即可，步骤如下：

### 5.1、指定过滤的字段与过滤的函数

```
year_is_even_number = filters.BooleanFilter('student_birthday', label='生日年份是偶数', method='filter_student_birthday')
```

`label参数`指定的是过滤名称是`生日年份是偶数`

`method参数`指定的是过滤函数是`filter_student_birthday`

`第一个参数`指定过滤的字段名称是`student_birthday`

### 5.2、定义过滤的函数

```python
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
```

过滤函数需要三个参数：

- `qs`是未过滤前的数据，类型是QuerySet

- `field_name`是过滤的字段，这里必然是student_birthday

- `value`是前端传递的参数，因为指定的是BooleanFilter类，所以必然是True或者False

完整代码如下

![image-20230516105639714](C:\Users\dell\AppData\Roaming\Typora\typora-user-images\image-20230516105639714.png)

```python
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
```

### 5.3、验证过滤器

![image-20230516105732469](C:\Users\dell\AppData\Roaming\Typora\typora-user-images\image-20230516105732469.png)

![image-20230516105800696](C:\Users\dell\AppData\Roaming\Typora\typora-user-images\image-20230516105800696.png)

## 6、参考链接

https://zhuanlan.zhihu.com/p/110060840

https://zhuanlan.zhihu.com/p/113328475





























[github](https://github.com/rainbow-tan/learn-drf)