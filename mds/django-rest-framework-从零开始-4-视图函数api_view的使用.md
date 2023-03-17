django-rest-framework-从零开始-4-视图函数api_view的使用

## 1、前言

我们之前测试都是基于本地调试，采用直接运行py的方式，并没有启动服务，接下来，我们尝试通过请求与相应来处理一些请求，首先是编写视图，接下来就是生成路由，然后启动服务即可。

## 2、编写视图函数

（1）在`student_manager/views.py`中添加视图代码

```python
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from student_manager.models import Student
from student_manager.serializers import StudentSerializer


@api_view(['GET', 'POST'])
def students_list(request: Request):
    if request.method == 'GET':
        result = Student.objects.all()
        serializer = StudentSerializer(result, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = request.data
        serializer = StudentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

图示

![image-20230316165034726](C:\Users\dell\AppData\Roaming\Typora\typora-user-images\image-20230316165034726.png)

说明：

- 通过`@api_view(['GET', 'POST'])`转化django的HttpRequest为rest_framework.request.Request对象，转为HttpResponse为rest_framework.request.HttpResponse对象。

- GET和POST说明，只支持这两种请求方式

- 当请求方式为GET时，则返回所有数据库数据，为POST时，则是创建记录。创建记录前，进行校验请求数据合法性。

（2）添加路由

创建`student_manager/urls.py`文件，添加代码

```python
from django.urls import path

from student_manager.views import students_list

urlpatterns = [
    path('list/', students_list),
]
```

图示

![image-20230316165702424](C:\Users\dell\AppData\Roaming\Typora\typora-user-images\image-20230316165702424.png)

在`tutorial/urls.py`中添加代码

```
path('student/',include('student_manager.urls'))
```

图示

![image-20230316165752589](C:\Users\dell\AppData\Roaming\Typora\typora-user-images\image-20230316165752589.png)

## 3、请求所有数据或者创建一条数据

启动服务

```
python.exe manage.py runserver 0.0.0.0:9000
```

发送GET请求获取所有数据库记录

![image-20230316165932354](C:\Users\dell\AppData\Roaming\Typora\typora-user-images\image-20230316165932354.png)

发送POST请求，创建一条记录

- 参数不合法

![image-20230316170005489](C:\Users\dell\AppData\Roaming\Typora\typora-user-images\image-20230316170005489.png)

- 参数合法

![image-20230316170126110](C:\Users\dell\AppData\Roaming\Typora\typora-user-images\image-20230316170126110.png)

数据库

![image-20230316170143720](C:\Users\dell\AppData\Roaming\Typora\typora-user-images\image-20230316170143720.png)

说明：

简单的请求路程为：

GET发起请求->过中间件->到达视图->获取所有数据->序列化数据->返回数据

POST发起请求->过中间件->到达视图->获取请求载体>校验请求载体->失败贼抛出异常，异常经过中间件处理，返回异常信息|成功则保存对象到数据库，返回保存的对象序列化数据

## 4、请求一条数据或更新|删除一条数据

上面我们可以获取全部数据以及插入数据，接下来，我们来获取一条数据，或者更新、删除数据

在`student_manager/views.py`中添加详情视图

```python
@api_view(['GET', 'PUT', 'DELETE'])
def student_detail(request, pk):
    try:
        student = Student.objects.get(pk=pk)
    except Student.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = StudentSerializer(student)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = StudentSerializer(instance=student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

图示

![image-20230316172547411](C:\Users\dell\AppData\Roaming\Typora\typora-user-images\image-20230316172547411.png)

在student_manager/urls.py中添加详情视图路由

```
re_path(r'detail/([0-9]+)/', student_detail),
```

图示

![image-20230316173933956](C:\Users\dell\AppData\Roaming\Typora\typora-user-images\image-20230316173933956.png)

接下来就是启动服务，执行GET,PUT,DELETE请求来验证

- 启动服务

```
python.exe manage.py runserver 0.0.0.0:9000
```

发送GET请求

![image-20230316174002118](C:\Users\dell\AppData\Roaming\Typora\typora-user-images\image-20230316174002118.png)

发送PUT请求

![image-20230316174147807](C:\Users\dell\AppData\Roaming\Typora\typora-user-images\image-20230316174147807.png)

![image-20230316174225118](C:\Users\dell\AppData\Roaming\Typora\typora-user-images\image-20230316174225118.png)

发送DELETE请求

![image-20230316174255854](C:\Users\dell\AppData\Roaming\Typora\typora-user-images\image-20230316174255854.png)

说明：

在上面，我们可以获取所有数据，可以插入一条数据，更新一条数据，删除一条数据，基本的CRUD已经完成。

github：https://github.com/rainbow-tan/learn-drf