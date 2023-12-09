from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers, fields
from mailes.models import Mail, Financial, Marriage, Messages
from rest_framework.fields import Field


class FinancialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Financial
        fields = ['origin_card_number', 'destination_card_number', 'amount']


class MarriageSerializer(serializers.ModelSerializer):
    # date_marriage = fields.DateField(input_formats=['%Y-%m-%dT%H:%M:%S.%fZ'])
    class Meta:
        model = Marriage
        fields = ['picture_women_id', 'women_name', 'date_marriage']


class RecurringMeetingRelatedField(Field):
    def to_representation(self, value):
        if isinstance(value, Financial):
            serializer = FinancialSerializer(value)
        elif isinstance(value, Marriage):
            serializer = MarriageSerializer(value)
        else:
            raise Exception('Unexpected type of tagged object')
        return serializer.data

    def to_internal_value(self, data):
        # if not isinstance(data, dict):
        #     raise serializers.ValidationError('Invalid data type provided')

        meeting_type = data.pop('meeting_type', None)
        print(meeting_type)

        if meeting_type == 'financial':
            print(1)
            serializer = FinancialSerializer(data=data)
        elif meeting_type == 'marriage':
            print(2)
            serializer = MarriageSerializer(data=data)
        else:
            print(3)
            raise serializers.ValidationError('no meeting_type provided')

        if serializer.is_valid():
            obj = serializer.save()
        else:
            raise serializers.ValidationError(serializer.errors)

        return obj


class MailSerializer(serializers.ModelSerializer):
    recurring_meeting = RecurringMeetingRelatedField(required=False)

    class Meta:
        model = Mail
        fields = ['id', 'subject', 'description', 'created_at', 'attachment', 'owner', 'is_accepted',
                  'type', 'updated_at', 'user', 'reason', 'recurring_meeting', 'object_id']

    def create(self, validated_data):
        meeting_type = validated_data.pop('recurring_meeting')
        type = validated_data.pop('type', None)
        object_id = validated_data.pop('object_id', None)
        print(isinstance(meeting_type, Marriage))
        if isinstance(meeting_type, Financial):
            print(4)
            serializer = FinancialSerializer(data=meeting_type)
        elif isinstance(meeting_type, Marriage):
            print(5)
            serializer = MarriageSerializer(data=meeting_type)
        else:
            print(6)
            raise serializers.ValidationError('Invalid meeting_type provided')

        # if serializer.is_valid():
        #     instance = serializer.save()
        # else:
        #     raise serializers.ValidationError(serializer.errors)

        type = ContentType.objects.get_for_model(meeting_type)

        mail = Mail.objects.create(content_type=type, object_id=meeting_type.id, **validated_data)

        return mail
    # def validate(self, data):


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messages
        fields = ['user', 'description', 'attachment', 'is_accepted', 'mail', 'unread','meta_data']
