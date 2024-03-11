from rest_framework import serializers
from django.contrib.auth.models import User


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

        return validated_data