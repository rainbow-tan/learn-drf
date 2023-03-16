django-rest-framework-从零开始-3

## 1、前言

我们之前提到创建序列化类，需要继承`serializers.Serializer`类，然后映射`模型类`的字段，然后重写`create`方法和`update`方法。这样的代码，看起来映射字段有一些重复代码，而且`create`和`update`方法，遇到一个模型，需要重写一次，太麻烦了。

因此，我们可以使用`serializers.ModelSerializer`类代替`serializers.Serializer`类

## 2、使用`ModelSerializer`类代替`Serializer`类

- 重写`student_manager/serializers.py`文件中的`StudentSerializer`类

```python
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
```

图示

![image-20230316155825121](C:\Users\dell\AppData\Roaming\Typora\typora-user-images\image-20230316155825121.png)

- 查看自动生成的序列化类

  在`student_manager/debug_student_serializer.py`中添加以下代码

  ```python
  def show_serializer():
      serializer = StudentSerializer()
      print(f"serializer:{serializer}")
  ```

图示

![image-20230316160628845](C:\Users\dell\AppData\Roaming\Typora\typora-user-images\image-20230316160628845.png)

运行后

```python
serializer:StudentSerializer():
    id = IntegerField(read_only=True)
    student_id = CharField(help_text='学号最大长度为30', label='学号', max_length=30, validators=[<UniqueValidator(queryset=Student.objects.all())>])
    student_name = CharField(help_text='学号最大长度为30', label='姓名', max_length=30)
    student_sex = ChoiceField(choices=[(1, '男'), (0, '女')], help_text='1->男,0->女', label='性别')
    student_birthday = DateField(help_text='学生生日', label='生日')
    created = DateTimeField(label='创建时间', read_only=True)
    updated = DateTimeField(label='修改时间', read_only=True)
```

![image-20230316160249218](C:\Users\dell\AppData\Roaming\Typora\typora-user-images\image-20230316160249218.png)

说明：

- 通过Meta类中的model指定要序列化的模型类即可

- 完美的把模型类搬过来了，还添加了唯一属性校验器，帮助信息，标签等信息，比自己手动写序列化类方便多了，同时还重写了create方法和update方法，直接在源代码中就可以看到。

github：https://github.com/rainbow-tan/learn-drf