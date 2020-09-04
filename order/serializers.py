from rest_framework import serializers

from user.models import User
from .models import Order, Orderer
from datetime import datetime


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """
    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)
        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)
        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class OrdererSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Orderer
        fields = '__all__'

    def create(self, validated_data):
        try:
            Orderer(
                USER=User.objects.get(email=validated_data['email'])
            ).save()

            return Orderer

        except TypeError:
            raise serializers.ValidationError({'message': 'INVALID_HASHED'})
        except KeyError:
            raise serializers.ValidationError({'message': 'INVALID_KEYS'})

    def get(self, validated_data):
        try:
            orderer = Orderer.objects.get(email=validated_data['email'])

            return orderer

        except TypeError:
            raise serializers.ValidationError({'message': 'INVALID_HASHED'})
        except KeyError:
            raise serializers.ValidationError({'message': 'INVALID_KEYS'})

    def update(self, instance, validated_data):
        try:
            instance.first_name = validated_data.get('first_name', instance.first_name)
            instance.last_name = validated_data.get('last_name', instance.last_name)
            instance.address = validated_data.get('address', instance.address)
            instance.zipcode = validated_data.get('zipcode', instance.zipcode)
            instance.update_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            instance.save()

            return instance
        except TypeError:
            raise serializers.ValidationError({'message': 'INVALID_HASHED'})
        except KeyError:
            raise serializers.ValidationError({'message': 'INVALID_KEYS'})
