import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Load dataset
df = pd.read_csv("cleaned_jobs.csv")

# Define salary bins and labels
bins = [-1, 50000, 100000, float("inf")]
labels = ["Low", "Medium", "High"]
df["salary_category"] = pd.cut(df["Salary"], bins=bins, labels=labels)

# Remove jobs with titles that were not standardized
titles = ["Backend Engineer", "Software Engineer", "AI Trainer", "Software Developer",
          "Backend Developer", "Engineer", "Developer", "Government Engineer"]
df = df[df['Title'].isin(titles)]

# Select categorical features
categorical_cols = ["Title", "Company", "Location", "Experience"]

# One-Hot Encoding for categorical features
encoder = OneHotEncoder(handle_unknown="ignore")
X_encoded = encoder.fit_transform(df[categorical_cols])

# Convert to DataFrame
X = pd.DataFrame(X_encoded.toarray(), columns=encoder.get_feature_names_out(categorical_cols))

# Define target variable
y = df["salary_category"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Logistic Regression model
classifier = LogisticRegression(max_iter=500)
classifier.fit(X_train, y_train)

# Predict salaries
df["predicted_salary"] = classifier.predict(X)

# Convert salary categories to numerical values for plotting
salary_mapping = {"Low": 1, "Medium": 2, "High": 3}
df["predicted_salary_numeric"] = df["predicted_salary"].map(salary_mapping)

# -------------------------------------------------
# **1. Histogram of Predicted Salary Distribution by Job Role**
plt.figure(figsize=(10, 6))
sns.histplot(data=df, x="predicted_salary", hue="Title", multiple="stack", palette="Set2")
plt.xlabel("Predicted Salary Category")
plt.ylabel("Count")
plt.title("Distribution of Predicted Salaries by Job Role")
plt.legend(title="Job Role", loc="upper right")
plt.show()

# -------------------------------------------------
# **2. Box Plot: Salary Distributions Across Job Roles and Locations**
plt.figure(figsize=(14, 6))
sns.boxplot(data=df, x="Title", y="predicted_salary_numeric", palette="coolwarm")
plt.xlabel("Job Role")
plt.ylabel("Predicted Salary Category (Numeric)")
plt.title("Salary Distributions Across Job Roles")
plt.xticks(rotation=45)
plt.show()

plt.figure(figsize=(14, 6))
sns.boxplot(data=df, x="Location", y="predicted_salary_numeric", palette="coolwarm")
plt.xlabel("Location")
plt.ylabel("Predicted Salary Category (Numeric)")
plt.title("Salary Distributions Across Locations")
plt.xticks(rotation=45)
plt.show()

# -------------------------------------------------
# **3. Interactive Map of Average Salaries Across Locations**
# Aggregate salary data by location
location_salary = df.groupby("Location")["predicted_salary_numeric"].mean().reset_index()

fig = px.choropleth(location_salary,
                    locations="Location",
                    locationmode="USA-states",
                    color="predicted_salary_numeric",
                    color_continuous_scale="Viridis",
                    title="Average Predicted Salary by Location")

fig.show()

# -------------------------------------------------