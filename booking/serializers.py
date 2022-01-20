from rest_framework import serializers
from .models import Booking, Reason


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'


class ReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reason
        fields = ['user_id', 'booking_id', 'type', 'reason', 'message']
