"""
This script runs step 3 of the TrackML Quickstart example: Training the graph neural network.
"""

import sys
import os
import yaml
import argparse
import logging

from pytorch_lightning import Trainer

sys.path.append("../../")
from Pipelines.TrackML_Example.LightningModules.GNN.Models.interaction_gnn import InteractionGNN
from Pipelines.TrackML_Example.LightningModules.Embedding.Models.layerless_embedding import LayerlessEmbedding
from utils import headline

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser("3_Train_GNN.py")
    add_arg = parser.add_argument
    add_arg("config", nargs="?", default="pipeline_config.yaml")
    return parser.parse_args()


def train(config_file="pipeline_config.yaml"):

    logging.info(headline(" Step 3: Running GNN training "))

    with open(config_file) as file:
        all_configs = yaml.load(file, Loader=yaml.FullLoader)
    
    common_configs = all_configs["common_configs"]
    gnn_configs = all_configs["gnn_configs"]

    logging.info(headline("a) Initialising model" ))

    model = InteractionGNN(gnn_configs)

    logging.info(headline( "b) Running training" ))

    trainer = Trainer(
        gpus=common_configs["gpus"],
        max_epochs=common_configs["max_epochs"],
    )

    trainer.fit(model)

    logging.info(headline( "c) Saving model" ))

    save_directory = os.path.join(common_configs["artifact_directory"], "gnn")
    os.makedirs(save_directory, exist_ok=True)
    trainer.save_checkpoint(os.path.join(save_directory, common_configs["experiment_name"]+".ckpt"))


if __name__ == "__main__":

    args = parse_args()
    config_file = args.config

    train(config_file)    
