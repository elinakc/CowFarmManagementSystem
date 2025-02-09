import numpy as np

class DecisionTree:
    def __init__(self, depth=3, min_samples_split=2):
        self.depth = depth
        self.min_samples_split = min_samples_split
        self.tree = None

    def gini_impurity(self, y):
        _, counts = np.unique(y, return_counts=True)
        probabilities = counts / counts.sum()
        return 1 - np.sum(probabilities ** 2)

    def best_split(self, X, y):
        best_feature, best_value, best_score = None, None, float('inf')
        for feature_idx in range(X.shape[1]):
            values = np.unique(X[:, feature_idx])
            for value in values:
                left_mask = X[:, feature_idx] <= value
                right_mask = ~left_mask

                if sum(left_mask) < self.min_samples_split or sum(right_mask) < self.min_samples_split:
                    continue

                left_gini = self.gini_impurity(y[left_mask])
                right_gini = self.gini_impurity(y[right_mask])
                weighted_gini = (sum(left_mask) * left_gini + sum(right_mask) * right_gini) / len(y)

                if weighted_gini < best_score:
                    best_feature, best_value, best_score = feature_idx, value, weighted_gini

        return best_feature, best_value

    def build_tree(self, X, y, depth=0):
        if depth >= self.depth or len(np.unique(y)) == 1:
            return np.mean(y)

        feature, value = self.best_split(X, y)
        if feature is None:
            return np.mean(y)

        left_mask = X[:, feature] <= value
        right_mask = ~left_mask

        return {
            'feature': feature,
            'value': value,
            'left': self.build_tree(X[left_mask], y[left_mask], depth + 1),
            'right': self.build_tree(X[right_mask], y[right_mask], depth + 1)
        }

    def fit(self, X, y):
        self.tree = self.build_tree(np.array(X), np.array(y))

    def predict_sample(self, tree, x):
        if isinstance(tree, dict):
            if x[tree['feature']] <= tree['value']:
                return self.predict_sample(tree['left'], x)
            else:
                return self.predict_sample(tree['right'], x)
        return tree

    def predict(self, X):
        return [self.predict_sample(self.tree, x) for x in np.array(X)]
