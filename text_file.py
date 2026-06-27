# test_model.py

from src.utils.model_loader import (
    load_admission_model
)

model = load_admission_model()

print(type(model))
print(model)