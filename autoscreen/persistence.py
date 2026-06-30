import json
import os
import joblib

MODELS_DIR = "models"


def save_model(
    model,
    target_id,
    metadata,
):
    """
    Save a trained model together with its metadata.
    """

    model_dir = os.path.join(MODELS_DIR, target_id)

    os.makedirs(model_dir, exist_ok=True)

    # Save sklearn model
    joblib.dump(
        model,
        os.path.join(model_dir, "model.pkl")
    )


    # Save metadata
    with open(
        os.path.join(model_dir, "metadata.json"),
        "w"
    ) as f:

        json.dump(
            metadata,
            f,
            indent=4
        )

    return model_dir

def load_model(target_id):
    model_dir = os.path.join(MODELS_DIR, target_id)

    model = joblib.load(
        os.path.join(model_dir, "model.pkl")
    )

    with open(
        os.path.join(model_dir, "metadata.json")
    ) as f:
        metadata = json.load(f)

    # with open(
    #     os.path.join(model_dir, "metrics.json")
    # ) as f:
    #     metrics = json.load(f)

    return {
        "model": model,
        "metadata": metadata,
        # "metrics": metrics
    }