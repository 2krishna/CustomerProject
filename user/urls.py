
from django.urls import path
from user.views import RegisterView
from user.views import MyObtainTokenPairView, RegisterView,ProductListView,ProductDetailView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('signup/', RegisterView.as_view()),

    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('product/',ProductListView.as_view({'get': 'list','post': 'create'}),name='product_list'),
    path('product/<int:pk>/',ProductDetailView.as_view(),name='product_detail'),
    ]
