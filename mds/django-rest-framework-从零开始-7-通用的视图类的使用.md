django-rest-framework-从零开始-7-通用的视图类的使用

## 1、前言

- 之前，我们知道了有一个公共的`GenericAPIView`类，只需要将模型类和序列化类通过定义`GenericAPIView`类中`queryset`和`serializer_class`属性或者重写`GenericAPIView`类中的`get_queryset()`和`get_serializer_class()`就可以告知它我们的模型类和序列化类，这样它就能完成一般的CRUD功能。

- 但是我们还需要明确写出`get`视图函数调用`list`方法，`post`视图函数调用`create`方法，`put`视图函数调用`update`方法，`delete`视图函数调用`destory`方法，这又是重复代码，因此drf又提供了功能的类，名叫`ListCreateAPIView`类和`RetrieveUpdateDestroyAPIView`类

- `ListCreateAPIView`类用于List视图，而`RetrieveUpdateDestroyAPIView`类用于Detail视图。List视图就是用于获取所有模型对象信息和创建一个模型对象。Detail视图用于获取单个模型对象和更新、删除单个模型对象。

- `ListCreateAPIView`类继承了`mixins.ListModelMixin`,`mixins.CreateModelMixin`和`GenericAPIView`，并重写了get、post方法。直接完成了List视图的功能

- `RetrieveUpdateDestroyAPIView`类继承了`RetrieveModelMixin`,`UpdateModelMixin`,`DestroyModelMixin`,`GenericAPIView`类，重写了get、put、patch、delete方法，直接完成了Detail视图

## 2、创建`ListCreateAPIView`类视图和`RetrieveUpdateDestroyAPIView`类视图

修改`student_manager/views.py`文件

```python
class StudentList(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class StudentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
```

图示

![image-20230317142347819](C:\Users\dell\AppData\Roaming\Typora\typora-user-images\image-20230317142347819.png)

说明：

- 可以看出这里把之前的所有公共的方法都抽出来，作为基类了。只需要我们填充模型类和序列化类。

- 到这里，整体的流程就是：
  - 发起请求，到达路由，路由分配对应的请求视图函数，视图函数找到mixins的处理函数，处理函数调用基类GenericAPIView的一些函数，执行后返回数据

## 3、启动服务，测试类视图

测试和之前一样。

## 4、跋文

最终，我们如果想要编写一个drf的项目，完成简单的CRUD，则只需要以下几步

（1）定义模型，例如`class Student(models.Model):`

（2）通过继承`ModelSerializer`类定义序列化类，例如`class StudentSerializer(serializers.ModelSerializer):`

（3）通过继承`ListCreateAPIView`和`RetrieveUpdateDestroyAPIView`定义视图函数，例如

```
class StudentList(generics.ListCreateAPIView):
class StudentDetail(generics.RetrieveUpdateDestroyAPIView):
```

（4）添加路由，例如

```
path('list/', StudentList.as_view()),
re_path(r'detail/(?P<pk>[0-9]+)/', StudentDetail.as_view()),
```

这样，就完成了一个简单的CRUD。可以通过get获取所有数据或单条数据，通过post添加一条数据，通过put修改一条数据，通过delete删除一条数据。相当简单，而且请求的流程也在脑海中，清晰可见。

github：https://github.com/rainbow-tan/learn-drf