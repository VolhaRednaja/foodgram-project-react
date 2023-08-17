from django.urls import include, path
from djoser.views import TokenCreateView, TokenDestroyView
from rest_framework.routers import DefaultRouter

from .views import (IngredientsViewSet, RecipeViewSet,
                    TagsViewSet, FollowApiView,
                    ListFollowViewSet, UserViewSet)

router = DefaultRouter()

router.register('ingredients', IngredientsViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('tags', TagsViewSet, basename='tags')
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('auth/token/login/', TokenCreateView.as_view(), name='login'),
    path('auth/token/logout/', TokenDestroyView.as_view(), name='logout'),
    path('auth/', include('djoser.urls.authtoken')),
    path('users/<int:id>/subscribe/',
         FollowApiView.as_view(),
         name='subscribe'
         ),
    path('users/subscriptions/', ListFollowViewSet.as_view(),
         name='subscription'
         ),
    path('', include(router.urls)),
]
