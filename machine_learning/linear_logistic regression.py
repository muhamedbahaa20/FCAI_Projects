#MLAss1_
# 20201211_Hesham ahmed mohamed
# 20200449_mohamed sayed khalil
# 20200434_mohamed bahaa elden
# 20200230_salma mourad galal
# 20210609_abdelrahman elhossini mobarak
# import numpy as np
# import matplotlib.pyplot as plt
#
# def compute_cost(X, y, theta):
#     m = len(y)
#     predictions = X.dot(theta)
#     cost = (1/(2*m)) * np.sum(np.square(predictions - y))
#     return cost
#
# def gradient_descent(X, y, theta, learning_rate, n_iterations):
#     m = len(y)
#     cost_history = np.zeros(n_iterations)
#
#     for iteration in range(n_iterations):
#         predictions = X.dot(theta)
#         errors = predictions - y
#         gradient = (1/m) * X.T.dot(errors)
#         theta = theta - learning_rate * gradient
#         cost_history[iteration] = compute_cost(X, y, theta)
#
#     return theta, cost_history
#
# # Generate some random data for demonstration
# np.random.seed(42)
# X = 2 * np.random.rand(100, 1)
# y = 4 + 3 * X + np.random.randn(100, 1)
#
# # Add a bias term to X
# X_b = np.c_[np.ones((100, 1)), X]
#
# # Initialize random weights
# theta = np.random.randn(2, 1)
#
# # Set learning rate and number of iterations
# learning_rate = 0.01
# n_iterations = 1000
#
# # Perform gradient descent
# theta, cost_history = gradient_descent(X_b, y, theta, learning_rate, n_iterations)
#
# # Print the final theta values
# print("Final Theta:", theta)
#
# # Plot the cost history over iterations
# plt.plot(range(1, n_iterations + 1), cost_history, color='blue')
# plt.xlabel('Iterations')
# plt.ylabel('Cost')
# plt.title('Cost History over Iterations')
# plt.show()
#
# # Plot the original data and the regression line
# plt.scatter(X, y)
# plt.plot(X, X_b.dot(theta), color='red', linewidth=3)
# plt.xlabel('X')
# plt.ylabel('y')
# plt.title('Linear Regression with Gradient Descent')
# plt.show()


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

from sklearn.metrics import r2_score, mean_squared_error
from sklearn import svm
from sklearn.model_selection import train_test_split
#from sklearn.metrics import accuracy_score

df = pd.read_csv('TSLA.csv')

df = df.drop('Date', axis=1)

null_counts = df.isnull().sum()
print(null_counts)


data = df.describe().round(2)
print(data)


#task 3
range_values = df.max() - df.min()
print("\nRange values:\n", range_values.round(1))
df_standardized = (df - df.mean()) / df.std()
print("\nStandardized data:\n", df_standardized.round(2))
df = df_standardized

# #task 4
X = df.drop('Close', axis=1).values
y = df['Close'].values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = svm.SVR(kernel='linear')
model.fit(X_train, y_train)
predictions = model.predict(X_test)
#
# #task 5
#
r2 = r2_score(y_test, predictions)
print('R2 Score:', r2)
mse=mean_squared_error(y_test,predictions)
print('MSE:',mse)
###################################
# Function fit_GD
# Input: X, y
# Output: theta
# 1: Initialize theta
# 2: Set alpha and max_iterations
# 3: for i=0 to max_iterations
# 4: Compute the hypothesis function values according to the equation: h=thetaT*X
#       5: for j=0 to theta.length
#           6: Compute the partial derivative of the error: part_der=(1/m)*sum((h-y)*Xj )
#           7: Update thetaj according to the equation: thetaj=thetaj-alpha*part_der
#       8: end
# 9: end
###################################


# y_pred = linear_reg_model.predict(X_test)
#
# r2 = r2_score(y_test, y_pred)
# print("R2Score:",r2)
#
#
# print("..........................................................................................\n")
# print("..........................................................................................\n")
#
# data_new =pd.read_csv("loan_new.csv")
#
# df_new = pd.DataFrame(data_new)
# df_new = df_new.drop('Loan_ID', axis=1)
# df_new.dropna(subset=['Gender','Married','Dependents','Loan_Tenor','Credit_History'], inplace=True)
# print(df_new)
#
# print("..........................................................................................\n")
# print("..........................................................................................\n")
# df_new.info()
#
#
#
# numerical_columns = ['Income','Coapplicant_Income','Loan_Tenor']
#
#
# ranges = df_new[numerical_columns].max() - df_new[numerical_columns].min()
#
# print("..........................................................................................\n")
# print("..........................................................................................\n")
# print("Ranges of numerical features:")
# print(ranges)
#
# plt.figure(figsize=(12, 6))
# sns.boxplot(data=df_new[numerical_columns])
# plt.title("Box Plots of Numerical Features Before Standardization")
# plt.xlabel("Numerical Features")
# plt.ylabel("Values")
# plt.show()
#
#
# sns.pairplot(df_new[numerical_columns])
# plt.show()
#
#
#
#
#
# categorical_features = ['Gender','Married','Dependents','Education', 'Property_Area']
#
#
# label_encoder = LabelEncoder()
# for feature in categorical_features:
#     df_new[feature] = label_encoder.fit_transform(df_new[feature])
#
#
#
#
# scaler = StandardScaler()
#
# df_new[numerical_columns]=scaler.fit_transform(df_new[numerical_columns])
#
# #linear
# y_pred_new = linear_reg_model.predict(df_new)
# print("Linear : \n")
# print(y_pred_new)
# print("..........................................................................................\n")
# print("..........................................................................................\n")
#
# #.....................................................................................................................
#
# y_train_single = y_train[:, 0]
# y_test_single = y_test[:, 0]
#
# learning_rates = [0.001, 0.01, 0.1, 1]
# num_iterations = 100
# accuracies = []
#
# for learning_rate in learning_rates:
#
#     theta = np.zeros(X_train.shape[1])
#
#
#     for i in range(num_iterations):
#
#         h = 1 / (1 + np.exp(-np.dot(X_train, theta)))
#
#
#         gradient = (1 / len(y_train_single)) * np.dot(X_train.T, (h - y_train_single))
#
#
#         theta = theta - learning_rate * gradient
#
#
#     y_pred_logistic = 1 / (1 + np.exp(-np.dot(X_test, theta)))
#
#
#     accuracy_logistic = np.mean((y_pred_logistic > 0.5) == y_test_single)
#     accuracies.append(accuracy_logistic)
#
#     print(f"Logistic Regression Accuracy (learning rate {learning_rate}): {accuracy_logistic}")
#
# print("..........................................................................................\n")
# print("..........................................................................................\n")
# print("logistic: \n")
# print(y_pred_logistic)






#############################################
#naive bayes
#############################################

# import numpy as np
# from collections import defaultdict
#
# def fit_NB(X, y, alpha=1):
#     model_parameters = defaultdict(dict)
#     classes = np.unique(y)
#
#     for c in classes:
#         c_rows = X[y == c]
#         n_class = len(c_rows)
#         c_prior = n_class / len(y)
#         model_parameters[c]['prior'] = c_prior
#
#         for j in range(X.shape[1]):  # Iterate over features
#             xj_categories = np.unique(X[:, j])
#             n_xj = len(xj_categories)
#
#             for t in xj_categories:
#                 n_t = np.sum(c_rows[:, j] == t)
#                 cond_prob = (n_t + alpha) / (n_class + alpha * n_xj)
#
#                 model_parameters[c][(j, t)] = cond_prob
#
#     return model_parameters
#
# # Example usage:
# # Assuming X is your feature matrix and y is your target variable
# X = np.array([[1, 'A'], [2, 'B'], [1, 'A'], [2, 'B'], [2, 'A']])
# y = np.array(['Y', 'N', 'Y', 'N', 'Y'])
#
# model_params = fit_NB(X, y)
#
# # Print the learned parameters
# for c, params in model_params.items():
#     print(f'Class {c}:')
#     print(f'Prior: {params["prior"]}')
#     for key, value in params.items():
#         if key != 'prior':
#             print(f'P({key[0]}={key[1]}|Class={c}): {value}')
#     print('\n')

