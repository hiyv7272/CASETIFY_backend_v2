from rest_framework import serializers

from user.models import User
from .models import Order, Orderer, Cart, CheckoutStatus, CheckOut
from datetime import datetime

from .models import Order, Orderer, CheckoutStatus, CheckOut, Cart
from user.models import User
from artwork.models import Phonecase, PhonecasePrice

from user.serializers import UserSerializer
from artwork.serializers import (
    PhonecaseSerializer,
    PhonecasePriceSerializer,
    FeaturedSerializer,
    DeviceModelSerializer,
    PhonecaseColorSerializer,
    PhonecaseTypeSerializer,
    ArtworkSerializer,
)


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

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['USER'] = UserSerializer(instance.USER).data
        response['PHONECASE'] = PhonecaseSerializer(instance.PHONECASE).data
        response['PHONECASE_PRICE'] = PhonecasePriceSerializer(instance.PHONECASE_PRICE).data
        response['PHONECASE']['FEATURED'] = FeaturedSerializer(instance.PHONECASE.FEATURED).data
        response['PHONECASE']['DEVICE_MODEL'] = DeviceModelSerializer(instance.PHONECASE.DEVICE_MODEL).data
        response['PHONECASE']['PHONECASE_COLOR'] = PhonecaseColorSerializer(instance.PHONECASE.PHONECASE_COLOR).data
        response['PHONECASE']['PHONECASE_TYPE'] = PhonecaseTypeSerializer(instance.PHONECASE.PHONECASE_TYPE).data
        response['PHONECASE']['ARTWORK'] = ArtworkSerializer(instance.PHONECASE.ARTWORK).data
        return response


class OrderSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


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


class CartSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

    def insert_cart_validate(self, data):
        if not PhonecasePrice.objects.get(PHONECASE=data['phonecase_id']):
            raise serializers.ValidationError({'message': "INVALID_VALUE"})

        if data['is_custom'] > 1:
            raise serializers.ValidationError({'message': "INVALID_VALUE"})

        if data['is_custom'] == 1:
            if len(data['custom_info']) == 0:
                raise serializers.ValidationError({'message': "INVALID_VALUE"})

        return data

    def create(self, validated_data):
        try:
            Cart.objects.create(
                USER=User.objects.get(id=validated_data['id']),
                PHONECASE=Phonecase.objects.get(id=validated_data['phonecase_id']),
                PHONECASE_PRICE=PhonecasePrice.objects.get(PHONECASE=validated_data['phonecase_id']),
                is_custom=validated_data['is_custom'],
                custom_info=validated_data['custom_info'],
                quantity=validated_data['quantity'],
                is_use=True
            )

            return Cart

        except TypeError:
            raise serializers.ValidationError({'message': 'INVALID_HASHED'})
        except KeyError:
            raise serializers.ValidationError({'message': 'INVALID_KEYS'})


class CheckoutStatusSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = CheckoutStatus
        fields = '__all__'


class CheckOutSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = CheckOut
        fields = '__all__'
