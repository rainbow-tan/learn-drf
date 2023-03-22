django-rest-framework-从零开始-9-视图类ModelViewSet的使用

## 1、前言

在之前（django-rest-framework-从零开始-7-通用的视图类的使用），我们通过简单几步，就可以创建出简单CRUD的drf项目，通过路由的list和detail路径， 分别指向不同的视图类，即List类和Detail类。

路由如下

![image-20230320101213260](https://img2023.cnblogs.com/blog/1768648/202303/1768648-20230321190515728-973033735.png)

视图类如下

![image-20230320101259239](https://img2023.cnblogs.com/blog/1768648/202303/1768648-20230321190516143-1161472773.png)

但是，他们之间，也有相同的代码，都需要指定模型类和序列化视图。那么是否有一个公用类，可以直接代替这两个类，完成最终的基类，实现只要告知一次模型类和序列化类即可。

## 2、创建`ModelViewSet`类视图（模型视图类）

### （1）改造`student_manager/views.py`文件

```
class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
```

图示

![image-20230320101647294](https://img2023.cnblogs.com/blog/1768648/202303/1768648-20230321190516489-1113197332.png)

说明:

- 我们把`StudentList`和`StudentDetail`重命名为`StudentViewSet`，然后继承ModelViewSet，直接完成了类的合二为一

- 可以看到`ModelViewSet`类，继承了`CreateModelMixin`, `RetrieveModelMixin`, `UpdateModelMixin`, `DestroyModelMixin`, `ListModelMixin`, `GenericViewSet`类，这几个类，就是之前的`RetrieveUpdateDestroyAPIView`类和`ListCreateAPIView`类的基类，相当于`ModelViewSet`类，把它们合二为一了，完成了真正的基类，通过`ModelViewSet`类，我们只需要告知一次模型类和序列化类即可。

### （2）路由改造

在此之前，我们需要通过路由，list指向`StudentList`视图，detail指向`StudentDetail`视图，那么我们把`StudentList`和`StudentDetail`合二为一了，是否也能直接把路由合二为一？

我们细想一下，它们直接的其他请求方式，获取所有数据和创建数据不需要主键PK,而检索一条数据和修改、删除、更新一条数据需要主键PK，因此，还是分不开，所以，我们这么改造路由。

改造`student_manager/urls.py`路由文件

```python
from django.urls import path, re_path

# from student_manager.views import student_list, student_detail
# from student_manager.views import StudentList, StudentDetail
from student_manager.views import StudentViewSet

urlpatterns = [
    # path('list/', student_list),
    # re_path(r'detail/([0-9]+)/', student_detail),
    # path('list/', StudentList.as_view()),
    # re_path(r'detail/([0-9]+)/', StudentDetail.as_view()),
    # re_path(r'detail/(?P<pk>[0-9]+)/', StudentDetail.as_view()),

    path('', StudentViewSet.as_view({'get': 'list', 'post': 'create'})),
    re_path(r'(?P<pk>[0-9]+)/', StudentViewSet.as_view({'get': 'retrieve',
                                                        'put': 'update',
                                                        'patch': 'partial_update',
                                                        'delete': 'destroy'})),
]
```

图示

![image-20230320103137539](https://img2023.cnblogs.com/blog/1768648/202303/1768648-20230321190516830-2017817675.png)

说明：

- 我们直接去掉了list和detail关键字，直接通过是否携带主键PK来决定走哪一种视图，带有PK的路由，就走detail路由对应的视图，不带PK的路由，就走list路由对应的视图，这里把两个关键字直接去掉了，然后通过`as_view`函数来显示定义出请求方式对应的视图函数，请注意，这里的`as_view`函数不再是之前`View`基类的`as_view`函数。而是`ViewSetMixin`类的`as_view`函数，可不要混淆了。
- 我们得告诉路由，什么请求方式用哪一个函数作为视图，因此，我们显示定义了这样的字典`{'get': 'list', 'post': 'create'}`和`{'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}`这样，当请求来临时，就可以找到对应处理的视图函数


## 3、启动服务，测试类视图

测试和之前一样。

## 4、模型视图通用URL改造

在上面，我们的路由，其实都是相同的，增加一个模型类，我们增加序列化类和模型视图类，都需要增加两个路由，且内容都一样，只是模型视图类不一致，后面as_view函数的参数都一致，因此，drf提供了针对于模型视图的路由注册通用方法。

- 改造`student_manager/urls.py`路由文件

  ```python
  from django.urls import path, include
  # from student_manager.views import student_list, student_detail
  # from student_manager.views import StudentList, StudentDetail
  from rest_framework.routers import DefaultRouter
  
  from student_manager.views import StudentViewSet
  
  router = DefaultRouter()
  router.register('', StudentViewSet)
  
  urlpatterns = [
      # path('list/', student_list),
      # re_path(r'detail/([0-9]+)/', student_detail),
      # path('list/', StudentList.as_view()),
      # re_path(r'detail/([0-9]+)/', StudentDetail.as_view()),
      # re_path(r'detail/(?P<pk>[0-9]+)/', StudentDetail.as_view()),
  
      # path('', StudentViewSet.as_view({'get': 'list', 'post': 'create'})),
      # re_path(r'(?P<pk>[0-9]+)/', StudentViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
  
      path('', include(router.urls)),
  ]
  ```

图示

![image-20230320105012692](https://img2023.cnblogs.com/blog/1768648/202303/1768648-20230321190517240-1133771658.png)

说明：

- 我们只需要简单的把模型类视图注册到路由即可。

- 通过查看了源码，可以看到，就是把我们之前的显示表达的映射关系，给定义出来，然后映射出去。直接替我们完成了映射请求方式与处理视图的代码。

  ![image-20230320105447894](https://img2023.cnblogs.com/blog/1768648/202303/1768648-20230321190517728-1902950032.png)

## 4、跋文

最终，我们如果想要编写一个drf的项目，完成简单的CRUD，则只需要以下几步

（1）定义模型，例如`class Student(models.Model):`

（2）通过继承`ModelSerializer`类定义序列化类，例如`class StudentSerializer(serializers.ModelSerializer):`

（3）通过继承`ModelViewSet`类定义模型视图类，例如`class StudentViewSet(ModelViewSet):`

（4）注册路由DefaultRouter().register注册路由，例如`router.register('', StudentViewSet)`、`path('', include(router.urls)),`

这样，就完成了一个简单的CRUD。可以通过get获取所有数据或单条数据，通过post添加一条数据，通过put修改一条数据，通过delete删除一条数据。相当简单，而且请求的流程也在脑海中，清晰可见。
