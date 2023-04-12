django-rest-framework-从零开始-11-定义数据源不来自于数据库的视图

## 1、前言

​	我们之前定义视图，数据源都是来源于数据库，从数据库中获取数据，然后序列化。那么，如果数据源不来自于数据库，而是来自于其他途径，比如requests请求，这时候，序列化类就用不上ModelSerializer类了。就需要最初的Serializer类了。

​	对于视图类的queryset属性，也用不了`模型类.objects.all()`这样的写法了，而是需要自己实现。

## 2、情景描述

​	假设需要获取一些物理机的实际情况用于展示，数据库中没有对应的数据，需要通过ssh方式连接到Linux主机中，抓取核心数cores,内存memory和磁盘disk的信息，用于展示。获取物理机可以是全部，也可以是某一个。毕竟物理机的信息实时都在变化，因此，就得请求获取一次，就ssh连接Linux主机一次，然后获取信息。

​	此时，我们无法通过数据库获取信息，也就没有了视图类的queryset属性，而且也不能用ModelSerializer类了，这时候就得从头开始

- 第一个思路：
  - 直接使用视图函数api_view装饰器，一条路走到黑，请求到了视图函数以后，连接ssh，抓取信息，然后包装为JSON数据，返回给前端。
  - 这个方法最简单，什么也不用考虑，非常方便，请求中带有要获取的物理机的IP，直接连进去就行，如果没有IP，则是连接所有的物理机，获取信息.
  - 不太好的地方就是不好对接，因为我们写了自动生成接口文档【django-rest-framework-从零开始-10-自动生成接口文档drf-spectacular的使用】，drf会自动更新接口信息，但用api_view装饰器则没有信息，还需要手动添加@extend_schema装饰器，比较麻烦
- 第二个思路：
  - 用视图类ModelViewSet来实现，设置好queryset属性，设置好Serializer类
  - 这样的困难就是手动写Serializer类和queryset属性，好处就是不用手动补充文档

以下使用第二个思路，第一个思路也很简单，不需要演示了。第二个思路其实就是最初的使用Serializer类写序列化类，以及ModelViewSet中各请求对应的方法的实现，也不是很难，理解了就很简单，这里我记录一下，免得以后想不起来

## 3、定义数据源不来自于数据库的视图

我们的思路是：

①先获取Linux宿主机的信息，获取了以后，就知道应该返回什么样格式的JSON给前端了，JSON格式自己可以先模拟写出来，看看样子

②知道了JSON的格式，就可以定义序列化类了，毕竟序列化类决定了JSON的格式

③接下来就是设置序列化类的queryset属性，这个属性就是第①步中的获取Linux信息的函数的返回值

④然后就是路由和验证了

### 3.1、获取Linux宿主机信息

可以通过paramiko连接Linux主机获取，这里不实际演示，使用虚假数据

新建physical_machine文件夹，新建machine_data.py输入以下内容，模拟物理机数据

```python
import pprint
import random


class Host:
    def __init__(self, ip, core, memory, disk):
        self.ip = ip
        self.core = core
        self.memory = memory
        self.disk = disk

    def __str__(self):
        return vars(self).__str__()

    def __repr__(self):
        return self.__str__()


def get_host_info(search_ip=None):
    data = []
    for i in range(5):
        ip = f"192.168.10.{i + 1}"
        core = random.randint(100, 200)
        memory = f"{random.randint(500, 2048)}G"
        disk = f"{random.randint(1024, 4096)}G"
        if search_ip:
            if ip == search_ip:
                data.append(Host(ip, core, memory, disk))
        else:
            data.append(Host(ip, core, memory, disk))
    return data


if __name__ == '__main__':
    pprint.pprint(get_host_info())  # 测试获取所有机器
    pprint.pprint(get_host_info("192.168.10.3"))  # 测试获取某个机器
    pprint.pprint(get_host_info("192.168.10.9"))  # 测试获取某个不存在机器

```

获取到的信息如下，也打算这么返回JSON给前端

![image-20230412141909930](C:\Users\dell\AppData\Roaming\Typora\typora-user-images\image-20230412141909930.png)

### 3.2、定义queryset属性

视图类的queryset属性其实就是数据集，例如模型类的为模型类.objects.all()，就是获取所有数据库中的数据，那我们这里就是get_host_info()函数，queryset=get_host_info()

### 3.3、定义序列化类

知道了要返回的JSON格式，则就是去定义对应的序列化类，新建student_manager/physical_machine/serializers.py，内容如下

```python
from rest_framework import serializers


class MachineSerializer(serializers.Serializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    ip = serializers.CharField()
    core = serializers.IntegerField()
    memory = serializers.CharField()
    disk = serializers.CharField()
```

ip,core,memory,disk需要和Host类的属性对应，因为序列化类会根据这个名称调用getattr()获取实际信息。如果不一样，例如：

ip想返回时，显示为host,则需要指定source字段，`host = serializers.CharField(source='ip')`这样返回的JSON的ip键就变成了host了。

### 3.4、定义视图类

为了好写路由，我们使用ModelViewSet类来实现，新建student_manager/physical_machine/views.py文件，内容如下

```python
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from physical_machine.machine_data import get_host_info
from physical_machine.serializers import MachineSerializer


class MachineViewSet(ModelViewSet):
    queryset = get_host_info()
    serializer_class = MachineSerializer

    def retrieve(self, request, *args, **kwargs):
        ip = kwargs['pk']
        instance = get_host_info(ip)
        if not instance:
            raise NotFound()
        serializer = MachineSerializer(instance[0])
        return Response(serializer.data)
```

### 3.5、定义路由URL

由于我们只需要get请求，获取所有机器信息，获取某个机器信息，因此，我们只需要暴露get请求即可。新建student_manager/physical_machine/urls.py文件，添加以下内容

```python
from django.urls import path, re_path

from physical_machine.views import MachineViewSet

urlpatterns = [
    path('', MachineViewSet.as_view(dict(get='list'))),
    re_path(r"(?P<pk>\d+\.\d+\.\d+\.\d+)/", MachineViewSet.as_view({"get": "retrieve"})),
    # 路由的\d+\.\d+\.\d+\.\d+表示IP,可能比较简单 可以优化一下
]

```

tutorial/urls.py文件中添加一行

```python
path('physical_machine/', include('physical_machine.urls')),
```

![image-20230412141453090](C:\Users\dell\AppData\Roaming\Typora\typora-user-images\image-20230412141453090.png)

### 3.6、发起请求验证

直接从文档中验证或者使用postman或apipost验证都可以

获取所有物理机信息

![image-20230412143701502](C:\Users\dell\AppData\Roaming\Typora\typora-user-images\image-20230412143701502.png)

获取某个物理机信息

![image-20230412144334370](C:\Users\dell\AppData\Roaming\Typora\typora-user-images\image-20230412144334370.png)

获取不存在的机器

![image-20230412144357284](C:\Users\dell\AppData\Roaming\Typora\typora-user-images\image-20230412144357284.png)

接口文档

![image-20230412144435090](C:\Users\dell\AppData\Roaming\Typora\typora-user-images\image-20230412144435090.png)

[github](https://github.com/rainbow-tan/learn-drf)