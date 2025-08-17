from collections import defaultdict
import random
from django.shortcuts import render

# Create your views here.
import joblib
import numpy as np
from rest_framework.response import Response
from rest_framework import status

from accounts.serializers import ProfileSerializer
from illnesses.models import IllnessToAvoidFood
from .models import DietPlan, Meal , Food, MealsSchedule,Order, OrderMeal, Restaurant
from .serializers import DietPlanSerializer,  FoodSerializer,  MealSerializer, OrderSerializer, RestaurantSerializer,MealSerializer2
import logging #للتأكد من صحةالبيانات
from django.shortcuts import get_object_or_404
from accounts.models import Profile
from rest_framework.decorators import api_view, permission_classes
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

#اضافة مطعم
@api_view(['POST'])
def create_restaurant(request):
    serializer = RestaurantSerializer(data=request.data)
    if serializer.is_valid():
        name = request.data.get('name')
        location = request.data.get('location')
        latitude=request.data.get('latitude')
        longitude=request.data.get('longitude')
        restaurant = Restaurant.objects.create(
          name=name,
          location=location,
          latitude=latitude,
          longitude=longitude
         )

         
        ##serialized_restaurant = RestaurantSerializer(restaurant)
        return Response({
            "message": "Restaurant created successfully.",
            "id": restaurant.id,
            "name": restaurant.name,
            "location": restaurant.location,
            "latitude":restaurant.latitude,
            "longitude":restaurant.longitude
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
         name = request.data.get('name')
         calories = request.data.get('calories')
         food = Food.objects.create(
          name=name,
          calories=calories
         )
            
             
         return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#ارجاع انواع الغذاء
@api_view(["GET"])
def foods(request):
    foods = Food.objects.all()  
    serializer = FoodSerializer(foods, many=True)  
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_meal(request):
    serializer = MealSerializer2(data=request.data)
    if serializer.is_valid():
        meal = serializer.save()
        # name = request.data.get('name')
        # price = request.data.get('price')
        # description=request.data.get('description')
        # restaurant = request.data.get('restaurant')
        # meal_time= request.data.get('restaurant',[])
        # ingredients = request.data.get('ingredients',[])
        
        # meal = Food.objects.create(
        #   name=name,
          
        #  )
        meal_data = MealSerializer2(meal).data
        restaurant_data = [{"id": restaurant.id, "name": restaurant.name, "location":restaurant.location} for restaurant in meal.restaurant.all()]
        ingredients_data = [{"id": food.id, "name": food.name, "calories":food.calories} for food in meal.ingredients.all()]

        return Response({
            "message": "Meal created successfully.",
            **meal_data,
            "restaurant":restaurant_data,
            "ingredients":ingredients_data,
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#ارجاع الوجبات الصحية
@api_view(["GET"])
def HealthyMealList(request):
    healthy_meals = Meal.objects.all()  
    serializer = MealSerializer(healthy_meals, many=True)  
    return Response(serializer.data, status=status.HTTP_200_OK)

#اضافة طلب  
@api_view(['POST'])
##@permission_classes([IsAuthenticated])
def create_order(request,user_id,restaurant_id):
    meals_data = request.data.get('meals', [])
    
    try:
        profile = Profile.objects.get(user__id=user_id)
    except Profile.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    try:
       restaurant = Restaurant.objects.get(id=restaurant_id)
    except Restaurant.DoesNotExist:
        return Response({"error": "Restaurant not found."}, status=status.HTTP_404_NOT_FOUND)
    # إنشاء الطلب
    order = Order.objects.create(user=profile, status='pending')  # تعيين المستخدم
    # إضافة الوجبات إلى الطلب
    order_meals = []
    for meal_data in meals_data:
        meal_id1 = meal_data.get('meal')
        quantity = meal_data.get('quantity', 1)
        
        meal = Meal.objects.filter(meals_id=meal_id1).first()
            # إضافة الوجبة إلى الطلب
        if meal:
              order_meal= OrderMeal.objects.create(order=order, meal=meal, quantity=quantity)        
              order_meals.append({
                "meal_id": meal.meals_id,
                "meal_name": meal.name,
                "quantity": order_meal.quantity,
                "price": meal.price,
                "restaurant": restaurant.name,
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
#@permission_classes([IsAuthenticated])
def list_user_orders(request,user_id):
    try:
        profile = get_object_or_404(Profile,user__id=user_id)
    except Profile.DoesNotExist:
        return Response({"error": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)
    
    orders = Order.objects.filter(user=profile)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

#حذف  مطعم
@api_view(['DELETE'])
def delete_restaurant(request, restaurant_id):
    try:
        restaurant = Restaurant.objects.get(id=restaurant_id)
    except Restaurant.DoesNotExist:
        return Response({"error": "Restaurant not found"}, status=status.HTTP_404_NOT_FOUND)

    restaurant.delete()
    return Response({"message": "Restaurant deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

#بحث عن وجبات حسب الاسم
@api_view(["GET"])
def search_HealthyMeal(request):
    query = request.query_params.get('q')
    print(query)
    if query:
        healthy_meals = Meal.objects.filter(name__icontains=query) 
    else:
        healthy_meals = Meal.objects.all()  

    serializer = MealSerializer(healthy_meals, many=True)  
    return Response(serializer.data, status=status.HTTP_200_OK)


# للحصول على الخطط الغذائية لمدرب محدد
@api_view(["GET"])
def get_coach_diet_plans(request, coach_id):
    coach = get_object_or_404(Profile, user__id=coach_id)
    diet_plans = DietPlan.objects.filter(coach=coach)

    result = []

    for plan in diet_plans:
        # جلب جميع الوجبات لهذا النظام ا لغذائي
        scheduled_meals = MealsSchedule.objects.filter(dietplan=plan)
        grouped_by_day = defaultdict(list)

        for schedule in scheduled_meals:
            serialized_meal = MealSerializer(schedule.meal).data

            # إضافة وصف اليوم من جدول MealsSchedule
            grouped_by_day[schedule.day].append({
                "meal": serialized_meal
            })
        days_meals = []
        for day, meals_list in grouped_by_day.items():
            days_meals.append({
                "diet_plan_id": plan.id,
                "day": day,
                "description": scheduled_meals.filter(day=day).first().description,
                "meals": meals_list
            })

      
        result.append({                     
              "coach": ProfileSerializer(plan.coach).data,
              "trainer": ProfileSerializer(plan.trainer).data,
              "days_meals": days_meals                            
        })

    return Response(result, status=status.HTTP_200_OK)


# للحصول على الخطة الغذائية للاعب محدد
@api_view(["GET"])
def get_trainner_diet_plans(request,trainer_id):
    trainer = get_object_or_404(Profile,user__id=trainer_id)
    diet_plan = DietPlan.objects.filter(trainer=trainer).first()
    if not diet_plan:
        return Response({}, status=status.HTTP_200_OK)

    result = []

        # جلب جميع الوجبات لهذا النظام الغذائي
    scheduled_meals = MealsSchedule.objects.filter(dietplan=diet_plan)
    grouped_by_day = defaultdict(list)

    for schedule in scheduled_meals:
        serialized_meal = MealSerializer(schedule.meal).data

            #  إضافة وصف اليوم من جدول MealsSchedule لتصنيف الوجبات حسب اليوم
        grouped_by_day[schedule.day].append({
            "meal": serialized_meal
        })

    days_meals = []
    for day, meals_list in grouped_by_day.items():
        days_meals.append({
            "day": day,
            "description": scheduled_meals.filter(day=day).first().description,
            "meals": meals_list
        })

      
    result.append({                     
          "id": diet_plan.id,
          "coach": ProfileSerializer(diet_plan.coach).data,
          "trainer": ProfileSerializer(diet_plan.trainer).data,
          "days_meals": days_meals                            
    })

    return Response(result, status=status.HTTP_200_OK)

#للحصول على الخطط الغذائية
@api_view(["GET"])
def get_diet_plans(request):
    diet_plans = DietPlan.objects.all()
    serializer = DietPlanSerializer(diet_plans, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

#لإضافة خطة غذائية
@api_view(["POST"])
def add_diet_plan(request,coach_id,trainer_id):
    coach = get_object_or_404(Profile,user__id=coach_id)
    trainer = get_object_or_404(Profile,user__id=trainer_id)
    days_meals = request.data.get("days_meals", [])
    print(days_meals)
    ## هون في حال لم يكن هناك برنامج رح يفرش بس اذا كان في رح يعلم المستخدم انو في برنامج
    dietplan = DietPlan.objects.filter(trainer=trainer).first()

    if dietplan:
        return Response({"detail": "This User already got a dite plan"}, status=status.HTTP_400_BAD_REQUEST)
    if not days_meals:
        return Response({"detail": "At least one meal must be provided."}, status=status.HTTP_400_BAD_REQUEST)
    
    print("H"*50)
      
    dietplan = DietPlan.objects.create(
        coach=coach,
        trainer=trainer,
    )

    for day_meal in days_meals:
        day = day_meal.get("day")
        description = day_meal.get("description")
        meals_ids = day_meal.get("meals" , [])

        if not meals_ids:
             return Response({"detail": "Meals must be provided for each day."}, status=status.HTTP_400_BAD_REQUEST)
        
        meals = Meal.objects.filter(meals_id__in=meals_ids)
        print("K"*50)
        print(meals[0])

        for meal in meals:
             MealsSchedule.objects.create(
                meal=meal,
                description = description,
                dietplan=dietplan,
                day=day
            )

    serialized_program = DietPlanSerializer(dietplan)
    return Response(serialized_program.data, status=status.HTTP_201_CREATED)


#البحث عن الخطة بالنسبة لوقتها(افطار غداء عشاء)
@api_view(["GET"])
def search_meal_time(request):
    meal_time = request.GET.get('meal_time', None)
    if meal_time:
        meals = Meal.objects.filter(meal_time=meal_time)
    else:
        meals = Meal.objects.all()

    serializer = MealSerializer(meals, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["Post"])
def update_dietplan(request,coach_id,plan_id):
    coach = get_object_or_404(Profile,user__id=coach_id)
    print(coach.user.username)
    dietplan = get_object_or_404(DietPlan,id=plan_id)
    days_meals = request.data.get("days_meals", [])

    if not days_meals:
        return Response({"detail": "At least one meal must be provided."}, status=status.HTTP_400_BAD_REQUEST)
    
    if coach!=dietplan.coach:
        print(dietplan.coach.user.id)
        print(coach_id)
        return Response({"detail":"You Cant update on this plan"})
    
    print("H"*50)
    MealsSchedule.objects.filter(dietplan=dietplan).delete()
    print("K"*50)
    
    for day_meal in days_meals:
        day = day_meal.get("day")
        meals_ids = day_meal.get("meals" , []) 
        description = day_meal.get("description")

        if not meals_ids:
             return Response({"detail": "Meals must be provided for each day."}, status=status.HTTP_400_BAD_REQUEST)
        
        for meal_id in meals_ids:
            try:
               meal = Meal.objects.get(meals_id=meal_id)
            except Meal.DoesNotExist:
               return Response({"detail": f"Meal with id {meal_id} not found."}, status=status.HTTP_400_BAD_REQUEST)

            MealsSchedule.objects.create(
                  meal=meal,
                  description=description,
                  dietplan=dietplan,
                  day=day
            )
          
    
    
    serialized_program = DietPlanSerializer(dietplan)
    return Response(serialized_program.data, status=status.HTTP_200_OK)
   
@api_view(["GET"])
def get_restaurants_with_meal(request,meal_id):
    meal = get_object_or_404(Meal,meals_id=meal_id)
    restaurants = meal.restaurant
    serializer = RestaurantSerializer(restaurants, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(["GET"])
def get_meals_in_restaurant(request, restaurant_id):
    # Fetch the restaurant object or return 404 if not found
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    
    # Fetch all meals that are associated with this restaurant
    meals = Meal.objects.filter(restaurant=restaurant)
    
    # Serialize the meals data
    serializer = MealSerializer(meals, many=True)
    
    # Return the serialized data
    return Response(serializer.data, status=status.HTTP_200_OK)
####################################################################################


@api_view(['POST'])
def update_meal(request, meal_id):
    meal = get_object_or_404(Meal, meals_id=meal_id)
    ingredient_ids = request.data.get('ingredients', [])

    if not ingredient_ids:
        return Response({"detail": "Food IDs must be provided."}, status=status.HTTP_400_BAD_REQUEST)

    new_foods = []
    for food_id in ingredient_ids:
        food = get_object_or_404(Food, id=food_id)
        new_foods.append(food)

    meal.ingredients.clear()

    meal.ingredients.add(*new_foods)

    serializer = MealSerializer(meal)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
def delete_meal(request,  meal_id):
    
    meal = get_object_or_404(Meal, meals_id=meal_id)

  
    meal.delete()

    return Response({"detail": "Meal deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def get_meal_by_id(request,  meal_id):
    
    meal = get_object_or_404(Meal, meals_id=meal_id)
    serializer = MealSerializer(meal)
    return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(["DELETE"])
def delete_dietplan(request,dietplan_id,user_id):

    deleter = get_object_or_404(Profile,user__id=user_id)
    dietplan = get_object_or_404(DietPlan,id=dietplan_id)


    if(dietplan and (dietplan.coach==deleter or dietplan.trainer==deleter)):
            dietplan.delete()
            return(Response("dietplan Deleted Succesfuly"))
    else:
           return(Response("no dietplan with that info"))
    

@api_view(["POST"])
def recommend_diet_ai(request, user_id):
    profile = get_object_or_404(Profile, user__id=user_id)

    #اذا كان للمتدرب خطة غذائية
    existing_plan = DietPlan.objects.filter(trainer=profile).first()
    if existing_plan:
        return Response({
            "message": "User already has a diet plan.",
            "plan_id": existing_plan.id
        }, status=status.HTTP_400_BAD_REQUEST)
    

    #جلب الأمراض من الداتا بيز
    illnesses = list(IllnessToAvoidFood.objects.all())
    illness_id= {ill.id: idx for idx, ill in enumerate(illnesses)}


    # معلومات المتدرب
    weight = profile.weight
    height = profile.height
    gender = encode_gender(profile.gender)
    level = encode_fitness_level(profile.experianse_level)
    goal = encode_goal(profile.goal)
    illnesses = encode_illnesses(profile.illnesses or [], illness_id, len(illnesses))

    # تحميل المودل
    model = joblib.load("diet_recommender.joblib")
    mlb = joblib.load("meal_mlb.joblib")

    #  مصفوفة الأطعمة المتوقعة
    X_basic = [weight, height, level, goal, gender]
    X = np.array([X_basic + illnesses])
    predicted = model.predict(X)
    meal_ids = mlb.inverse_transform(predicted)[0]

    # جلب الوجبات
    meals = list(Meal.objects.filter(meals_id__in=meal_ids))

    if not meals:
        return Response({"detail": "No meals found for the predicted IDs."}, status=status.HTTP_404_NOT_FOUND)
#المدرب الافتراضي
    virtual_coach = Profile.objects.get(user__username='ai_trainer')

    new_plan = DietPlan.objects.create(
        coach=virtual_coach,
        trainer=profile
    )

#من اجل كل يوم سيعرض لنا ثلاث تمارين بكل يوم من ايام الاسبوع
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    meals_per_day = 5
    total = meals_per_day * len(days)

    if len(meals) < total:
        meals = random.choices(meals, k=total)
    else:
        meals = random.sample(meals, total)
        
    #لإضافة البرنامج لجدول البرنامج في الداتا
    for i, day in enumerate(days):
        day_meals = meals[i * meals_per_day : (i + 1) * meals_per_day]
        for meal in day_meals:
            MealsSchedule.objects.create(
                meal=meal,
                dietplan=new_plan,
                day=day,
                description="AI generated meal plan"
            )

    serializer = DietPlanSerializer(new_plan)
    return Response(serializer.data)

def encode_fitness_level(level):
    return {'beginner': 0, 'intermediate': 1, 'advanced': 2}.get(level, 0)

def encode_goal(goal):
    return {'lose_weight': 0, 'build_muscle': 1, 'endurance': 2}.get(goal, 0)

def encode_gender(gender):
    return {'male': 0, 'female': 1}.get(gender, 0)

#تحويل الأمراض الى قائمة اعداد 0 اذا لم يكن موجود و 1 اذا كان المرض موجود
def encode_illnesses(user_illness, id, total_illness):
    list = [0] * total_illness
    for ill_id in user_illness:
        index = id.get(ill_id)
        if index is not None:
            list[index] = 1
    return list

@api_view(["GET"])
def get_meals_with_avoid_flag(request, user_id):
    try:
        profile = Profile.objects.get(user_id=user_id)
    except Profile.DoesNotExist:
        return Response({"error": "User profile not found"}, status=status.HTTP_404_NOT_FOUND)

    illnesses = profile.illnesses  

    avoid_entries = IllnessToAvoidFood.objects.filter(illness__in=illnesses)
    avoid_food_names = set()
    for entry in avoid_entries:
        avoid_food_names.update(entry.foods_to_avoid)  

    all_meals = Meal.objects.prefetch_related("ingredients").all()
    result = []

    for meal in all_meals:
        ingredient_names = [food.name for food in meal.ingredients.all()]
        should_avoid = any(name in avoid_food_names for name in ingredient_names)

        result.append({
            "meal_id": meal.meals_id,
            "name": meal.name,
            "description": meal.description,
            "price": meal.price,
            "ingredients": ingredient_names,
            "avoid": "yes" if should_avoid else "no"
        })

    return Response(result, status=status.HTTP_200_OK)