import numpy as np

# Power Iteration
# Approximate dominant eigenvalue of a matrix
# Compare with NumPy result

maxIter = 1000
rtol = 1e-3

size = np.random.randint(2, 5)
A = np.random.randint(low=0, high=10, size=(size, size))
print(A)

b = np.random.rand(size, 1)
print(b)

b /= np.linalg.norm(b)

for i in range(maxIter):
    bk = A @ b
    bk /= np.linalg.norm(bk)

    if np.linalg.norm(bk - b) < rtol:
        break

    b = bk

eigenvalue = float((b.T @ A @ b)[0, 0])
print(f"dominant eigenval: {eigenvalue:.6f}")

print(f"dominant vecter: {b.ravel()}")


# Code below was made by claud for ease of use
vals, vecs = np.linalg.eig(A)
dominant_idx = np.argmax(np.abs(vals))
print(f"Dominant eigenvalue (NumPy): {vals[dominant_idx].real:.6f}")
print(f"Dominant eigenvector (NumPy):{vecs[:, dominant_idx]}")
