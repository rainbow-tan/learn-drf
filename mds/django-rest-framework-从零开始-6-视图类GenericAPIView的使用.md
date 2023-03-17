django-rest-framework-从零开始-6-视图类GenericAPIView的使用

## 1、前言

- 之前提到过的基于`APIView`类的视图，需要重写["get","post","put","patch", "delete","head","options","trace"]等方法，来达到处理请求的目的。

- 基于`APIView`类的视图，核心功能都是一样的，如果我们有多个模型，则需要所有模型都写一个基于`APIView`类的视图，然后修改其中的模型类和序列化类，这样看起来，代码就重复了很多。

- 是否有一个类，可以直接完成这些功能，只需要告诉它模型类和序列化类。它就可以自己生成这些方法，并补充完其中的函数体。

## 2、创建`GenericAPIView`类视图

上面我们需要一个类，直接完成绑定请求视图的功能。django-rest-framework提供了一些类，可以用于实现以上功能。

改造`student_manager/views.py`文件

```python
class StudentList(generics.GenericAPIView,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  ):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class StudentDetail(generics.GenericAPIView,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
```

图示

![image-20230317111422747](C:\Users\dell\AppData\Roaming\Typora\typora-user-images\image-20230317111422747.png)

修改`student_manager/urls.py`路由，指定视图参数pk

```
re_path(r'detail/(?P<pk>[0-9]+)/', StudentDetail.as_view()),
```

图示

![image-20230317134349455](C:\Users\dell\AppData\Roaming\Typora\typora-user-images\image-20230317134349455.png)

说明：

- 我们要基于类的视图，那肯定要继承`APIView`类，但`APIView`类无法知道我们的模型类和序列化类都分别是什么，因此django-rest-framework封装了一个类，名叫`GenericAPIView`类，该类继承了`APIView`类，因此继承它后，我们也需要定义对应的["get","post","put","patch", "delete","head","options","trace"]方法。

- `GenericAPIView`类多了一些方法，能识别模型类和序列化类。我们通过定义`GenericAPIView`类中`queryset`和`serializer_class`属性，告知我们的模型类和序列化类。也可以通过重写`GenericAPIView`类中的`get_queryset()`和`get_serializer_class()`告知我们的模型类和序列化类

  - 注意：当我们重写了视图类，即重写了["get","post","put","patch", "delete","head","options","trace"]方法，在视图中，如果我们需要获取模型类时，应该调用`get_queryset()`方法，而不是访问`queryset`属性，这是drf的约定。

    ![image-20230317112602261](C:\Users\dell\AppData\Roaming\Typora\typora-user-images\image-20230317112602261.png)

- 我们重写了get，post,put，delete方法，这些方法都直接调用了对应mixins文件中的各个基类，完成视图的自动适配。

  - 重写了`StudentList`的`get`方法，调用了`ListModelMixin`的`list`方法，`list`方法中调用了`GenericAPIView`类的`filter_queryset`方法和`get_serializer`方法，所以最终还是使用了`GenericAPIView`类和它的基类`APIView`类的方法。只是绑定了get请求来临时，调用list方法。

  - 重写的`post`方法，调用了`CreateModelMixin`类的`create`方法，`create`方法中调用了`GenericAPIView`类的`get_serializer`方法，最终调用了序列化类的`save`方法，`save`方法，还是调用序列化类的`create`方法（这是之前就了解到的了）。

  - 重写了`StudentDetail`中的`get`方法，调用了`RetrieveModelMixin`的`retrieve`方法，`retrieve`方法调用了`GenericAPIView`类的`get_object()`和`get_serializer`方法

  - 重写了put方法，调用了`UpdateModelMixin`的update方法，update方法调用了`GenericAPIView`类的`get_object()`和`get_serializer`方法以及最终调用了序列化类的`save`方法，`save`方法，还是调用序列化类的`create`方法（这是之前就了解到的了）。

  - 重写了`delete`方法，调用了`DestroyModelMixin`的`destory`方法，`destory`方法调用了`GenericAPIView`类的`get_object()`最终调用了模型类的`delete`方法

    大概就是表中样子，具体可以看源码

    | 视图方法        | 对应视图基类及方法             | 调用`GenericAPIView`类的函数     |
    | --------------- | ------------------------------ | -------------------------------- |
    | List中的get方法 | ListModelMixin：list()         | get_queryset()和get_serializer() |
    | post            | CreateModelMixin：create()     | get_serializer()                 |
    | Detail的get方法 | RetrieveModelMixin：retrieve() | get_object()和get_serializer()   |
    | put             | UpdateModelMixin：update()     | get_object()和get_serializer()   |
    | delete          | DestroyModelMixin：destory()   | get_object()                     |

- 这里要注意的是，URL路由的写法，需要为(?P<name>pattern) 这种写法

## 3、启动服务，测试基于`GenericAPIView`类视图

测试和之前一样。

github：https://github.com/rainbow-tan/learn-drf