from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import CodeSubmissionSerializer
from .utils.submission_evaluation import test_submission_script

@api_view(['POST'])
def test_submission(request):
    serializer = CodeSubmissionSerializer(data = request.data)
    if serializer.is_valid():
        problem_id = serializer.validated_data['problem_id']
        code = serializer.validated_data['code']
        base_path = serializer.validated_data['base_path']
        number_of_testcases = serializer.validated_data['number_of_testcases']
        time_limit = serializer.validated_data['time_limit']
        inputs = serializer.validated_data['inputs']
        correct_outputs = serializer.validated_data['correct_outputs']
        results = test_submission_script(inputs, correct_outputs, problem_id, code, base_path, number_of_testcases, time_limit)
        return Response({'results': results}, status = status.HTTP_200_OK)
    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
