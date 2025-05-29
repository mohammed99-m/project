from django.core.management.base import BaseCommand
from exercises.models import Program, ExerciseSchedule
from accounts.models import Profile
import numpy as np
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.model_selection import train_test_split

class Command(BaseCommand):
    help = 'Train a recommendation model based on previous programs'

    def handle(self, *args, **kwargs):
        data = []

        for program in Program.objects.all():
            try:
                profile = program.trainer
                exercises = ExerciseSchedule.objects.filter(program=program).values_list('exercise_id', flat=True)

                if profile and exercises:
                    data.append({
                        'weight': profile.weight,
                        'height': profile.height,
                        'gender': self.encode_gender(profile.gender),
                        'level': self.encode_fitness_level(profile.experianse_level),
                        'goal': self.encode_goal(profile.goal),
                        'exercises': list(exercises)
                    })
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'❌ Error in program {program.id}: {e}'))

        if not data:
            self.stdout.write(self.style.ERROR('No training data found.'))
            return

        df = pd.DataFrame(data)

        mlb = MultiLabelBinarizer()
        Y = mlb.fit_transform(df['exercises'])
        X = df[['weight', 'height', 'level', 'goal', 'gender']].values

        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
        model = RandomForestClassifier()
        model.fit(X_train, Y_train)

        joblib.dump(model, 'program_recommender_multi.joblib')
        joblib.dump(mlb, 'exercise_mlb.joblib')

        self.stdout.write(self.style.SUCCESS("✅ Model trained and saved successfully."))

    def encode_fitness_level(self, level):
        return {'beginner': 0, 'intermediate': 1, 'advanced': 2}.get(level, 0)

    def encode_goal(self, goal):
        return {'lose_weight': 0, 'build_muscle': 1, 'endurance': 2}.get(goal, 0)

    def encode_gender(self, gender):
        return {'male': 0, 'female': 1}.get(gender, 0)