from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from student_manager.models import Student
from student_manager.serializers import StudentSerializer


@api_view(['GET', 'POST'])
def students_list(request: Request):
    if request.method == 'GET':
        result = Student.objects.all()
        serializer = StudentSerializer(result, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = request.data
        serializer = StudentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
