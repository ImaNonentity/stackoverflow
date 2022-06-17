# from django.contrib.contenttypes.models import ContentType
# from rest_framework import serializers
# from .models import Vote
from vote.models import Vote
from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType

from vote.services import VotingCountSystem

CONTENT_TYPES_MODEL = ['question', 'answer']


class VoteSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    content_type = serializers.SlugRelatedField(queryset=ContentType.objects.filter(model__in=CONTENT_TYPES_MODEL),
                                                slug_field='model')
    object_id = serializers.IntegerField()
    action_type = serializers.IntegerField()
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Vote
        fields = ['id', 'user', 'object_id', 'content_type', 'action_type', 'created_at', 'updated_at']

    def validate(self, attrs):
        try:
            attrs['content_object'] = attrs['content_type'].model_class().objects.get(pk=attrs['object_id'])
        except:
            raise serializers.ValidationError(
                {'object_id': ['Invalid pk "' + str(attrs['object_id']) + '" - object does not exist.']})
        if attrs['action_type'] not in Vote.RATING_CHOICES_LIST_INT:
            raise serializers.ValidationError(
                {'action_type': [f'Invalid action type {attrs["action_type"]} '
                                 f'- action type must be in {", ".join(Vote.RATING_CHOICES_LIST_STR)}']}
            )
        return attrs

    def create(self, validated_data):
        print("I'm here!")
        return Vote.objects.create(**validated_data)

    def update(self, instance, validated_data):
        print(f'"its pickle rick boom big reveal" {validated_data}')
        # voting_system = VotingCountSystem(user=instance.user, data=validated_data)
        # instance = voting_system.update_vote()
        print(instance.action_type)
        instance.action_type = validated_data.get('action_type', instance.action_type)
        print(instance.action_type)
        instance.save()

        return instance

