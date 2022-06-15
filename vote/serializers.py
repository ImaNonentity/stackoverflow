from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from .models import Vote

CONTENT_TYPES_MODEL = ['question', 'answer']
rating_choice = (
    ('1', 1),
    ('0', 0),
    ('-1', -1)
)


class VoteSerializer(serializers.ModelSerializer):
    content_type = serializers.SlugRelatedField(queryset=ContentType.objects.filter(model__in=CONTENT_TYPES_MODEL),
                                                slug_field='model')
    object_id = serializers.IntegerField()
    action_type = serializers.IntegerField()

    class Meta:
        model = Vote
        fields = '__all__'

    def validate(self, attrs):
        try:
            attrs['content_object'] = attrs['content_type'].model_class().objects.get(pk=attrs['object_id'])
        except:
            raise serializers.ValidationError(
                {'object_id': ['Invalid pk "' + str(attrs['object_id']) + '" - object does not exist.']})
        return attrs
