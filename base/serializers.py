from rest_framework.serializers import ModelSerializer
from customer.models import User

class BaseSerializer(ModelSerializer):

    def create(self, validated_data):
        user = self.context.get('request').user
        if isinstance(user, User):
            validated_data['author_create'] = self.context.get('request').user
        return self.Meta.model.objects.create(**validated_data)

    def update(self, instance, validated_data):
        user = self.context.get('request').user
        if isinstance(user, User):
            instance.author_update = self.context.get('request').user
        instanse.save()
        return instance

