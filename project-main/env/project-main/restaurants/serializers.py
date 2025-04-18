from rest_framework import serializers
from .models import Food, Order, OrderMeal, Meal, Restaurant ,DietPlan
from accounts.serializers import ProfileSerializer
from rest_framework import serializers
from .models import Restaurant

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['restaurant_id', 'name', 'location']

class FoodSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Food
        fields = ['id', 'name', 'calories']

class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = ['meals_id', 'name', 'price', 'description', 'photo', 'restaurant', 'meal_time', 'ingredients']

class OrderMealSerializer(serializers.Serializer):
    meal = serializers.PrimaryKeyRelatedField(queryset=Meal.objects.all())  
    quantity = serializers.IntegerField()

class OrderSerializer(serializers.Serializer):
    user = ProfileSerializer()
    id = serializers.IntegerField(read_only=True)
    order_meal = OrderMealSerializer(many=True)
    status = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    total_price = serializers.SerializerMethodField()
    serializers.PrimaryKeyRelatedField(read_only=True)

    def get_total_price(self, obj):
        return obj.total_price  

    def create(self, validated_data):
        order_meal_data = validated_data.pop('order_meal', [])
        user = validated_data.pop('user', None)  # تأكد من أن user موجود

        if user is None:
            raise ValueError("User must be provided.")

        order = Order.objects.create(
            status='pending',  
            user=user
        )

        for meal_data in order_meal_data:
            meal_id = meal_data.get('meal')  # تأكد من أن meal موجود
            quantity = meal_data.get('quantity', 1)  # افتراض الكمية 1 إذا لم تكن موجودة

            try:
                meal = Meal.objects.get(id=meal_id)
                OrderMeal.objects.create(order=order, meal=meal, quantity=quantity)        
            except Meal.DoesNotExist:
                raise ValueError(f"Meal with id {meal_id} not found.")

        return order

    def update(self, instance, validated_data):
        order_meal_data = validated_data.pop('order_meal', None)
        instance.status = validated_data.get('status', instance.status)
        instance.save()

        if order_meal_data is not None:
            instance.order_meal.all().delete()  # حذف الوجبات القديمة
            for meal_data in order_meal_data:
                OrderMeal.objects.create(order=instance, **meal_data)
        instance.save()
        return instance
    

class DietPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = DietPlan
        fields = ['id', 'coach', 'trainer', 'meals', 'created_at']

        
    # def create(self, validated_data):
    #     healthymeals_ids = validated_data.pop('healthymeals')
    #     diet_plan = DietPlan.objects.create(**validated_data)
    #     diet_plan.healthymeals.set(healthymeals_ids)
    #     return diet_plan

    # def update(self, instance, validated_data):
    #     healthymeals_data = validated_data.pop('healthymeals', None)
    #     instance.coach = validated_data.get('coach', instance.coach)
    #     instance.trainer = validated_data.get('trainer', instance.trainer)
    #     instance.meal_time = validated_data.get('meal_time', instance.meal_time)
    #     instance.save()

    #     if healthymeals_data is not None:
    #         instance.healthymeals.clear()
    #         for meal_data in healthymeals_data:
    #             healthy_meal = HealthyMeal.objects.create(**meal_data)
    #             instance.healthymeals.add(healthy_meal)

    #     return instance