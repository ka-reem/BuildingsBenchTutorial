from buildings_bench.models.base_model import BaseModel
import torch
import torch.nn as nn

class MyModel(BaseModel):

    def __init__(self,
                 hidden_size,
                 context_len=168,
                 pred_len=24,
                 continuous_loads=True,
                 **args):
        """Init method for MyModel.

        Args:
            hidden_size (int): size of hidden layer
            context_len (int): length of context window
            pred_len (int): length of prediction window
            continuous_loads (bool): whether this model uses continuous load values
        """
        super().__init__(context_len, pred_len, continuous_loads)

        # Our model will be a simple MLP with two hidden layers
        # and will output two values (mean and std dev) for each hour.
        self.mlp = nn.Sequential(
            nn.Linear(context_len, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, pred_len*2)
        )

    def forward(self, x):
        """
        `x` is a dictionary with the following keys:

        ```
        'load': torch.Tensor,               # (batch_size, seq_len, 1)
        'building_type': torch.LongTensor,  # (batch_size, seq_len, 1)
        'day_of_year': torch.FloatTensor,   # (batch_size, seq_len, 1)
        'hour_of_day': torch.FloatTensor,   # (batch_size, seq_len, 1)
        'day_of_week': torch.FloatTensor,   # (batch_size, seq_len, 1)
        'latitude': torch.FloatTensor,      # (batch_size, seq_len, 1)
        'longitude': torch.FloatTensor,     # (batch_size, seq_len, 1)
        ```

        This model only uses the 'load'.
        """
        # (batch_size, self.context_len)
        x = x['load'][:, :self.context_len, 0]
        out = self.mlp(x)  # (batch_size, self.pred_len*2)
        return out.view(-1, self.pred_len, 2) # (batch_size, self.pred_len, 2)

    def loss(self, x, y):
        """
        Args:
            x (torch.Tensor): preds of shape (batch_size, seq_len, 2)
            y (torch.Tensor): targets of shape (batch_size, seq_len, 1)
        Returns:
            loss (torch.Tensor): scalar loss
        """
        return nn.functional.gaussian_nll_loss(x[:, :, 0].unsqueeze(2), y,
                                       nn.functional.softplus(x[:, :, 1].unsqueeze(2))**2)

    def predict(self, x):
        """
        Args:
            x (Dict): dictionary of input tensors
        Returns:
            predictions (torch.Tensor): of shape (batch_size, pred_len, 1)
            distribution_parameters (torch.Tensor): of shape (batch_size, pred_len, -1)
        """
        out = self.forward(x)
        means = out[:, :, 0].unsqueeze(2)
        stds = nn.functional.softplus(out[:, :, 1].unsqueeze(2))
        return means, torch.cat([means, stds], dim=2)

    def unfreeze_and_get_parameters_for_finetuning(self):
        """For transfer learning."""
        return self.parameters()

    def load_from_checkpoint(self, checkpoint_path):
        """Describe how to load model from a checkpoint."""
        self.load_state_dict(torch.load(checkpoint_path)['model'])
