from rest_framework import serializers


class MachineSerializer(serializers.Serializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    ip = serializers.CharField()
    # host = serializers.CharField(source='ip')
    core = serializers.IntegerField()
    memory = serializers.CharField()
    disk = serializers.CharField()


