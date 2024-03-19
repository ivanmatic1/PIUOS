from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.Serializer): #seriaizer za registraciju korisnika
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username  =  serializers.CharField()
    password = serializers.CharField()


    def validate(self, data): #funkcija za validiranje korisnika
        
        if User.objects.filter(username = data['username']).exists(): #ukoliko korisnik upise username koji je već u bazi, javlja poruku
            raise serializers.ValidationError('Username is taken')
        
        return data #else vraća unesene podatke
    
    def create(self, validated_data): #funkcija za kreiranje accounta
        user = User.objects.create(first_name = validated_data['first_name'],
            last_name =  validated_data['last_name'],
            username = validated_data['username'].lower()                
        )
        user.set_password(validated_data['password'])
        user.save()
        return validated_data
    
class LoginSerializer(serializers.Serializer): #serializer za login korisnika
    username  =  serializers.CharField()
    password = serializers.CharField()

    def validate(self, data): #funkcija za validiranje korisnika
        
        if not User.objects.filter(username = data['username']).exists(): #ukoliko korisnik upise krivi username, javlja poruku
            raise serializers.ValidationError('Account not found')
        
        return data #else vraća unesene podatke
    
    def get_jwt_token(self, data): #funkcija za dohvacanje jwt tokena
        user = authenticate(username = data['username'], password = data['password'])

        if not user:
            return{'message' : 'Invalid credentials', 'data' : {}}
        refresh = RefreshToken.for_user(user)

        return {'message':'Login succesfull!', 'data':{'token':{
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }}}

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
            validated_data.pop('password')
        return super().update(instance, validated_data)
    
class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','first_name','last_name']