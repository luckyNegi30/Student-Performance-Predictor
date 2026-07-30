import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

# ✅ NEW DATA (sirf 3 features)
data = {
    'study_hours': [2, 4, 6, 8, 10, 5, 7, 9],
    'attendance': [50, 60, 70, 80, 90, 65, 75, 85],
    'sleep': [4, 5, 6, 7, 8, 6, 7, 8],
    'score': [40, 55, 65, 80, 95, 60, 75, 90]
}

df = pd.DataFrame(data)

# 🔥 ONLY 3 FEATURES
X = df[['study_hours', 'attendance', 'sleep']]
y = df['score']

# Model
model = LinearRegression()
model.fit(X, y)

# Save model
joblib.dump(model, 'model.pkl')

print("✅ Model trained with 3 features successfully!")