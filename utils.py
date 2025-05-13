import json
import numpy as np


def save_model(weights: np.ndarray, mean: float, std: float, model_path: str):
    """
    Save the model weights to a file.

    Args:
        weights (np.ndarray): The model weights to save.
        mean (float): The mean used for normalization.
        std (float): The standard deviation used for normalization.
        model_path (str): The path where the model should be saved.
    """
    np.save(model_path + ".npy", weights)
    with open(model_path + "_meta.json", "w") as f:
        json.dump({"mean": mean, "std": std}, f)


def load_model(model_path: str) -> np.ndarray:
    """
    Load the model weights from a file.

    Args:
        model_path (str): The path where the model is saved.

    Returns:
        np.ndarray: The loaded model weights.
    """
    weights = np.load(model_path + ".npy")
    with open(model_path + "_meta.json", "r") as f:
        meta = json.load(f)
    return weights, meta["mean"], meta["std"]


def sigmoid(z):
    return 1 / (1 + np.exp(-z))


def substitute_sex(x: str) -> int:
    return int(x != "male")


def stone_the_adulters(x: int) -> str:  # denormalizing function
    return "male" if x == 0 else "female"


def normalize_age(x: int, mean, std) -> float:
    return (x - mean) / std
