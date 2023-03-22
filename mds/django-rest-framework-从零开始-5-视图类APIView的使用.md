django-rest-framework-从零开始-5-视图类`APIView`的使用

## 1、前言

之前编写的视图函数，都是基于`@api_view`函数创建出的视图，通过判断`request.method`获取到请求方式，然后执行对应的逻辑。接下来，我们基于类创建视图。

## 2、创建`APIView`类视图

1.创建视图只需要继承`APIView`类，即可

2.修改对应的路由

改造`student_manager/views.py`文件，把基于`@api_view`编写的视图，变成基于`APIView`类的视图

```python
class StudentList(APIView):
    @staticmethod
    def get(request):
        result = Student.objects.all()
        serializer = StudentSerializer(result, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        serializer = StudentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentDetail(APIView):
    @staticmethod
    def get_object(pk):
        try:
            return Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        obj = self.get_object(pk)
        serializer = StudentSerializer(instance=obj)
        return Response(serializer.data)

    def put(self, request, pk):
        snippet = self.get_object(pk)
        serializer = StudentSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        obj = self.get_object(pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

图示

![image-20230317100253477](https://img2023.cnblogs.com/blog/1768648/202303/1768648-20230321172721581-801580758.png)

改造路由，修改`student_manager/urls.py`文件，修改路由

```python
path('list/', StudentList.as_view()),
re_path(r'detail/([0-9]+)/', StudentDetail.as_view()),
```

图示

![image-20230317100212628](https://img2023.cnblogs.com/blog/1768648/202303/1768648-20230321172722002-68375055.png)

说明

- 基于`APIView`类创建出的视图，需要重写"get","post","put","patch","delete"等方法，发起的请求，会根据请求方式来执行对应的视图。

- 关于为什么是重写这些方法，发起请求后怎么决定访问哪一个视图，可以从路由`APIView`类的`as_view()`方法得到答案

- 查看`as_view()`的函数定义源代码，最终在基类`View`中，可以看到，先调用了`setup`函数，然后调用了`dispatch`函数（[学习链接](https://www.cnblogs.com/olivertian/p/11072528.html)）

  ![image-20230317101404124](https://img2023.cnblogs.com/blog/1768648/202303/1768648-20230321172722391-2068542042.png)

- 查看`setup`函数和`dispatch`函数

![image-20230317101908944](https://img2023.cnblogs.com/blog/1768648/202303/1768648-20230321172722767-1692996143.png)

可以看到，首先判断是否请求在["get","post","put","patch", "delete","head","options","trace",]中，在其中则合理，合理就会获取对象的方法，然后返回该方法。

因此，每个请求对应`APIView`类的一个方法，所以我们需要把对应方法定义出来。为定义出来的，则抛出405

`"detail": "Method "请求方式" not allowed."`不得不说，这个用法挺好。

## 3、启动服务，测试基于`APIView`类视图

测试和之前一样。

github：https://github.com/rainbow-tan/learn-drf