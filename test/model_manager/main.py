from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from model_manager import *


if __name__ == "__main__":
    model_loader = ModelManager.PickleLoaderSaver("model_metadata.pkl")
    model_manager = ModelManager()
    model_manager.add(
        ModelMetadata(name="model", version="1.0", path="model.pkl", additional={"type": "regression"})
        .save_model({"weights": [0.1, 0.2, 0.3]})
    )
    model_manager.save(model_loader)
    model_manager.load(model_loader)
    metadata = model_manager.find(ModelMetadata.Filter())

    # =======

    category_results, model_results = model_manager.find(
        ModelManager.Category.Filter(
            name="model",
            models=[
                ModelMetadata.Filter(name="model"),
                ModelMetadata.Filter(name="another_model")
            ],
            categories=[
                ModelManager.Category.Filter(
                    name="subcategory",
                    models=[
                        ModelMetadata.Filter(name="sub_model")
                    ]
                )
            ]
        )
    )

    # =======

    if len(metadata) > 0:
        for meta in metadata:
            meta.name = "model"
            model = meta.load_model()
            print(f"Loaded model: {meta.name}, Version: {meta.version}")
            print(model)
    else:
        print("No matching model found.")
    model_manager.save(model_loader)