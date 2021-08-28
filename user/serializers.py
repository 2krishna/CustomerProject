
from rest_framework import serializers
from user.models import User,Product
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'phone_no', 'gender')
        # extra_kwargs = {
        #     'first_name': {'required': True},
        #     'last_name': {'required': True}
        # }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            phone_no=validated_data['phone_no'],
            gender=validated_data['gender']
        )

        
        user.set_password(validated_data['password'])
        user.save()

        return user



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['username'] = user.username
        return token


class ProductSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    class Meta:
        model=Product
        #fields='__all__'
        fields=['id','name','image','description','currency','price']

    def get_image(self,obj):
        return f'http://127.0.0.1:8000/media/{obj.image}'


class ProductCreateSerializer(serializers.ModelSerializer):
    # image = serializers.SerializerMethodField()
    class Meta:
        model=Product
        #fields='__all__'
        fields=['id','name','image','description','currency','price']

    # def get_image(self,obj):
    #     return f'http://127.0.0.1:8000/media/{obj.image}'