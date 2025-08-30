import numpy as np
import os

def create_weak_learner(feature_idx, threshold, polarity, error, alpha=0):
    return {
        "feature_idx": feature_idx,
        "threshold": threshold,
        "polarity": polarity,
        "error": error,
        "alpha": alpha
    }

def adaboost_train(X, y, num_classifiers=10):
    n_samples, n_features = X.shape
    weights = np.ones(n_samples) / n_samples
    weak_classifiers = []

    for t in range(num_classifiers):
        print(f"\n=== Training Weak Classifier {t+1}/{num_classifiers} ===")
        best_feature, best_threshold, best_polarity, min_error = None, None, None, float('inf')

        for f_idx in range(n_features):
            feature_values = X[:, f_idx]
            thresholds = np.unique(feature_values)

            for threshold in thresholds:
                for polarity in [1, -1]:
                    predictions = np.ones(n_samples)
                    predictions[polarity * feature_values < polarity * threshold] = 0
                    error = np.sum(weights[predictions != y])

                    if error < min_error:
                        min_error = error
                        best_threshold = threshold
                        best_polarity = polarity
                        best_feature = f_idx

        eps = 1e-10
        alpha = 0.5 * np.log((1 - min_error) / (min_error + eps))
        wl = create_weak_learner(best_feature, best_threshold, best_polarity, min_error, alpha)
        weak_classifiers.append(wl)

        predictions = np.ones(n_samples)
        predictions[best_polarity * X[:, best_feature] < best_polarity * best_threshold] = 0
        weights *= np.exp(-alpha * (2*y-1) * (2*predictions-1))
        weights /= np.sum(weights)

        print(f"Selected Feature: {best_feature}, Threshold: {best_threshold}, Error: {min_error:.4f}, Alpha: {alpha:.4f}")

    return weak_classifiers

def adaboost_predict(X, weak_classifiers):
    final_prediction = np.zeros(X.shape[0])
    for wl in weak_classifiers:
        predictions = np.ones(X.shape[0])
        predictions[wl["polarity"] * X[:, wl["feature_idx"]] < wl["polarity"] * wl["threshold"]] = 0
        final_prediction += wl["alpha"] * (2*predictions - 1)
    return (final_prediction >= 0).astype(int)

if __name__ == "__main__":
    X = np.load("./aug_dataset/features.npy")
    y = np.load("./aug_dataset/y.npy")

    weak_classifiers = adaboost_train(X, y, num_classifiers=10)
    y_pred = adaboost_predict(X, weak_classifiers)
    acc = np.mean(y_pred == y)
    print("Training accuracy:", acc)

    # Save classifier
    if not os.path.exists("./classifiers"):
        os.makedirs("./classifiers")
    np.save("./classifiers/stage1_classifier.npy", weak_classifiers)
    print("Stage 1 classifier saved to ./classifiers/stage1_classifier.npy")
