from django.core.management.base import BaseCommand
from accounts.models import Profile
from health.models import DietPlan, MealsSchedule 
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import joblib

from illnesses.models import IllnessToAvoidFood

class Command(BaseCommand):
    help = "Train diet recommendation model based on previous plans"

    def handle(self, *args, **kwargs):
        #نجلب الامراض من  IllnessToAvoidExercises ليتجنبها المودل عندما يضع برنامج للمتدرب
        self.illnesses = list(IllnessToAvoidFood.objects.all())
        self.illness_id = {IllnessToAvoidFood.id: idx for idx, illness in enumerate(self.illnesses)}

        data = []
#الحلقة للمرور على جميع البرامج المخزنة للتدريب عليها
        for plan in DietPlan.objects.all():
            #جلب كل المعلومات للبرنامج
            profile = plan.trainer
            meal_ids = MealsSchedule.objects.filter(dietplan=plan).values_list('meal_id', flat=True)
                
            if profile and meal_ids:
                #نخزن البيانات بعد تكويدها
                data.append({
                    'weight': profile.weight,
                    'height': profile.height,
                    'gender': self.encode_gender(profile.gender),
                    'level': self.encode_fitness_level(profile.experianse_level),
                    'goal': self.encode_goal(profile.goal),
                    'illnesses': self.encode_illnesses(profile.illnesses),
                    'meals': list(meal_ids)
                })

        if not data:
            self.stdout.write(self.style.ERROR("No diet plan data found."))
            return
#نتحقق من وجود بيانات
        df = pd.DataFrame(data)

        mlb = MultiLabelBinarizer()
        Y = mlb.fit_transform(df['meals'])
        X_basic = df[['weight', 'height', 'level', 'goal', 'gender']].values
        X_illness = np.array(df['illnesses'].tolist())

        X = np.hstack([X_basic, X_illness])
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

        model = RandomForestClassifier()
        model.fit(X_train, Y_train)

        joblib.dump(model, 'diet_recommender.joblib')
        joblib.dump(mlb, 'meal_mlb.joblib')
        joblib.dump(self.illness_id, 'illness_index_map.joblib')

        self.stdout.write(self.style.SUCCESS("Diet model trained and saved successfully."))

    def encode_fitness_level(self, level):
        return {'beginner': 0, 'intermediate': 1, 'advanced': 2}.get(level, 0)

    def encode_goal(self, goal):
        return {'lose_weight': 0, 'build_muscle': 1, 'endurance': 2}.get(goal, 0)

    def encode_gender(self, gender):
        return {'male': 0, 'female': 1}.get(gender, 0)
#اذا كان المرض موجود نضع 1 وإلا نضع 0
    def encode_illnesses(self, illnesses):
        list = [0] * len(self.illnesses)

        if not illnesses:
          return list

        for ill_id in illnesses:
            id = self.illness_id.get(ill_id)
            if id is not None:
                list[id] = 1

        return list