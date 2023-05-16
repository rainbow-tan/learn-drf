from rest_framework.viewsets import ModelViewSet

from student_manager.filter import StudentFilter
from student_manager.models import Student
from student_manager.serializers import StudentSerializer


# @api_view(['GET', 'POST'])
# def student_list(request: Request):
#     if request.method == 'GET':
#         result = Student.objects.all()
#         serializer = StudentSerializer(result, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         data = request.data
#         serializer = StudentSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(['GET', 'PUT', 'DELETE'])
# def student_detail(request, pk):
#     try:
#         student = Student.objects.get(pk=pk)
#     except Student.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'GET':
#         serializer = StudentSerializer(student)
#         return Response(serializer.data)
#
#     elif request.method == 'PUT':
#         serializer = StudentSerializer(instance=student, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     elif request.method == 'DELETE':
#         student.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# class StudentList(APIView):
#     @staticmethod
#     def get(request):
#         result = Student.objects.all()
#         serializer = StudentSerializer(result, many=True)
#         return Response(serializer.data)
#
#     @staticmethod
#     def post(request):
#         data = request.data
#         serializer = StudentSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class StudentDetail(APIView):
#     @staticmethod
#     def get_object(pk):
#         try:
#             return Student.objects.get(pk=pk)
#         except Student.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk):
#         obj = self.get_object(pk)
#         serializer = StudentSerializer(instance=obj)
#         return Response(serializer.data)
#
#     def put(self, request, pk):
#         snippet = self.get_object(pk)
#         serializer = StudentSerializer(snippet, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk):
#         obj = self.get_object(pk)
#         obj.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# class StudentList(generics.GenericAPIView,
#                   mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   ):
#     queryset = Student.objects.all()
#     serializer_class = StudentSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
#
#
# class StudentDetail(generics.GenericAPIView,
#                     mixins.RetrieveModelMixin,
#                     mixins.UpdateModelMixin,
#                     mixins.DestroyModelMixin):
#     queryset = Student.objects.all()
#     serializer_class = StudentSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
#
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
#
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)

# class StudentList(generics.ListCreateAPIView):
#     queryset = Student.objects.all()
#     serializer_class = StudentSerializer
#
#     def list(self, request, *args, **kwargs):
#         queryset = self.filter_queryset(self.get_queryset())
#         page = self.paginate_queryset(queryset)
#         if page is not None:
#             serializer = self.get_serializer(page, many=True)
#             return self.get_paginated_response(serializer.data)
#         serializer = self.get_serializer(queryset, many=True)
#         for one in serializer.data:
#             one['game_id'] = uuid.uuid4().hex
#         return Response(serializer.data)
#
#
# class StudentDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Student.objects.all()
#     serializer_class = StudentSerializer
#
#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance)
#         data = serializer.data
#         data['game_id'] = uuid.uuid4().hex
#         return Response(data)

class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    # filter_backends = [DjangoFilterBackend]  # 仅使用该类过滤
    # filterset_fields = ['student_name', 'student_sex', 'student_birthday']  # 过滤的字段
    filter_class = StudentFilter
