from rest_framework import mixins, generics

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

class StudentList(generics.GenericAPIView,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  ):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class StudentDetail(generics.GenericAPIView,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
