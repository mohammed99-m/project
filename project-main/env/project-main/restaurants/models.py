from accounts.models import Profile
from django.db import models


class Restaurant(models.Model):
  restaurant_id = models.AutoField(primary_key=True)
  name = models.CharField(max_length=255)
  location = models.CharField(max_length=255)

  def __str__(self):
     return self.name

class Food(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    calories = models.DecimalField(max_digits=100,decimal_places=2)


class Meal(models.Model):
    meals_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.FloatField()
    description = models.TextField()
    photo = models.URLField()
    restaurant = models.ForeignKey(Restaurant, related_name='meals', on_delete=models.CASCADE)
    meal_time = models.CharField(max_length=255, help_text="Time for the meal")  
    ingredients = models.ManyToManyField(Food, related_name='ingredients_food')

    def __str__(self):
        return self.name

class DietPlan(models.Model):
    id = models.AutoField(primary_key=True)
    coach = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name="health_Program_maker")
    trainer = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name="health_Program_assigned")
    meals = models.ManyToManyField(Meal, related_name='diet_plans')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Diet Plan {self.id}"

  
class Order(models.Model):
  user = models.ForeignKey(Profile, on_delete=models.CASCADE)
  meals = models.ManyToManyField(Meal, through='OrderMeal')
  status = models.CharField(max_length=10, default='pending')
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
      return f"Order {self.id} - {self.status}"
  @property
  def total_price(self):
      total = sum(order_meal.quantity * order_meal.meal.price for order_meal in self.order_meal.all())
      return total

class OrderMeal(models.Model):
  order = models.ForeignKey(Order, related_name='order_meal', on_delete=models.CASCADE)
  meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
  quantity = models.PositiveIntegerField(default=1)