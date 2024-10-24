import numpy as np
from scipy.integrate import quad

# Heston Model characteristic function
def heston_charfunc(phi, S0, v0, kappa, theta, sigma, rho, lambd, tau, r):
    a = kappa * theta
    b = kappa + lambd
    rspi = rho * sigma * phi * 1j
    d = np.sqrt((rho * sigma * phi * 1j - b) ** 2 + (phi * 1j + phi ** 2) * sigma ** 2)
    g = (b - rspi + d) / (b - rspi - d)

    exp1 = np.exp(r * phi * 1j * tau)
    term2 = S0 ** (phi * 1j) * ((1 - g * np.exp(d * tau)) / (1 - g)) ** (-2 * a / sigma ** 2)
    exp2 = np.exp(a * tau * (b - rspi + d) / sigma ** 2 + v0 * (b - rspi + d) *
                  ((1 - np.exp(d * tau)) / (1 - g * np.exp(d * tau))) / sigma ** 2)

    return exp1 * term2 * exp2

# Integrand function for option price calculation
def integrand(phi, S0, v0, kappa, theta, sigma, rho, lambd, tau, r, K):
    args = (S0, v0, kappa, theta, sigma, rho, lambd, tau, r)
    numerator = np.exp(r * tau) * heston_charfunc(phi - 1j, *args) - K * heston_charfunc(phi, *args)
    denominator = 1j * phi * K ** (1j * phi)
    return numerator / denominator

# Option price calculation using numerical integration
def heston_price(S0, K, v0, kappa, theta, sigma, rho, lambd, tau, r):
    args = (S0, v0, kappa, theta, sigma, rho, lambd, tau, r, K)
    real_integral, err = np.real(quad(integrand, 0, 100, args=args))
    return (S0 - K * np.exp(-r * tau)) / 2 + real_integral / np.pi

# Test the Heston model
if __name__ == "__main__":
    S0 = 100.  # initial asset price
    K = 100.  # strike price
    v0 = 0.1  # initial variance
    r = 0.03  # risk-free rate
    kappa = 1.5768  # mean reversion rate
    theta = 0.0398  # long-term variance
    sigma = 0.3  # volatility of volatility
    lambd = 0.575  # variance risk premium
    rho = -0.5711  # correlation between stock price and variance
    tau = 1.  # time to maturity

    price = heston_price(S0, K, v0, kappa, theta, sigma, rho, lambd, tau, r)
    print(f"Option Price: {price}")
