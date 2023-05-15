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

### PS：

**上述的查询条件是与的关系，且查询的内容是==的关系**

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



[github](https://github.com/rainbow-tan/learn-drf)