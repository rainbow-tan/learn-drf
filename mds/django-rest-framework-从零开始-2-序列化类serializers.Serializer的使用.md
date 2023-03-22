django-rest-framework-从零开始-2-序列化类serializers.Serializer的使用

## 1、前言

我们编写的django程序，需要与前端或者其他程序交互，通常会提供出自己的API接口，此时需要把程序中的对象，转换为JSON字符串，然后返回，让对接同事获取到数据。

把对象转化为JSON字符串的过程，称之为序列化。一般就是把数据库中的数据，转换为模型对象，模型对象再转换为JSON字符串。

## 2、创建序列化类

添加student_manager/serializers.py文件，添加以下内容

```python
from rest_framework import serializers

from student_manager.models import Student


class StudentSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    student_id = serializers.CharField()
    student_name = serializers.CharField()
    student_sex = serializers.IntegerField()
    student_birthday = serializers.DateField()

    id = serializers.IntegerField(required=False)
    created = serializers.DateTimeField(required=False)
    updated = serializers.DateTimeField(required=False)

    class Meta:
        fields = '__all__'

    def create(self, validated_data):
        print(f"StudentSerializer create validated_data:{validated_data}, type:{type(validated_data)}")
        instance = Student.objects.create(**validated_data)
        return instance
```

​	图示

![image-20230316144005325](https://img2023.cnblogs.com/blog/1768648/202303/1768648-20230321152418064-1820059071.png)

说明：

- 创建序列化类，只需要继承`serializers.Serializer`类，重写`create`方法和`update`方法即可。其中，`create`方法用于保存模型对象到数据库，`update`方法用于更新模型对象到数据库，这里先重写`create`方法，用于保存模型对象，`update`方法，后续再补充。
- `StudentSerializer`序列化类，本意就是序列化`Student`模型，因此，这里需要把`Student`模型中的字段，都映射过来，映射方式就是把`Student`模型的属性都搬过来，这样看起来，代码重复了，没关系，后续会优化，现在先理解一下原理。

这样就完成了序列化类的编写，接下来，我们写一个测试脚本，测试一下，用序列化类添加一条记录到数据库

## 3、使用序列化类添加数据

我们添加一条数据到数据库，即添加一个`Student`模型对象，并保存到数据库中。

创建`student_manager/debug_student_serializer.py`文件，添加以下内容

```python
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tutorial.settings')
import django

django.setup()
from student_manager.serializers import StudentSerializer


def add_student():
    data = dict(student_id="1001",
                student_name="小红",
                student_sex=1,
                student_birthday="2020-1-1")
    serializer = StudentSerializer(data=data)
    print(f"serializer:{serializer}")

    serializer.is_valid(True)  # 判断数据是否合法
    serializer.save()  # 调用save方法, 会调用到序列化类中的create方法


if __name__ == '__main__':
    add_student()
```

图示：

![image-20230316145312429](https://img2023.cnblogs.com/blog/1768648/202303/1768648-20230321152418526-47669745.png)

说明：

- 我们需要创建一个`Student`模型对象，因此，需要把student_id、student_name、student_sex、student_birthday都定义好，然后传递给`StudentSerializer`序列化类

- 传递给序列化类后，调用`is_valid`方法校验一下数据是否合法，这里的校验类似于模型中的校验，比如必填，非必填，是否在选项中等。我们之前定义的`StudentSerializer`序列化类，没有额外的校验，甚至，我们申明了id、created、updated为非必填，因为我们直接让数据库自己填充就可以了。
- 最后调用save方法，save方法会调用之前重写的create方法。从源代码中就可以看出来。
- **我们也可以给save方法传递参数，参数会传递下去，通过create方法进行使用，这个用法可以记录一下，有时候有奇效**

运行`student_manager/debug_student_serializer.py`文件，就可以看到数据库新增了一条数据

![image-20230316150335443](https://img2023.cnblogs.com/blog/1768648/202303/1768648-20230321152418855-183768675.png)

## 4、使用序列化类序列化对象

接下来，我们使用序列化类，显示数据库的数据，首先是加载成模型对象，接下来转化为序列化类对象，最后转为JSON字符串，即可。最终通过API返回数据。

- 先往数据库中添加几条数据

  ![image-20230316151219631](https://img2023.cnblogs.com/blog/1768648/202303/1768648-20230321152419175-1358464259.png)

- 在`student_manager/debug_student_serializer.py`中添加以下代码

  ```python
  from student_manager.models import Student
  from rest_framework.renderers import JSONRenderer
  ```

  ```python
  def list_student():
      instance = Student.objects.get(student_id="1001")
      serializer = StudentSerializer(instance=instance)
      data = serializer.data
      print(f'data:{data}')
      content = JSONRenderer().render(serializer.data)
      print(f'content:{content}')
  ```

  图示
  
  ![image-20230316151753510](https://img2023.cnblogs.com/blog/1768648/202303/1768648-20230321152419549-362161912.png)

说明：使用`Student`模型获取到数据库数据后，传递给`StudentSerializer`序列化类，序列化类的`data`数据就是对象的序列化信息，再通过`JSONRenderer`转为JSON字符串即可

- 序列化多条数据，只需要传递`many=True`即可

```python
def list_all_students():
    instance = Student.objects.all()
    serializer = StudentSerializer(instance=instance, many=True)
    data = serializer.data
    print(f'data:{data}')
    content = JSONRenderer().render(serializer.data)
    print(f'content:{content.decode("utf-8")}')
```

## 5、使用序列化类修改数据

要想修改数据，步骤：

1. 重写序列化类中的`update`方法
2. 从数据库获取数据，转化为模型对象
3. 模型对象传递给序列化类
4. 调用序列化类的`save`方法，当调用save方法时，如果传递了instance对象，则调用序列化类的update方法，否则调用序列化类的create方法。**同理，可以给save方法传递额外参数，在update函数中使用，这个用法可以记录一下，有时候有奇效**

- 因此修改`student_manager/serializers.py`中的`update`方法

```python
def update(self, instance, validated_data):
    print(f"StudentSerializer update instance:{instance}, type:{type(instance)}")
    print(f"StudentSerializer update validated_data:{validated_data}, type:{type(validated_data)}")
    instance.student_id = validated_data.get('student_id', instance.student_id)
    instance.student_name = validated_data.get('student_name', instance.student_name)
    instance.student_sex = validated_data.get('student_sex', instance.student_sex)
    instance.student_birthday = validated_data.get('student_birthday', instance.student_birthday)
    instance.save()
    return instance
```

图示

![image-20230316153807200](https://img2023.cnblogs.com/blog/1768648/202303/1768648-20230321152419889-907070381.png)

- 在`student_manager/debug_student_serializer.py`中添加代码

  ```python
  def update_student():
      data = dict(student_id="1009",
                  student_name="小红rename",
                  student_sex=1,
                  student_birthday="2020-1-19")
      instance = Student.objects.get(student_id="1001")
      serializer = StudentSerializer(instance=instance, data=data)
      serializer.is_valid(True)
      serializer.save()  # 调用save方法, 会调用到序列化类中的update方法(传递instance参数时)
  ```

图示

![image-20230316153952599](https://img2023.cnblogs.com/blog/1768648/202303/1768648-20230321152420246-249912453.png)

最后运行`student_manager/debug_student_serializer.py`，查看数据库数据

![image-20230316154031457](https://img2023.cnblogs.com/blog/1768648/202303/1768648-20230321152420616-2136743753.png)

github：https://github.com/rainbow-tan/learn-drf