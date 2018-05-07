import numpy as np
import torch
from .strategy import Strategy

class EntropySamplingDropout(Strategy):
	def __init__(self, X, Y, idxs_lb, args, n_drop=10):
		super(EntropySamplingDropout, self).__init__(X, Y, idxs_lb, args)
		self.n_drop = n_drop

	def query(self, n):
		idxs_unlabed = np.arange(self.n_pool)[~self.idxs_lb]
		probs = self.predict_prob_dropout(self.X[idxs_unlabed], self.Y[idxs_unlabed], self.n_drop)
		log_probs = torch.log(probs)
		U = (probs*log_probs).sum(1)
		return idxs_unlabed[U.sort()[1][:n]]
