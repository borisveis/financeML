import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 10, 100)
y = np.sin(x)

plt.figure(figsize=(8, 5))
plt.plot(x, y, label="Sine Wave", color="blue", linewidth=2)
plt.xlabel("X values")
plt.ylabel("Sine of X")
plt.title("Sine Wave Plot")
plt.legend()

# Ensure the plot stays open
plt.show(block=True)
