import fastapi
import numpy as np
from pydantic import BaseModel, Field
from utils import load_model, sigmoid, substitute_sex, normalize_age

app = fastapi.FastAPI()
W, mean, std = load_model("model_weights")


class PassengerData(BaseModel):
    passenger_class: int = Field(..., ge=1, le=3, description="Passenger class (1-3)")
    sex: str = Field(..., pattern="^(male|female)$", description="Passenger sex")
    age: float = Field(..., ge=0, lt=100, description="Passenger age")
    siblings_spouses: int = Field(..., ge=0, description="Number of siblings/spouses aboard")
    parents_children: int = Field(..., ge=0, description="Number of parents/children aboard")


def predict(X: np.ndarray) -> np.ndarray:
    y = sigmoid(np.matmul(X, W))
    return float(y[0][0])


@app.post("/predict")
def predict_survival(data: PassengerData):
    """
    Predict survival based on the input data.

    Args:
        data (PassengerData): The validated input data containing passenger information.

    Returns:
        dict: The prediction result with survival chance.
    """
    # Normalize the input data
    X = np.array(
        [
            data.passenger_class,
            substitute_sex(data.sex),
            normalize_age(data.age, mean, std),
            data.siblings_spouses,
            data.parents_children,
            1,  # Bias
        ]
    ).reshape(1, -1)

    prediction = predict(X)

    return {"survival_chance": prediction}
