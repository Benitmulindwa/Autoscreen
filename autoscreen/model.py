import numpy as np

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import (
    StratifiedKFold,
    cross_validate
)


def train_model(X, y):

    X = np.array(X)
    y = np.array(y)

    clf = RandomForestClassifier(
        n_estimators=300,
        random_state=42,
        n_jobs=-1
    )

    cv = StratifiedKFold(
        n_splits=5,
        shuffle=True,
        random_state=42
    )

    results = cross_validate(
        clf,
        X,
        y,
        cv=cv,
        scoring=["roc_auc", "accuracy"],
        return_train_score=True
    )

    print("\n=== Cross Validation Results ===")
    print(f"Mean Train AUC : {results['train_roc_auc'].mean():.4f}")
    print(f"Mean Test AUC  : {results['test_roc_auc'].mean():.4f}")
    print(f"Mean Accuracy  : {results['test_accuracy'].mean():.4f}")

    # Train final model on ALL available data
    clf.fit(X, y)

    return {
        "model": clf,
        "train_auc": results["train_roc_auc"].mean(),
        "test_auc": results["test_roc_auc"].mean(),
        "accuracy": results["test_accuracy"].mean()
    }