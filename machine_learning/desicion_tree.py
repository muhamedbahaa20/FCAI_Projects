#    #MLAss2
# # 20201211_Hesham ahmed mohamed
# # 20200449_mohamed sayed khalil
# # 20200434_mohamed bahaa elden
# # 20200230_salma mourad galal
# # 20210609_abdelrahman elhossini mobarak

###############desicion tree#############################################
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import numpy as np
import matplotlib.pyplot as plt


# Load the dataset
df = pd.read_csv('drug.csv')
df.info()
print('\n .........................................................................................................')
# Handle missing values
# Assuming empty cells are represented by NaN
# df= df.drop('Na_to_K', axis=1)
# df.ffill(inplace=True)  # Use forward fill to fill missing values
df= df.dropna()
df.info()
print('\n .........................................................................................................')
df_shuffle = df.sample(frac=1, random_state=42).reset_index(drop=True)
# Encode categorical variables
label_encoder = LabelEncoder()
df['Sex'] = label_encoder.fit_transform(df['Sex'])
df['Cholesterol'] = label_encoder.fit_transform(df['Cholesterol'])
df['BP'] = label_encoder.fit_transform(df['BP'])
df['Drug']=label_encoder.fit_transform(df['Drug'])

numerical_columns = ['Age','Na_to_K']

scaler = StandardScaler()
df[numerical_columns]=scaler.fit_transform(df[numerical_columns])

X = df[['Age', 'Sex', 'BP', 'Cholesterol','Na_to_K']]
y = df['Drug']

#first Experiment

# Repeat the experiment five times with different random splits
for i in range(5):

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=i)

    # Create and fit the decision tree model
    model = DecisionTreeClassifier()
    model.fit(X_train, y_train)

    # Make predictions on the test set
    y_pred = model.predict(X_test)

    # Calculate and print accuracy
    tree_size = model.tree_.node_count
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Experiment ({i+1}):")
    print(f"Size: {tree_size}")
    print(f"Accuracy: {accuracy}")


#Second Experiment
print('\n .........................................................................................................')

# Initialize lists to store statistics
mean_accuracies = []
max_accuracies = []
min_accuracies = []
mean_tree_sizes = []
max_tree_sizes = []
min_tree_sizes = []
results = []
# Range of training set sizes (30% to 70% in increments of 10%)
for train_size in np.arange(0.3, 0.71, 0.1):
    train_size = round(train_size, 2)

    accuracies = []
    tree_sizes = []

    # Repeat the experiment with five different random seeds
    for i in range(5):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=1-train_size, random_state=i)

        # Create and fit the decision tree model
        model = DecisionTreeClassifier()
        model.fit(X_train, y_train)

        # Make predictions on the test set
        y_pred = model.predict(X_test)

        # Calculate accuracy and tree size
        accuracy = accuracy_score(y_test, y_pred)
        tree_size = model.tree_.node_count

        accuracies.append(accuracy)
        tree_sizes.append(tree_size)

    # Calculate and store statistics
    mean_accuracies.append(np.mean(accuracies))
    max_accuracies.append(np.max(accuracies))
    min_accuracies.append(np.min(accuracies))
    mean_tree_sizes.append(np.mean(tree_sizes))
    max_tree_sizes.append(np.max(tree_sizes))
    min_tree_sizes.append(np.min(tree_sizes))

    results.append({
        'Training Set Size': train_size,
        'Mean Accuracy': mean_accuracies,
        'Max Accuracy': max_accuracies,
        'Min Accuracy': min_accuracies,
        'Mean Tree Size': mean_tree_sizes,
        'Max Tree Size': max_tree_sizes,
        'Min Tree Size': min_tree_sizes
    })

# Create a DataFrame from the results
report_df = pd.DataFrame(results)

# Save the report to a CSV file
report_df.to_csv('experiment_report.csv', index=False)

# Create plots
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.plot(np.arange(0.3, 0.71, 0.1), mean_accuracies, label='Mean Accuracy')
plt.plot(np.arange(0.3, 0.71, 0.1), max_accuracies, label='Max Accuracy')
plt.plot(np.arange(0.3, 0.71, 0.1), min_accuracies, label='Min Accuracy')
plt.xlabel('Training Set Size')
plt.ylabel('Accuracy')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(np.arange(0.3, 0.71, 0.1), mean_tree_sizes, label='Mean Tree Size')
plt.plot(np.arange(0.3, 0.71, 0.1), max_tree_sizes, label='Max Tree Size')
plt.plot(np.arange(0.3, 0.71, 0.1), min_tree_sizes, label='Min Tree Size')
plt.xlabel('Training Set Size')
plt.ylabel('Number of Nodes in Tree')
plt.legend()

plt.tight_layout()
plt.show()
