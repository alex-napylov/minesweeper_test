import uuid

from rest_framework import status
from rest_framework import views
from rest_framework.response import Response
from django.core.cache import cache

from .serializers import MineSerializerResponse, MineSerializerNew, MineSerializerTurn

from mine.game import Minesweeper


class MineAPIViewNew(views.APIView):
    """ Представление для endpoint-a /api/new """
    def post(self, request, *args, **kwargs):
        serializer = MineSerializerNew(data=request.data)
        if serializer.is_valid():
            game = Minesweeper(serializer.data['width'], serializer.data['height'], serializer.data['mines_count'])
            # Генерация game_id с помощью модуля uuid
            game_id = str(uuid.uuid4())
            game.game_id = game_id
            width = serializer.data['width']
            height = serializer.data['height']
            mines_count = serializer.data['mines_count']
            # Установка кеша перед отправкой ответа
            cache.set('game', game)

            response = Response(MineSerializerResponse({'game_id': game_id,
                                                        'width': width,
                                                        'height': height,
                                                        'mines_count': mines_count,
                                                        'completed': False,
                                                        'field': game.board}).data)
            return response
        return Response({'error': "Произошла непредвиденная ошибка"})


class MineAPIViewTurn(views.APIView):
    """ Представление для endpoint-a /api/turn """
    def post(self, request, *args, **kwargs):
        serializer = MineSerializerTurn(data=request.data)
        if serializer.is_valid():
            if cache.get('game').completed:
                return Response({"error": 'игра завершена'}, status=status.HTTP_400_BAD_REQUEST)

            if serializer.data['game_id'] == cache.get('game').game_id:
                game = cache.get('game')
                game.open_cell(serializer.data['row'], serializer.data['col'])
                # Обновление кеша
                cache.set('game', game)
                response = Response(MineSerializerResponse({'game_id': cache.get("game_id"),
                                                            'width': cache.get("width"),
                                                            'height': cache.get("height"),
                                                            'mines_count': cache.get("mines_count"),
                                                            'completed': game.completed,
                                                            'field': game.board}).data)
                return response
            else:
                return Response({"error": f"игра с идентификатором {serializer.data['game_id']}"
                                          f" не была создана или устарела (неактуальна)"}, status=status.HTTP_400_BAD_REQUEST)
        else: return Response({"error": 'Произошла непредвиденная ошибка'}, status=status.HTTP_400_BAD_REQUEST)

