import numpy as np
import os
from adaboost import adaboost_train, adaboost_predict

# Load dataset
X = np.load("./aug_dataset/features.npy")
y = np.load("./aug_dataset/y.npy")

# Create folder to save classifiers
if not os.path.exists("./classifiers"):
    os.makedirs("./classifiers")

cascade_stages = 2
num_classifiers_per_stage = [5, 10]  # stage1:5 weak classifiers, stage2:10 weak classifiers

X_stage = X.copy()
y_stage = y.copy()

for stage in range(cascade_stages):
    print(f"\n=== Training Cascade Stage {stage+1}/{cascade_stages} ===")
    weak_classifiers = adaboost_train(X_stage, y_stage, num_classifiers=num_classifiers_per_stage[stage])
    y_pred = adaboost_predict(X_stage, weak_classifiers)
    acc = np.mean(y_pred == y_stage)
    print(f"Stage {stage+1} training accuracy: {acc:.4f}")

    # Save this stage classifier
    np.save(f"./classifiers/stage{stage+1}_classifier.npy", weak_classifiers)
    print(f"Stage {stage+1} classifier saved to ./classifiers/stage{stage+1}_classifier.npy")

    # Keep only positives + false positives for next stage
    positive_idx = np.where(y_stage == 1)[0]
    false_positive_idx = np.where((y_stage == 0) & (y_pred == 1))[0]
    X_stage = X_stage[np.concatenate([positive_idx, false_positive_idx])]
    y_stage = y_stage[np.concatenate([positive_idx, false_positive_idx])]

    print(f"Stage {stage+1} data for next stage: {X_stage.shape[0]} samples")
