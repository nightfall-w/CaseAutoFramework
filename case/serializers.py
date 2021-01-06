from rest_framework import serializers
from case.models import GitlabModel, GitCaseModel


class GitlabAuthenticationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GitlabModel
        fields = '__all__'
        depth = 1


class GitlabBranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = GitCaseModel
        fields = '__all__'
        depth = 1

    # def create(self, validated_data):
    #     return GitCaseModel.objects.create(**self.context['request'].data)

# class CaseTypeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CaseTypeModel
#         fields = '__all__'
#         depth = 1
#
#
# class CaseSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CaseModel
#         exclude = ['create_time']
#         depth = 2
#
#     def create(self, validated_data):
#         return CaseModel.objects.create(**self.context['request'].data)


# class CodeBaseSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CodeBaseModel
#         fields = '__all__'
#         depth = 1
#         validators = [
#             UniqueTogetherValidator(
#                 queryset=CodeBaseModel.objects.all(),
#                 fields=('address',),
#                 message="已经存在相同地址的代码仓库"
#             )
#         ]
