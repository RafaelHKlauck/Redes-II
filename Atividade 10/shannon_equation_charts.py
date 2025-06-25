

import numpy as np
import matplotlib.pyplot as plt

SNRs = [1000, 5000, 10000, 50000]

bandas = np.array([1000, 5000, 10000])

plt.figure(figsize=(10, 6))
for snr in SNRs:
    C = bandas * np.log2(1 + snr)
    plt.plot(bandas / 1000, C / 1000, marker='o', label=f"S/N = {snr}")

plt.title("Capacidade do Canal (C) vs Banda (B) para diferentes valores de S/N")
plt.xlabel("Banda (kHz)")
plt.ylabel("Capacidade (kbit/s)")
plt.grid(True)
plt.legend(title="Relação S/N")
plt.tight_layout()
plt.show()
