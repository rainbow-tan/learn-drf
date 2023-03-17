from rest_framework import serializers

from student_manager.models import Student


# class StudentSerializer(serializers.Serializer):
#
#     def update(self, instance, validated_data):
#         print(f"StudentSerializer update instance:{instance}, type:{type(instance)}")
#         print(f"StudentSerializer update validated_data:{validated_data}, type:{type(validated_data)}")
#         instance.student_id = validated_data.get('student_id', instance.student_id)
#         instance.student_name = validated_data.get('student_name', instance.student_name)
#         instance.student_sex = validated_data.get('student_sex', instance.student_sex)
#         instance.student_birthday = validated_data.get('student_birthday', instance.student_birthday)
#         instance.save()
#         return instance
#
#     student_id = serializers.CharField()
#     student_name = serializers.CharField()
#     student_sex = serializers.IntegerField()
#     student_birthday = serializers.DateField()
#
#     id = serializers.IntegerField(required=False)
#     created = serializers.DateTimeField(required=False)
#     updated = serializers.DateTimeField(required=False)
#
#     class Meta:
#         fields = '__all__'
#
#     def create(self, validated_data):
#         print(f"StudentSerializer create validated_data:{validated_data}, type:{type(validated_data)}")
#         instance = Student.objects.create(**validated_data)
#         return instance

class StudentSerializer(serializers.ModelSerializer):
    game_id = serializers.CharField(read_only=True)

    class Meta:
        model = Student
        fields = '__all__'
