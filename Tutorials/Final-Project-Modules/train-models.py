# ------------------- #
# --- Do Not Edit --- #
# ------------------- #

import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from buildings_bench import load_torch_dataset
from buildings_bench.models import model_factory

import tomli
from pathlib import Path
import os 
import time
import json
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


class DataHandler:
    def __init__(self, batch_size=32):
        self.batch_size = batch_size

    def load_dataset(self, dataset_name, scaler_transform):
        from buildings_bench import load_torch_dataset
        return list(load_torch_dataset(
            dataset_name,
            apply_scaler_transform=scaler_transform,
            scaler_transform_path=Path(os.environ["TRANSFORM_PATH"])
        ))

    def create_dataloader(self, dataset):
        return DataLoader(dataset, batch_size=self.batch_size, shuffle=False)

class TimeSeriesSinusoidalPeriodicEmbedding(nn.Module):
    def __init__(self, embedding_dim: int):
        super().__init__()
        self.linear = nn.Linear(2, embedding_dim)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = torch.cat([torch.sin(torch.pi * x), torch.cos(torch.pi * x)], dim=2)
        return self.linear(x)

class Model(nn.Module):
    DEFAULT_CONTEXT_LEN = 168
    DEFAULT_PRED_LEN = 24

    def __init__(self, activation):
        super().__init__()
        self.context_len = self.DEFAULT_CONTEXT_LEN
        self.pred_len = self.DEFAULT_PRED_LEN
        self.activation = self._get_activation(activation)
        self.embeddings = self._create_embeddings()

    def _create_embeddings(self):
        return nn.ModuleDict({
            'power': nn.Linear(1, 64),
            'building': nn.Embedding(2, 32),
            'lat': nn.Linear(1, 32),
            'lon': nn.Linear(1, 32), 
            'day_of_year': TimeSeriesSinusoidalPeriodicEmbedding(32),
            'day_of_week': TimeSeriesSinusoidalPeriodicEmbedding(32),
            'hour_of_day': TimeSeriesSinusoidalPeriodicEmbedding(32)
        })

    def _get_activation(self, name):
        return {
            "relu": nn.ReLU(),
            "tanh": nn.Tanh(),
            "gelu": nn.GELU(),
            "leaky_relu": nn.LeakyReLU()
        }.get(name.lower(), nn.ReLU())

    def _data_pre_process(self, x):
        lat = self.embeddings['lat'](x['latitude'])
        lon = self.embeddings['lon'](x['longitude'])
        btype = self.embeddings['building'](x['building_type'].squeeze(-1))
        load = self.embeddings['power'](x['load'])
        day_of_year = self.embeddings['day_of_year'](x['day_of_year'])            
        day_of_week = self.embeddings['day_of_week'](x['day_of_week'])            
        hour_of_day = self.embeddings['hour_of_day'](x['hour_of_day']) 
        return torch.cat([lat, lon, btype, day_of_year, day_of_week, hour_of_day, load], dim=2)

class NN(Model):
    def __init__(self, activation):
        super().__init__(activation)
        self.model = self._build_model()

    def _build_model(self):
        input_dim = self.context_len * 256
        return nn.Sequential(
            nn.Linear(input_dim, 128), 
            self.activation,
            nn.Linear(128, self.pred_len)
        )

    def forward(self, x):
        ts_embed = self._data_pre_process(x)
        x_flat = ts_embed[:, :self.context_len, :].reshape(x['load'].shape[0], -1)
        return self.model(x_flat).unsqueeze(-1)


class RNN(Model):
    def __init__(self, activation="relu"):
        super().__init__(activation)
        self.rnn1, self.rnn2, self.output_layer = self._build_model()

    def _build_model(self):
        rnn1 = nn.RNN(256, 128, batch_first=True)
        rnn2 = nn.RNN(128, 128, batch_first=True)
        output_layer = nn.Linear(128, self.pred_len)
        return rnn1, rnn2, output_layer

    def forward(self, x):
        ts_embed = self._data_pre_process(x)
        out1, _ = self.rnn1(ts_embed)
        out2, _ = self.rnn2(out1)
        last_hidden = self.activation(out2[:, -1, :])
        return self.output_layer(last_hidden).unsqueeze(-1)

class LSTM(Model):
    def __init__(self, activation="relu"):
        super().__init__(activation)
        self.lstm1, self.lstm2, self.output_layer = self._build_model()

    def _build_model(self):
        lstm1 = nn.LSTM(256, 128, batch_first=True)
        lstm2 = nn.LSTM(128, 128, batch_first=True)
        output_layer = nn.Linear(128, self.pred_len)
        return lstm1, lstm2, output_layer

    def forward(self, x):
        ts_embed = self._data_pre_process(x)
        out1, _ = self.lstm1(ts_embed)
        out2, _ = self.lstm2(out1)
        last_hidden = self.activation(out2[:, -1, :])
        return self.output_layer(last_hidden).unsqueeze(-1)

class GRU(Model):
    def __init__(self, activation="relu"):
        super().__init__(activation)
        self.gru1, self.gru2, self.output_layer = self._build_model()

    def _build_model(self):
        gru1 = nn.GRU(256, 128, batch_first=True)
        gru2 = nn.GRU(128, 128, batch_first=True)
        output_layer = nn.Linear(128, self.pred_len)
        return gru1, gru2, output_layer

    def forward(self, x):
        ts_embed = self._data_pre_process(x)
        out1, _ = self.gru1(ts_embed)
        out2, _ = self.gru2(out1)
        last_hidden = self.activation(out2[:, -1, :])
        return self.output_layer(last_hidden).unsqueeze(-1)

class Trainer:
    def __init__(self, model_name, device, scaler_transform, dataset_name, epochs, train_buildings, test_buildings, activation='relu', optimizer_name='adam', lr=1e-3):
        self.model_name = model_name
        self.device = device
        self.scaler_transform = scaler_transform
        self.dataset_name = dataset_name
        self.epochs = epochs
        self.train_buildings = train_buildings
        self.test_buildings = test_buildings
        self.activation = activation
        self.optimizer_name = optimizer_name
        self.lr = lr
        self.model = self._load_model()
        self.optimizer = self._get_optimizer()
        self.loss_fn = nn.MSELoss()
        self.handler = DataHandler(batch_size=32)
        self.path = os.path.join(os.getcwd(), self.dataset_name, self.model_name, self.activation, self.optimizer_name, f'epochs-{self.epochs}') ##
        os.makedirs(self.path, exist_ok=True)

    def _load_model(self):
        model_map = {
            'NN': NN,
            'RNN': RNN,
            'LSTM': LSTM,
            'GRU': GRU, 
            'MyNN': MyNN
        }
        return model_map[self.model_name](activation=self.activation).to(self.device)

    def _get_optimizer(self):
        opt_map = {
            'adam': torch.optim.Adam,
            'sgd': torch.optim.SGD,
            'adamw': torch.optim.AdamW
        }
        optimizer_cls = opt_map.get(self.optimizer_name.lower(), torch.optim.Adam)
        return optimizer_cls(self.model.parameters(), lr=self.lr)

    def train(self):
        self.model.train()
        log = []
        start_time = time.time()  # Start timer
        for epoch in range(self.epochs):
            total_loss = 0.0
            for building_id, building_dataset in self.train_buildings:
                dataloader = self.handler.create_dataloader(building_dataset)
                for batch in dataloader:
                    for key, value in batch.items():
                        batch[key] = value.to(self.device)
                    self.optimizer.zero_grad()
                    predictions = self.model(batch)
                    targets = batch['load'][:, self.model.context_len:, 0]
                    loss = self.loss_fn(predictions[:, :, 0], targets)
                    loss.backward()
                    self.optimizer.step()
                    total_loss += loss.item()
            print(f"[{self.model_name}] Epoch {epoch + 1}: Loss = {total_loss:.4f}")
            log.append({"epoch": epoch + 1, "loss": total_loss})
        train_duration = time.time() - start_time  # End timer
        with open(os.path.join(self.path, "train_loss.json"), "w") as f:
             json.dump({"train_loss": log, "train_duration": train_duration}, f, indent=2)
        return train_duration

    def evaluate(self):
        self.model.eval()
        results = {}
        mae_total = 0.0
        rmse_total = 0.0
        r2_total = 0.0
        count = 0
        for building_id, building_dataset in self.test_buildings:
            inverse_transform = building_dataset.datasets[0].load_transform.undo_transform
            dataloader = self.handler.create_dataloader(building_dataset)
            
            target_list = []
            prediction_list = []
            load_list = []
            
            with torch.no_grad():
                for batch in dataloader:
                    for key, value in batch.items():
                        batch[key] = value.to(self.device)

                    
                    predictions = self.model(batch)
                    targets = batch['load'][:, self.model.context_len:]
                    loads = batch['load'][:, :self.model.context_len]
                    
                    targets = inverse_transform(targets)
                    predictions = inverse_transform(predictions)
                    loads = inverse_transform(loads)
                    
                    prediction_list.append(predictions.detach().cpu())
                    target_list.append(targets.detach().cpu())
                    load_list.append(loads.detach().cpu())
            
            predictions_all = torch.cat(prediction_list)
            targets_all = torch.cat(target_list)
            load_all = torch.cat(load_list)
            
            mae = torch.abs(predictions_all - targets_all).mean().item()
            rmse = torch.sqrt(((predictions_all - targets_all) ** 2).mean()).item()
            r2 = 1 - (((predictions_all - targets_all) ** 2).sum() / ((targets_all - targets_all.mean()) ** 2).sum()).item()
            mae_total += mae
            rmse_total += rmse
            r2_total += r2
            count += 1
            results[building_id] = {
                "load": load_all.tolist(),
                "predictions": predictions_all.tolist(),
                "targets": targets_all.tolist()
            }
        with open(os.path.join(self.path, "predictions.json"), "w") as f:
            json.dump(results, f, indent=2)
        eval_metrics = {
            "mae": mae_total / count,
            "rmse": rmse_total / count,
            "r2": r2_total / count}
        with open(os.path.join(self.path, "evaluate_model.json"), "w") as f:
            json.dump(eval_metrics, f, indent=2)
        return results, eval_metrics["mae"], eval_metrics["rmse"], eval_metrics["r2"]

# ------------------- #
# --- Do Not Edit --- #
# ------------------- #
# ------------------- #
# ------ Edit ------- #
# ------------------- #

# dataset_names = ["ideal"] # TODO: Provide the dataset name as a list using the format [dataset_name] instead of passing it as a variable
# # TODO: Explore at least 30 different combinations using all four models
# model_classes = ["NN", "RNN", "LSTM", "GRU"]
# activations = ["relu", "tanh", "leaky_relu", "gelu"]
# optimizers = ["adam", "sgd", "adamw"]
# epoch_options = [5, 10, 15]

dataset_names = ["ideal"] # TODO: Provide the dataset name as a list using the format [dataset_name]
# TODO: Explore at least 30 different combinations using all four models
# model_classes = ["NN"]
# activations = ["relu"]
# optimizers = ["adam"]
# epoch_options = [1]

# 30 diff combinations
model_classes = ["NN", "RNN", "LSTM", "GRU"]
activations = ["relu", "tanh", "leaky_relu", "gelu"]
optimizers = ["adam", "sgd", "adamw"]
# epoch_options = [5, 10, 15]
epoch_options = [3]


# ------------------- #
# ------ Edit ------- #
# ------------------- #


# ------------------- #
# --- Do Not Edit --- #
# ------------------- #

class MyNN(Model):
     def __init__(self):
         pass

os.environ["REPO_PATH"] = "/global/cfs/cdirs/m4388/Project4/BuildingsBench"
os.environ["BUILDINGS_BENCH"] = "/global/cfs/cdirs/m4388/Project4/Dataset"
os.environ["TRANSFORM_PATH"] = "/global/cfs/cdirs/m4388/Project4/Dataset/metadata/transforms"
device = "cuda:0" if torch.cuda.is_available() else "cpu"

for dataset_name in dataset_names:
    print(f"\n=== Dataset: {dataset_name} ===")
    handler = DataHandler(batch_size=32)
    all_buildings = handler.load_dataset(dataset_name, scaler_transform="boxcox")
    train_buildings = all_buildings[:int(0.8 * len(all_buildings))]
    test_buildings = all_buildings[int(0.8 * len(all_buildings)):]
    for model_class in model_classes:
        for activation in activations:
            for optimizer_name in optimizers:
                for epochs in epoch_options:
                    print(f"\n--- Training {model_class} | Activation: {activation} | Optimizer: {optimizer_name} | Epochs: {epochs} ---")
                    trainer = Trainer(
                        model_name=model_class,
                        device=device,
                        dataset_name=dataset_name,
                        epochs=epochs,
                        train_buildings=train_buildings,
                        test_buildings=test_buildings,
                        scaler_transform="boxcox",
                        activation=activation,
                        optimizer_name=optimizer_name,
                        lr=1e-3)
                    train_duration = trainer.train()
                    results, mae, rmse, r2 = trainer.evaluate()
                    print(f"[{model_class}] MAE: {mae:.4f}, RMSE: {rmse:.4f}, R²: {r2:.4f}")
                    print(f"Training Time: {train_duration:.2f} seconds")
                    
# ------------------- #
# --- Do Not Edit --- #
# ------------------- #

# to run
# sbatch /pscratch/sd/k/kareem8/BuildingsBenchTutorial/Tutorials/Final-Project-Modules/run_pi.slurm
