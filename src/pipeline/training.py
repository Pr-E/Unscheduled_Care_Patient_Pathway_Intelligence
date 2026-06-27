import logging

from src.modelling.train_models import ModellingPipeline

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class TrainingPipeline:

    def __init__(self):
        self.modelling_pipeline = ModellingPipeline()


    def train(self):
        logging.info("Starting training pipeline...")

        results = self.modelling_pipeline.run()

        logging.info("Training pipeline completed successfully.")

        return results


if __name__ == "__main__":
    pipeline = TrainingPipeline()
    pipeline.train()