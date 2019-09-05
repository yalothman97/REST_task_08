from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Flight, Booking, Profile

from django.utils import timezone

from datetime import date


class FlightSerializer(serializers.ModelSerializer):
	class Meta:
		model = Flight
		fields = ['destination', 'time', 'price', 'id']


class BookingSerializer(serializers.ModelSerializer):
	flight = serializers.SlugRelatedField(
	    read_only=True,
	    slug_field='destination'
	 )

	class Meta:
	    model = Booking
	    fields = ['flight', 'date', 'id']


class BookingDetailsSerializer(serializers.ModelSerializer):
	total = serializers.SerializerMethodField()
	flight = FlightSerializer()
	class Meta:
		model = Booking
		fields = ['flight', 'date', 'passengers', 'id','total']

	def get_total(self,obj):
		return obj.passengers * obj.flight.price


class AdminUpdateBookingSerializer(serializers.ModelSerializer):
	class Meta:
		model = Booking
		fields = ['date', 'passengers']


class UpdateBookingSerializer(serializers.ModelSerializer):
	class Meta:
		model = Booking
		fields = ['passengers']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        new_user = User(username=username, first_name=first_name, last_name=last_name)
        new_user.set_password(password)
        # Profile.objects.create(user=new_user)
        new_user.save()
        return validated_data

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['first_name','last_name']


class ProfileSerializer(serializers.ModelSerializer):
	user = UserSerializer()
	past_bookings = serializers.SerializerMethodField()
	tier = serializers.SerializerMethodField()
	class Meta:
		model = Profile
		fields = ['user', 'miles','past_bookings', 'tier',]


	def get_past_bookings(self, obj):
		bookings = obj.user.bookings.filter(date__lt=timezone.now())
		return BookingSerializer(bookings, many = True).data

	def get_tier(self,obj):
		miles = obj.miles
		if miles <= 9999 and miles >= 0:
			return "Blue"
		elif miles <= 59999 and miles >= 10000:
			return 'Silver'
		elif miles <= 99999 and miles >= 60000:
			return 'Gold'
		else:
			return 'Platinum'
		 

