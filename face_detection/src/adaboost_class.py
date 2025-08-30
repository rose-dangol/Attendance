import numpy as np

class WeakLearner:
    def __init__(self, feature_idx, threshold, polarity, error):
        self.feature_idx = feature_idx
        self.threshold = threshold
        self.polarity = polarity
        self.error = error
        self.alpha = 0  # Weight assigned later

class AdaBoost:
    def __init__(self, num_classifiers=10):
        self.num_classifiers = num_classifiers
        self.weak_classifiers = []

    def train(self, X, y, features):
        """
        X         : N x F array → feature values for all samples
        y         : N array → labels (1 for face, 0 for non-face)
        features  : list of Haar features (already computed)
        """
        n_samples, n_features = X.shape
        
        # Step 1: Initialize uniform weights for all training samples
        weights = np.ones(n_samples) / n_samples

        for t in range(self.num_classifiers):
            print(f"\n=== Training Weak Classifier {t+1}/{self.num_classifiers} ===")

            best_feature = None
            min_error = float("inf")
            best_threshold = None
            best_polarity = None

            # Step 2: For every Haar feature → find the best threshold & polarity
            for f_idx in range(n_features):
                feature_values = X[:, f_idx]
                thresholds = np.unique(feature_values)

                for threshold in thresholds:
                    for polarity in [1, -1]:
                        predictions = np.ones(n_samples)
                        predictions[polarity * feature_values < polarity * threshold] = 0

                        # Calculate weighted error
                        error = np.sum(weights[predictions != y])

                        if error < min_error:
                            min_error = error
                            best_threshold = threshold
                            best_polarity = polarity
                            best_feature = f_idx

            # Step 3: Compute alpha (weight of weak classifier)
            eps = 1e-10  # to prevent division by zero
            alpha = 0.5 * np.log((1 - min_error) / (min_error + eps))

            # Step 4: Save this weak classifier
            wl = WeakLearner(best_feature, best_threshold, best_polarity, min_error)
            wl.alpha = alpha
            self.weak_classifiers.append(wl)

            # Step 5: Update sample weights
            predictions = np.ones(n_samples)
            predictions[best_polarity * X[:, best_feature] < best_polarity * best_threshold] = 0

            weights *= np.exp(-alpha * (2 * y - 1) * (2 * predictions - 1))
            weights /= np.sum(weights)

            print(f"Selected Feature: {best_feature}, Threshold: {best_threshold}, Error: {min_error:.4f}, Alpha: {alpha:.4f}")

    def predict(self, X):
        # Combine all weak learners into a strong classifier
        final_prediction = np.zeros(X.shape[0])
        for wl in self.weak_classifiers:
            predictions = np.ones(X.shape[0])
            predictions[wl.polarity * X[:, wl.feature_idx] < wl.polarity * wl.threshold] = 0
            final_prediction += wl.alpha * (2 * predictions - 1)
        return (final_prediction >= 0).astype(int)



''' to run '''

# Suppose we already extracted Haar features into X and labels into y
# X → shape (num_samples, num_features)
# y → shape (num_samples,), values are 1 (face) or 0 (non-face)

adaboost = AdaBoost(num_classifiers=10)
adaboost.train(X, y, features=None)

# Prediction on the same dataset
y_pred = adaboost.predict(X)
accuracy = np.mean(y_pred == y)
print("Training Accuracy:", accuracy)
