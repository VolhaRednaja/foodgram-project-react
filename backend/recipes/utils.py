from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from .models import Recipe


def download_file_response(ingredients_list):
    buy_list = []
    for item in ingredients_list:
        buy_list.append(f'{item["ingredient__name"]} - {item["value"]} '
                        f'{item["ingredient__measurement_unit"]} \n')

    response = HttpResponse(buy_list, 'Content-Type: text/plain')
    response['Content-Disposition'] = ('attachment; '
                                       'filename="buylist.txt"')
    return response


def create_relation(model_type, serializer_type, request, error_text, pk=None):
    user = request.user
    recipe = get_object_or_404(Recipe, id=pk)
    if request.method == "POST":
        if model_type.objects.filter(user=user, recipe=recipe).exists():
            return Response(
                {"error": error_text},
                status=status.HTTP_400_BAD_REQUEST,
            )
        data = model_type.objects.create(user=user, recipe=recipe)
        serializer = serializer_type(data, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    if request.method == "DELETE":
        data = model_type.objects.filter(user=user, recipe=recipe)
        if data.exists():
            data.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)
