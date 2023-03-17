django-rest-framework-从零开始-8-Serializer多序列化一个字段

## 1、前言

这里是属于自己的项目需求，而研究的功能。

- 目的：想在Serializer类中，多显示一个字段。

例如：模型使用之前的Student模型

![image-20230317160104729](C:\Users\dell\AppData\Roaming\Typora\typora-user-images\image-20230317160104729.png)

- 情景：学校里面举办了一个游戏，游戏中，每个同学有一个自己的唯一的游戏ID，我们可以使用学号作为游戏ID，但为了演示新功能，我们不用学号，而是通过UUID为每个学生来生成一个游戏ID。
- 真实场景是，数据库中记录了虚拟机的信息，但是没记录IP，毕竟IP会变，每次调用时，通过其他http接口，获取到IP,然后显示

想到达到的效果是，通过get请求，获取所有学生信息时，多显示一个额外的字段，称为game_id。

原来通过获取的返回数据和我们想显示的数据如下

![image-20230317161521420](C:\Users\dell\AppData\Roaming\Typora\typora-user-images\image-20230317161521420.png)

## 2、在Serializer类中多序列化一个字段

在此之前，我们知道了怎么快速创建一个CRUD的drf项目，而且知道发送get请求，最终会调用视图的list方法，因此改造步骤如下：

（1）序列化类中添加想要显示的字段

修改`student_manager/serializers.py`文件中的`StudentSerializer`类

```
class StudentSerializer(serializers.ModelSerializer):
    game_id = serializers.CharField(read_only=True)

    class Meta:
        model = Student
        fields = '__all__'
```

说明：添加了一个game_id的字段，且设置为read_only，设置完read_only才会跳过从数据库同步，因此模型类没有该属性，想通过数据库同步，必然是失败的，不加read_only=True会这样报错

AttributeError: Got AttributeError when attempting to get a value for field `game_id` on serializer `StudentSerializer`.

![image-20230317162405159](C:\Users\dell\AppData\Roaming\Typora\typora-user-images\image-20230317162405159.png)

很好理解，就是去获取字段时，通过getattr获取，获取不到，则报错，因此设置为read_only=True即可

（2）重写视图函数中的list函数

因为最终调用是走的list函数，因此重写list函数即可,文件是`student_manager/views.py`

```python
class StudentList(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        for one in serializer.data:
            one['game_id'] = uuid.uuid4().hex
        return Response(serializer.data)
```

我们在获取到serializer.data时，添加game_id属性即可

（3）Detail的get对应retrieve方法也需要重写一下

```python
class StudentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        data['game_id'] = uuid.uuid4().hex
        return Response(data)
```

当然，如果post、put时，也想显示game_id，则需要重新对应的方法

（4）验证

发送List视图的get请求，验证数据

![image-20230317163618478](C:\Users\dell\AppData\Roaming\Typora\typora-user-images\image-20230317163618478.png)

发送Detail视图的get请求

![image-20230317164408598](C:\Users\dell\AppData\Roaming\Typora\typora-user-images\image-20230317164408598.png)

github：https://github.com/rainbow-tan/learn-drf