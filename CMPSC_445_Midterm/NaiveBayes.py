import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
from sklearn.metrics import ConfusionMatrixDisplay
import matplotlib.pyplot as plt
from sklearn.model_selection import GridSearchCV

# Load the dataset
df = pd.read_csv("cleaned_jobs.csv")

# Define salary bins and labels
bins = [-1, 50000, 100000, float("inf")]  # Example thresholds
labels = ["Low", "Medium", "High"]

# Convert salary into categorical labels
df["salary_category"] = pd.cut(df["Salary"], bins=bins, labels=labels)

# Encode categorical salary labels
label_encoder = LabelEncoder()
df["salary_category_encoded"] = label_encoder.fit_transform(df["salary_category"])

# Remove jobs with titles that were not standardized
titles = ["Backend Engineer", "Software Engineer", "AI Trainer", "Software Developer",
          "Backend Developer", "Engineer", "Developer", "Government Engineer"]
df = df[df['Title'].isin(titles)]

# Define categorical columns to be one-hot encoded
categorical_cols = ['Title', 'Company', 'Location', 'Experience']
df = pd.get_dummies(df, columns=categorical_cols)

# Define X and y
X = df.drop(columns=["Salary", "salary_category", "salary_category_encoded"])  # Features
y = df["salary_category_encoded"]  # Target variable

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define parameter grid for MultinomialNB
param_grid = {
    'alpha': [0.1, 0.5, 1.0, 5.0, 10.0]  # Smoothing parameter for Naive Bayes
}

# Create a MultinomialNB classifier
classifier = MultinomialNB()

# Create GridSearchCV object
grid_search = GridSearchCV(estimator=classifier, param_grid=param_grid, cv=5, scoring='accuracy')

# Fit the GridSearchCV object to the training data
grid_search.fit(X_train, y_train)

# Print the best parameters and best score
print("Best parameters:", grid_search.best_params_)
print("Best cross-validation score:", grid_search.best_score_)

# Use the best estimator to make predictions on the test set
y_pred = grid_search.best_estimator_.predict(X_test)
y_pred_train = grid_search.best_estimator_.predict(X_train)

# Evaluate the model on training data
print("Training data performance:")
cm1 = confusion_matrix(y_train, y_pred_train)
ac1 = accuracy_score(y_train, y_pred_train)
print("Accuracy:", ac1)
print("Classification Report:\n", classification_report(y_train, y_pred_train, target_names=label_encoder.classes_))

# Display Confusion Matrix
labels = label_encoder.inverse_transform(sorted(set(y_train) | set(y_pred_train)))
disp = ConfusionMatrixDisplay(confusion_matrix=cm1, display_labels=labels)
disp.plot()
plt.show()

# Evaluate the model on test data
cm = confusion_matrix(y_test, y_pred)
ac = accuracy_score(y_test, y_pred)
print("Test data performance:")
print("Accuracy:", ac)
print("Classification Report:\n", classification_report(y_test, y_pred, target_names=label_encoder.classes_))

# Display Confusion Matrix
labels = label_encoder.inverse_transform(sorted(set(y_test) | set(y_pred)))
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)
disp.plot()
plt.show()