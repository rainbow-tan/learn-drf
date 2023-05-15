from rest_framework import serializers


class MachineSerializer(serializers.Serializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    ip = serializers.CharField()
    # host = serializers.CharField(source='ip')  # 实现更改key的方式 通过指定 source字段 则key ip就变成了key host了
    core = serializers.IntegerField()
    memory = serializers.CharField()
    disk = serializers.CharField()
