from rest_framework import serializers

from users.models import Payment, User


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    payment_history = PaymentSerializer(source='user_payment', many=True, read_only=True)

    class Meta:
        model = User
        fields = '__all__'

    def get_payment_history(self, instance):
        return PaymentSerializer(instance.payment_history, many=True).data


class UserViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)
