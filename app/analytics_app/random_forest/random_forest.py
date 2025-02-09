import numpy as np
from .decision_tree import DecisionTree

class RandomForest:
    def __init__(self, n_trees=10, max_depth=3, min_samples_split=2):
        self.n_trees = n_trees
        self.trees = [DecisionTree(depth=max_depth, min_samples_split=min_samples_split) for _ in range(n_trees)]

    def bootstrap_sample(self, X, y):
        indices = np.random.choice(len(y), len(y), replace=True)
        return X[indices], y[indices]

    def fit(self, X, y):
        for tree in self.trees:
            X_sample, y_sample = self.bootstrap_sample(np.array(X), np.array(y))
            tree.fit(X_sample, y_sample)

    def predict(self, X):
        predictions = np.array([tree.predict(X) for tree in self.trees])
        return np.mean(predictions, axis=0)
