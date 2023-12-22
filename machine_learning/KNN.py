# # MLAss2
# # 20201211_Hesham ahmed mohamed
# # 20200449_mohamed sayed khalil
# # 20200434_mohamed bahaa elden
# # 20200230_salma mourad galal
# # 20210609_abdelrahman elhossini mobarak


import csv
import random
import math
# Function to load data from CSV file, skipping the header
def load_csv(filename):
    dataset = []
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the header row
        for row in csv_reader:
            dataset.append([float(x) for x in row])
    return dataset


# Function to split the dataset into training and testing sets
def split_dataset(dataset, split_ratio):
    train_size = int(len(dataset) * split_ratio)
    train_set = []
    test_set = list(dataset)
    while len(train_set) < train_size:
        index = random.randrange(len(test_set))
        train_set.append(test_set.pop(index))
    return [train_set, test_set]


# Function to calculate Euclidean distance between two instances
def euclidean_distance(instance1, instance2):
    distance = 0
    for i in range(len(instance1) - 1):
        distance += (instance1[i] - instance2[i]) ** 2
    return math.sqrt(distance)


# Function to normalize dataset using Min-Max Scaling
def min_max_scaling(dataset):
    min_values = [min(column) for column in zip(*dataset)]
    max_values = [max(column) for column in zip(*dataset)]
    for row in dataset:
        for i in range(len(row) - 1):
            row[i] = (row[i] - min_values[i]) / (max_values[i] - min_values[i])


# Function to perform KNN classification with distance-weighted voting
def knn_classify(train_set, test_instance, k):
    distances = []
    for train_instance in train_set:
        dist = euclidean_distance(test_instance, train_instance)
        distances.append((train_instance, dist))
    distances.sort(key=lambda x: x[1])

    votes = {}
    for i in range(k):
        neighbor = distances[i][0]
        label = neighbor[-1]
        weight = 1 / (distances[i][1] + 1e-10)
        votes[label] = votes.get(label, 0) + weight

    # Break ties using distance-weighted voting
    max_vote_label = max(votes, key=votes.get)
    return max_vote_label


# Function to evaluate the accuracy of predictions
def evaluate_accuracy(test_set, predictions):
    correct = 0
    for i in range(len(test_set)):
        if test_set[i][-1] == predictions[i]:
            correct += 1
    return correct


# Main function
def main():
    filename = 'diabetes.csv'
    dataset = load_csv(filename)
    min_max_scaling(dataset)

    split_ratio = 0.7
    train_set, test_set = split_dataset(dataset, split_ratio)

    k_values = [2, 3, 4, 5, 6]  # You can add more k values to test

    total_accuracy = 0

    for k in k_values:
        predictions = []
        for test_instance in test_set:
            prediction = knn_classify(train_set, test_instance, k)
            # print(prediction)
            predictions.append(prediction)

        correct_instances = evaluate_accuracy(test_set, predictions)
        total_instances = len(test_set)
        accuracy = correct_instances / total_instances * 100.0

        print(f'k value: {k}')
        print(f'Number of correctly classified instances: {correct_instances}')
        print(f'Total number of instances: {total_instances}')
        print(f'Accuracy: {accuracy:.2f}%\n')

        total_accuracy += accuracy

    avg_accuracy = total_accuracy / len(k_values)
    print(f'Average accuracy across all iterations: {avg_accuracy:.2f}%')



main()




