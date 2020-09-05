from rest_framework import serializers
from .models import User
from datetime import datetime

from .models import (
    Featured,
    DeviceBrand,
    DeviceModel,
    DeviceColor,
    Device,
    Artwork,
    Phonecase,
    PhonecasePrice,
    PhonecaseColor,
    PhonecaseType,
    PhonecaseColorDeivce,
    PhonecaseImage,
    PhonecaseReview
)
from user.models import User
from order.models import Order, Orderer, CheckoutStatus, CheckOut, Cart

from user.serializers import UserSerializer


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


class FeaturedSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Featured
        fields = '__all__'


class DeviceModelSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = DeviceModel
        fields = '__all__'


class PhonecaseColorSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = PhonecaseColor
        fields = '__all__'


class PhonecaseTypeSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = PhonecaseType
        fields = '__all__'


class ArtworkSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Artwork
        fields = '__all__'


class PhonecaseSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Phonecase
        fields = '__all__'


class PhonecasePriceSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = PhonecasePrice
        fields = '__all__'

