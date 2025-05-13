import fastapi
import numpy as np
from utils import load_model, sigmoid, substitute_sex, normalize_age

app = fastapi.FastAPI()
W, mean, std = load_model("model_weights")


def predict(X: np.ndarray) -> np.ndarray:
    y = sigmoid(np.matmul(X, W))
    return float(y[0][0])


@app.post("/predict")
def predict_survival(data: dict):
    """
    Predict survival based on the input data.

    Args:
        data (dict): The input data containing passenger information.

    Returns:
        dict: The prediction result.
    """
    # Normalize the input data
    X = np.array(
        [
            data["p_class"],
            substitute_sex(data["sex"]),
            normalize_age(data["age"], mean, std),
            data["sib_sp"],
            data["par_ch"],
            1,  # Bias
        ]
    ).reshape(1, -1)

    # Make the prediction

    prediction = predict(X)

    return {"survival_chance": prediction}
