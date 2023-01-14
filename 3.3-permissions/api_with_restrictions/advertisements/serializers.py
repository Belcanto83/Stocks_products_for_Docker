from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from advertisements.models import Advertisement, AdvertisementStatusChoices


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""
    creator = UserSerializer(
        read_only=True
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', )

    def create(self, validated_data):
        """Метод для создания"""

        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""
        MAX_OPEN_ADV = 10

        adv_count = Advertisement.objects.filter(creator=self.context['request'].user,
                                                 status=AdvertisementStatusChoices.OPEN).count()
        if adv_count >= MAX_OPEN_ADV:
            if self.context["request"].method == 'POST':
                raise ValidationError(
                    f'Not allowed. Q-ty {adv_count} of open advs >= {MAX_OPEN_ADV} (max. possible q-ty)'
                )
            elif self.context["request"].method in ['PUT', 'PATCH'] and \
                    data['status'] == AdvertisementStatusChoices.OPEN:
                raise ValidationError(
                    f'Not allowed. Q-ty {adv_count} of open advs >= {MAX_OPEN_ADV} (max. possible q-ty)'
                )

        return data
