from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from .filters import IngredientsFilter, RecipeFilter
from .mixins import RetriveAndListViewSet
from .paginator import CustomPaginator
from .permissions import IsAuthorOrAdmin
from .serializers import (AddRecipeSerializer, CustomUserSerializer,
                          FavouriteSerializer, IngredientsSerializer,
                          ShoppingListSerializer, ShowFollowSerializer,
                          ShowRecipeFullSerializer, TagsSerializer)
from recipes.models import (Favorite, Ingredient,
                            Recipe, RecipeIngredient,
                            ShoppingList, Tag)
from recipes.utils import download_file_response, create_relation
from users.models import Follow


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny, ]

    @action(
        detail=False,
        methods=['get'],
        permission_classes=(IsAuthenticated, )
    )
    def me(self, request):
        serializer = self.get_serializer(self.request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FollowApiView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('id', None)
        author = get_object_or_404(User, pk=pk)
        user = request.user

        if author == user:
            return Response(
                {'errors': 'Вы не можете подписываться на себя'},
                status=status.HTTP_400_BAD_REQUEST)

        if Follow.objects.filter(author=author, user=user).exists():
            return Response(
                {'errors': 'Вы уже подписаны на этого пользователя'},
                status=status.HTTP_400_BAD_REQUEST)

        obj = Follow(author=author, user=user)
        obj.save()

        serializer = ShowFollowSerializer(
            author, context={'request': request})

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        user = request.user
        author = get_object_or_404(User, id=id)
        try:
            subscription = get_object_or_404(Follow, user=user,
                                             author=author)
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Follow.DoesNotExist:
            return Response(
                'Ошибка отписки',
                status=status.HTTP_400_BAD_REQUEST,
            )


class ListFollowViewSet(generics.ListAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = ShowFollowSerializer
    pagination_class = CustomPaginator

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(following__user=user)


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
    permission_classes = [IsAuthenticatedOrReadOnly, ]
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
        ).annotate(amount=Sum('amount'))
        return download_file_response(ingredients_list)
