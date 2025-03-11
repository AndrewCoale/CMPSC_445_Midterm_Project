import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("cleaned_jobs.csv")

# Define salary bins and labels
bins = [-1, 50000, 100000, float("inf")]
labels = ["Low", "Medium", "High"]

# Convert salary into categorical labels
df["salary_category"] = pd.cut(df["Salary"], bins=bins, labels=labels)

# Remove jobs with titles that were not standardized
titles = ["Backend Engineer", "Software Engineer", "AI Trainer", "Software Developer",
          "Backend Developer", "Engineer", "Developer", "Government Engineer"]
df = df[df['Title'].isin(titles)]

# Select categorical features
categorical_cols = ["Title", "Company", "Location", "Experience"]

# One-Hot Encoding for categorical features
encoder = OneHotEncoder(handle_unknown="ignore")  # No `sparse=False`
X_encoded = encoder.fit_transform(df[categorical_cols])  # Transformed into sparse matrix

# Convert sparse matrix to DataFrame
X = pd.DataFrame(X_encoded.toarray(), columns=encoder.get_feature_names_out(categorical_cols))

# Define target variable
y = df["salary_category"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define hyperparameter grid
param_grid = {"C": [0.01, 0.1, 1, 10, 100]}

# Create a Logistic Regression model
classifier = LogisticRegression(max_iter=500)

# Use GridSearchCV to optimize C
grid_search = GridSearchCV(classifier, param_grid, cv=5, scoring="accuracy")
grid_search.fit(X_train, y_train)

# Get the best model
best_model = grid_search.best_estimator_

# Make predictions
y_pred = best_model.predict(X_test)
y_pred_train = best_model.predict(X_train)

# Evaluate model on train data
print("Training data performance:")
accuracy1 = accuracy_score(y_train, y_pred_train)
print(f"Best parameters: {grid_search.best_params_}")
print(f"Accuracy: {accuracy1:.4f}")

# Display classification report
print("\nClassification Report:\n", classification_report(y_train, y_pred_train))

# Confusion Matrix
cm1 = confusion_matrix(y_train, y_pred_train)
disp1 = ConfusionMatrixDisplay(confusion_matrix=cm1, display_labels=best_model.classes_)
disp1.plot()
plt.show()

# Evaluate model on test data
print("Test data performance:")
accuracy = accuracy_score(y_test, y_pred)
print(f"Best parameters: {grid_search.best_params_}")
print(f"Accuracy: {accuracy:.4f}")

# Display classification report
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=best_model.classes_)
disp.plot()
plt.show()