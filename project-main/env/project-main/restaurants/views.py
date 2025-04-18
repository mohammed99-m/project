from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import viewsets, status
from .models import DietPlan, Food,Meal, Profile, Order, OrderMeal, Restaurant
from .serializers import MealSerializer, OrderSerializer, RestaurantSerializer,DietPlanSerializer, FoodSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


#اضافة مطعم
@api_view(['POST'])
def create_restaurant(request):
    serializer = RestaurantSerializer(data=request.data)
    if serializer.is_valid():
        restaurant = serializer.save()
        return Response({
            "message": "Restaurant created successfully.",
            "restaurant_id": restaurant.restaurant_id,
            "name": restaurant.name,
            "location": restaurant.location
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#ارجاع المطاعم
@api_view(["GET"])
def list_restaurants(request):
    restaurants = Restaurant.objects.all()    
    restaurants_serializer = RestaurantSerializer(restaurants, many=True)  # Serialize resturant
    return Response(restaurants_serializer.data, status=status.HTTP_200_OK)

#اضافة food
@api_view(["POST"])
def add_food(request):
    serializer = FoodSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#للحصول على الfood
@api_view(["GET"])
def get_food(request):
    foods = Food.objects.all()  # الحصول على جميع عناصر الطعام
    serializer = FoodSerializer(foods, many=True)  # تسلسل البيانات
    return Response(serializer.data, status=status.HTTP_200_OK)


#اضافة وجبة
@api_view(['POST'])
def create_meal(request):
    serializer = MealSerializer(data=request.data)
    if serializer.is_valid():
        meal = serializer.save()
        meal_data = MealSerializer(meal).data
        ingredients_data = [{"id": food.id, "name": food.name, "calories":food.calories} for food in meal.ingredients.all()]

        return Response({
            "message": "Meal created successfully.",
            **meal_data,
            "ingredients":ingredients_data,
            "restaurant_name": meal.restaurant.name,
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#ارجاع الوجبات
@api_view(["GET"])
def list_Meal(request):
    meals = Meal.objects.all()    
    meal_serializer = MealSerializer(meals, many=True)  # Serialize meals
    return Response(meal_serializer.data, status=status.HTTP_200_OK)

#اضافة طلب  
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    meals_data = request.data.get('meals', [])
    
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    
    # إنشاء الطلب
    order = Order.objects.create(user=profile, status='pending')  # تعيين المستخدم

    # إضافة الوجبات إلى الطلب
    order_meals = []
    for meal_data in meals_data:
        meal_id1 = meal_data.get('meal')
        quantity = meal_data.get('quantity', 1)
        
        meal = Meal.objects.filter(meals_id=meal_id1).first()
        ingredients_data = [{"id": food.id, "name": food.name,"calories":food.calories} for food in meal.ingredients.all()]
        if meal:
              order_meal= OrderMeal.objects.create(order=order, meal=meal, quantity=quantity)        
              order_meals.append({
                "meal_id": meal.meals_id,
                "meal_name": meal.name,
                "quantity": order_meal.quantity,
                "price": meal.price,
                "restaurant": meal.restaurant.name,
                "ingredients": ingredients_data,
            })
        else:
              return Response({"error": f"Meal with id {meal_id1} not found."},
                               status=status.HTTP_404_NOT_FOUND)

    total_price = order.total_price
    return Response({
        "message": "Order created successfully.",
        "order": {
            "order_id": order.id,
            "user": profile.user.username,
            "status": order.status,
            "meals": order_meals,
            "total_price": total_price
            }
            }, status=status.HTTP_201_CREATED)

#لتعديل حالة الطلب من pending to ready...
@api_view(["PATCH"])
def update_order_status(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

    new_status = request.data.get('status')
    if new_status is None:
        return Response({"error": "Status must be provided"}, status=status.HTTP_400_BAD_REQUEST)

    order.status = new_status
    order.save()
    
    return Response({
            "message": "Order status updated",
            "order": {
                "id": order.id,
                "user": order.user.id,  
                "status": order.status,
                "created_at": order.created_at,  
            }
        }, status=status.HTTP_200_OK)

#ارجاع طلبات المسخدم
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_user_orders(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        return Response({"error": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)
    
    orders = Order.objects.filter(user=profile)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

#حذف  مطعم
@api_view(['DELETE'])
def delete_restaurant(request, restaurant_id):
    try:
        restaurant = Restaurant.objects.get(restaurant_id=restaurant_id)
    except Restaurant.DoesNotExist:
        return Response({"error": "Restaurant not found"}, status=status.HTTP_404_NOT_FOUND)

    restaurant.delete()
    return Response({"message": "Restaurant deleted successfully"}, status=status.HTTP_204_NO_CONTENT)




#اضافة وجبة صحية
# @api_view(["POST"])
# def add_healthy_meal(request):
#     serializer = MealSerializer(data=request.data) 
#     if serializer.is_valid(): 
#         serializer.save()  
#         return Response(serializer.data, status=status.HTTP_201_CREATED)  
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# #ارجاع الوجبات الصحية
# @api_view(["GET"])
# def HealthyMealList(request):
#     healthy_meals = Meal.objects.all()  
#     serializer = MealSerializer(healthy_meals, many=True)  
#     return Response(serializer.data, status=status.HTTP_200_OK)

#اليحث عن الوجبات الصحية من خلال اسمها

@api_view(["GET"])
def search_Meal(request):
    query = request.query_params.get('q', None)
    if query:
        meals = Meal.objects.filter(name__icontains=query) 
    else:
        meals = Meal.objects.all()  

    serializer = MealSerializer(meals, many=True)  
    return Response(serializer.data, status=status.HTTP_200_OK)

####
#للحصول على الخطط الغذائية
@api_view(["GET"])
def get_diet_plans(request):
    diet_plans = DietPlan.objects.all()
    serializer = DietPlanSerializer(diet_plans, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

#لإضافة خطة غذائية
@api_view(["POST"])
def add_diet_plan(request):
    serializer = DietPlanSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#البحث عن الوجبة ضمن الخطة الخاصة للمسخدم بالنسبة لوقتها(افطار غداء عشاء)
@api_view(["GET"])
def search_diet_plan(request):
    meal_time = request.GET.get('meal_time', None)
    diet_plans = DietPlan.objects.filter(trainer=request.user.profile)

    if meal_time:
        meals = Meal.objects.filter(meal_time=meal_time)
        diet_plans = meals.filter(diet_plans__in=diet_plans).distinct()
    if diet_plans.exists():
        serializer = MealSerializer(diet_plans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({"message": "No diet plans found."}, status=status.HTTP_404_NOT_FOUND)

#ارجاع النظم الغذئية للمستخدم
@api_view(["GET"])
def get_user_diet_plans(request):
    diet_plans = DietPlan.objects.filter(trainer=request.user.profile)

    serializer = DietPlanSerializer(diet_plans, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)