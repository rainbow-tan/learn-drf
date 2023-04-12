from django.urls import path, re_path

from physical_machine.views import MachineViewSet

urlpatterns = [
    path('', MachineViewSet.as_view(dict(get='list'))),
    re_path(r"(?P<pk>\d+\.\d+\.\d+\.\d+)/", MachineViewSet.as_view({"get": "retrieve"})),
    # 路由的\d+\.\d+\.\d+\.\d+表示IP,可能比较简单 可以优化一下
]
