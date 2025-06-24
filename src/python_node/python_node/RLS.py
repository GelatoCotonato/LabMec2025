import numpy as np

class RLS:
    def __init__(self, mu=0.95, sigma=100.0):
        self.mu = mu
        self.theta = np.array([[0.0], [40.0]])  # theta_0 = [m=0, b=40]
        self.Sigma = sigma * np.eye(2)         # 2x2 covariance matrix

    def update(self, x, y):
        phi = np.array([[x], [1.0]])  # regressore
        denom = self.mu + phi.T @ self.Sigma @ phi
        K = self.Sigma @ phi / denom
        error = y - phi.T @ self.theta
        self.theta = self.theta + K * error
        self.Sigma = (1 / self.mu) * (self.Sigma - K @ phi.T @ self.Sigma)

    def get_params(self):
        return self.theta.flatten()