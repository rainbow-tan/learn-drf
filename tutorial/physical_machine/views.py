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
