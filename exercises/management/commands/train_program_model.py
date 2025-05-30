from django.core.management.base import BaseCommand
from exercises.models import Program, ExerciseSchedule
from accounts.models import Profile
import numpy as np
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.model_selection import train_test_split

from illnesses.models import IllnessToAvoidExercises

class Command(BaseCommand):
    help = 'Train a recommendation model based on previous programs'
    # ILLNESS_MAPPING = [
    #     "Hypertension (Severe)", "Heart Failure", "Type 2 Diabetes (With Neuropathy)", "Osteoarthritis (Knees)","Rheumatoid Arthritis (Flare-Ups)", "Osteoporosis (Advanced)",
    #     "Multiple Sclerosis (Fatigue-Prone)", "Parkinson’s Disease","Epilepsy (Uncontrolled) (Balance Issues)","Severe Asthma", "COPD", "Herniated Disc", "Rotator Cuff Tear" ]   
    
    def handle(self, *args, **kwargs):
        #نجلب الامراض من  IllnessToAvoidExercises ليتجنبها المودل عندما يضع برنامج للمتدرب
        self.illnesses = list(IllnessToAvoidExercises.objects.all())
        self.illness_id = {ill.id: idx for idx, ill in enumerate(self.illnesses)}

        data = []
#الحلقة للمرور على جميع البرامج المخزنة للتدريب عليها
        for program in Program.objects.all():
            try:
                #جلب كل المعلومات للبرنامج
                profile = program.trainer
                exercises = ExerciseSchedule.objects.filter(program=program).values_list('exercise_id', flat=True)

                if profile and exercises:
                    #نخزن البيانات بعد تكويدها
                    data.append({
                        'weight': profile.weight,
                        'height': profile.height,
                        'gender': self.encode_gender(profile.gender),
                        'level': self.encode_fitness_level(profile.experianse_level),
                        'goal': self.encode_goal(profile.goal),
                        'illnesses':self.encode_illnesses(profile.illnesses),
                        'exercises': list(exercises)
                    })
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error in program {program.id}: {e}'))

        if not data:
            self.stdout.write(self.style.ERROR('No training data found.'))
            return
#نتحقق من وجود بيانات
        df = pd.DataFrame(data)

        mlb = MultiLabelBinarizer()
        Y = mlb.fit_transform(df['exercises'])
        X_basic = df[['weight', 'height', 'level', 'goal', 'gender']].values #مصفوفة ارقام بالبيانات الاساسية
        X_illness = np.array(df['illnesses'].tolist())  # قائمة الأمراض 

        X = np.hstack([X_basic, X_illness]) 

        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42) #نقسم البيانات الى اختبار وتدريب
        model = RandomForestClassifier()
        model.fit(X_train, Y_train)

        joblib.dump(model, 'program_recommender_multi.joblib')
        joblib.dump(mlb, 'exercise_mlb.joblib')

        self.stdout.write(self.style.SUCCESS("Model trained and saved successfully."))

    def encode_fitness_level(self, level):
        return {'beginner': 0, 'intermediate': 1, 'advanced': 2}.get(level, 0)

    def encode_goal(self, goal):
        return {'lose_weight': 0, 'build_muscle': 1, 'endurance': 2}.get(goal, 0)

    def encode_gender(self, gender):
        return {'male': 0, 'female': 1}.get(gender, 0)
    #اذا كان المرض موجود نضع 1 وإلا نضع 0
    def encode_illnesses(self, illness):

        list = [0] * len(self.illnesses)
        if not illness:
            return list
        for ill_id in illness:
            index = self.illness_id.get(ill_id)
            if index is not None:
                list[index] = 1
        return list