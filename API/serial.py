from rest_framework import serializers
from .models import Registration
import datetime

class RegistrationSerialization(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}
    def create(self, validated_data):
        print(validated_data)
        user = Registration.objects.create_user(username=validated_data['email'],email=validated_data['email'], password=validated_data['password'],first_name=validated_data['first_name'],last_name=validated_data['last_name'],mobile_number = validated_data['mobile_number'], date_of_birth = datetime.datetime.strptime(validated_data['date_of_birth'], '%Y-%m-%d').date())
        return user

class RegisterInputSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required = True, allow_blank = False)
    last_name = serializers.CharField(required = True, allow_blank = False)
    email = serializers.EmailField(required = True, allow_blank = False)
    mobile_number = serializers.CharField(required = True, allow_blank = False)
    date_of_birth  = serializers.DateField(required = False)

    class Meta:
        model = Registration
        fields = ('first_name', 'last_name', 'email', 'password', 'mobile_number', 'date_of_birth')
        extra_kwargs = {'password': {'write_only': True}}

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = ( 'email', 'password')

class ChangePasswordSerial(serializers.ModelSerializer):
    currentpassword=serializers.CharField(max_length=30)
    new_password=serializers.CharField(max_length=30,min_length=4)
    confirmpassword=serializers.CharField(max_length=20,min_length=4)
    
    class Meta:
        model = Registration
        fields = ['currentpassword','new_password','confirmpassword']
    