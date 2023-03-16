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
