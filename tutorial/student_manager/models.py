from django.db import models


class Student(models.Model):
    student_id = models.CharField(verbose_name="学号", max_length=30, unique=True, null=False, blank=False,
                                  db_index=True, help_text="学号最大长度为30")
    student_name = models.CharField("姓名", max_length=30, unique=False, null=False, blank=False,
                                    db_index=True, help_text="学号最大长度为30")
    student_sex = models.SmallIntegerField("性别", choices=[(1, '男'), (0, '女')], null=False, blank=False,
                                           help_text="1->男,0->女")
    student_birthday = models.DateField("生日", null=False, blank=False, help_text="学生生日")

    id = models.AutoField(primary_key=True)
    created = models.DateTimeField("创建时间", auto_now_add=True)
    updated = models.DateTimeField("修改时间", auto_now=True)

    class Meta:
        db_table = 't_student'

    def __str__(self):
        return f"Student({self.student_id}->{self.student_name})"

    def __repr__(self):
        return self.__str__()

    """
    学习链接
    https://blog.csdn.net/Mikowoo007/article/details/98203653
    官网 https://docs.djangoproject.com/zh-hans/4.1/ref/models/fields/
    """
