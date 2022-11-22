from __future__ import annotations
import numpy as np

trans_probs_3_state = np.array([
    [0.00, 0.05, 0.95],
    [0.20, 0.00, 0.80],
    [0.95, 0.05, 0.00],
])

t_array = []
states = trans_probs_3_state.shape[0]
for i in range(states):
    for j in range(states):
        if trans_probs_3_state[i, j] != 0:
            t_array.append((i, j, np.log(trans_probs_3_state[i, j])))

print(t_array)
for From, to, prob in t_array:
    print(f"V(i, {to}) = max( V(i, {to}), {prob} + V(i-1, {From})")
