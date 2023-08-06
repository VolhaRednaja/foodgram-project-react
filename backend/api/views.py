from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from users.paginator import CustomPaginator

from .filters import IngredientsFilter, RecipeFilter
from recipes.mixins import RetriveAndListViewSet
from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                     ShoppingList, Tag)
from .permissions import IsAuthorOrAdmin
from .serializers import (AddRecipeSerializer, FavouriteSerializer,
                          IngredientsSerializer, ShoppingListSerializer,
                          ShowRecipeFullSerializer, TagsSerializer)
from recipes.utils import download_file_response, create_relation


class IngredientsViewSet(RetriveAndListViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = IngredientsFilter
    pagination_class = None


class TagsViewSet(RetriveAndListViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all().order_by('-id')
    serializer_class = ShowRecipeFullSerializer
    permission_classes = [IsAuthorOrAdmin]
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter
    pagination_class = CustomPaginator

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ShowRecipeFullSerializer
        return AddRecipeSerializer

    @action(
        detail=True,
        methods=["POST", "DELETE"],
        url_path="favorite",
        permission_classes=[IsAuthorOrAdmin],
    )
    def favorite(self, request, pk=None):
        create_relation(
            Favorite,
            FavouriteSerializer,
            request,
            "Этот рецепт уже в избранном",
            pk,
        )


    @action(
        detail=True,
        methods=["POST", "DELETE"],
        url_path="shopping_cart",
        permission_classes=[IsAuthorOrAdmin],
    )
    def shopping_cart(self, request, pk=None):
        create_relation(
            ShoppingList,
            ShoppingListSerializer,
            request,
            "Этот рецепт уже в корзине покупок",
            pk,
        )


    @action(detail=False, methods=["GET"],
            permission_classes=[permissions.IsAuthenticated])
    def download_shopping_cart(self, request):
        ingredients_list = RecipeIngredient.objects.filter(
            recipe__shopping_cart__user=request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(value=Sum('value'))
        return download_file_response(ingredients_list)
