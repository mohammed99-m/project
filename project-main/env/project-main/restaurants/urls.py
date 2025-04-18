from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import  add_diet_plan, add_food, create_meal, create_order, create_restaurant, delete_restaurant, get_diet_plans, get_food, get_user_diet_plans, list_Meal, list_restaurants, list_user_orders, search_Meal, search_diet_plan, update_order_status


urlpatterns = [
    path('create_restaurant/', create_restaurant, name='create_restaurant'), #اضافة وجبة   
    path('restaurants/', list_restaurants, name='list_restaurants'),  #ارجاع الوجبات
    path('add-food/', add_food, name='add_food'),  # إضافة عنوان URL
    path('get-food/', get_food, name='get_food'),  # عنوان URL للحصول على الطعام
    path('create_meal/', create_meal, name='create_meal'),  #اضافة مطعم
    path('meals/', list_Meal, name='list_Meal'),  #ارجاع المطاعم
    path('creat-orders/', create_order, name='create-order'),# انشاء طلب
    path('user/orders/', list_user_orders, name='user-orders'), #عرض طلبات المستخدم
    path('orders/<int:order_id>/update-status/', update_order_status, name='update-order-status'), #لتغيير حالة الطلب (pendding ready ...)
    path('delete-restaurants/<int:restaurant_id>/', delete_restaurant, name='delete_restaurant'), #حذف مطعم
    
    path('meals/search/', search_Meal, name='search-meal'),#للحصول على الوجبة من خلال اسمها
    # path('healthy-meals/add/', add_healthy_meal, name='add-healthy-meal'),  # المسار لإضافة وجبة صحية
    path('diet-plans/', get_diet_plans, name='diet-plan-list'),# ارجاع الخطط الغذائية
    path('diet-plans/add/', add_diet_plan, name='add-diet-plan'),#إضافة خطة غذائية
    path('diet-plans/search/', search_diet_plan, name='search-diet-plan'),  # للبحث عن الخطة الغذائية حسب وقتها(افطار, غداء....) 
    path('user-diet-plans/', get_user_diet_plans, name='get_user_diet_plans'),

]

