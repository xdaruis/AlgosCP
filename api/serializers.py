from rest_framework import serializers

class CodeSubmissionSerializer(serializers.Serializer):
    problem_id = serializers.IntegerField()
    code = serializers.CharField()
    base_path = serializers.CharField()
    number_of_testcases = serializers.IntegerField()
    time_limit = serializers.IntegerField()
