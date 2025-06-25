# Defining a Recursive Least Square Estimator to find a line that approximates the points closest to the coast

import numpy as np

class RLS:
    def __init__(self, mu=0.95, sigma=100.0):
        self.mu = mu                            # forgetting factor
        self.theta = np.array([[0.0], [50.0]])  # theta_0 = [m=0, b=50]
        self.Sigma = sigma * np.eye(2)          # 2x2 covariance matrix

    def update(self, x, y):
        # Getting the Regressor
        phi = np.array([[x], [1.0]])                                       
        denom = self.mu + phi.T @ self.Sigma @ phi
        # Getting the Gain
        K = self.Sigma @ phi / denom                                      
        error = y - phi.T @ self.theta 
        # Parameter estimation
        self.theta = self.theta + K * error   
        # Updating covariance matrix                             
        self.Sigma = (1 / self.mu) * (self.Sigma - K @ phi.T @ self.Sigma)

    def get_params(self):
        return self.theta.flatten()