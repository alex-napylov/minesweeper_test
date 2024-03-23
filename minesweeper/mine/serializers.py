from rest_framework import serializers


class MineSerializerResponse(serializers.Serializer):
    """ Сериализатор ответа """
    game_id = serializers.CharField()
    width = serializers.IntegerField()
    height = serializers.IntegerField()
    mines_count = serializers.IntegerField()
    completed = serializers.BooleanField()
    field = serializers.ListField()


class MineSerializerNew(serializers.Serializer):
    """ Сериализатор POST запроса endpoint-а: api/new """
    width = serializers.IntegerField(max_value=30)
    height = serializers.IntegerField(max_value=30)
    mines_count = serializers.IntegerField()


class MineSerializerTurn(serializers.Serializer):
    """ Сериализатор POST запроса endpoint-а: api/turn """
    game_id = serializers.CharField()
    col = serializers.IntegerField()
    row = serializers.IntegerField()

