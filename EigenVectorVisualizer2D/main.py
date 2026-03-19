import matplotlib as mpl
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np

"""Visualize Eigenvectors

Generate random 2x2 matrix

Compute eigenvectors

Plot transformation of unit circle

"""


def det(mat):
    return mat[0][0] * mat[1][1] - mat[0][1] * mat[1][0]


def trace(mat):
    return mat[0][0] + mat[1][1]


A = np.random.randint(low=0, high=10, size=(2, 2))

# eigenvalue equation: 0 = det(A - λI)   expand and take determinant 0 = (a - λ)(d - λ) - bc => λ^2 - dλ - aλ + ad - bc => λ^2 - (d+a)λ - (ad - bc)

# quadratic equation values
# a = 1
# b = trace(A) or a+d
# c = det(A) or ad - bc

a = 1

c = det(A)

b = -trace(A)

dsc = b * b - 4 * c * a

lambda1 = (trace(A) + np.sqrt(dsc)) / 2.0
lambda2 = (trace(A) - np.sqrt(dsc)) / 2.0

iMat1 = ((A[0][0] - lambda1, A[0][1]), (A[1][0], A[1][1] - lambda1))
iMat2 = ((A[0][0] - lambda2, A[0][1]), (A[1][0], A[1][1] - lambda2))

# use (a - λ)x + by = 0 to solve for y
# or if b = 0
# use cx + (d - λ)y = 0 to solve for x

# use x = 1 as a placeholder
#  y = -x(a - λ)/b
#
# if b = 0
#
# use y = 1 as a placeholder
# x = -y(d - λ)/c

# Solve eigenvector, x and y compenents for λ1
if iMat1[0][1] == 0:
    y1 = 1
    x1 = -y1 * (iMat1[1][1]) / iMat1[1][0]
else:
    x1 = 1
    y1 = -x1 * (iMat1[0][0]) / iMat1[0][1]

# Solve eigenvector, x and y compenents for λ2
if iMat2[0][1] == 0:
    y2 = 1
    x2 = -y2 * (iMat2[1][1]) / iMat2[1][0]

else:
    x2 = 1
    y2 = -x2 * (iMat2[0][0]) / iMat2[0][1]


v1mag = np.sqrt(x1 * x1 + y1 * y1)
v2mag = np.sqrt(x2 * x2 + y2 * y2)

v1unit = (x1 / v1mag, y1 / v1mag)
v2unit = (x2 / v2mag, y2 / v2mag)

print(A)
print(v1unit)
print(v2unit)

fig, ax = plt.subplots()

circle = mpatches.Circle((0, 0), radius=1, fill=False, color="blue")
ax.add_patch(circle)

ax.quiver(
    0, 0, v1unit[0], v1unit[1], angles="xy", scale_units="xy", scale=1, color="red"
)
ax.quiver(
    0, 0, v2unit[0], v2unit[1], angles="xy", scale_units="xy", scale=1, color="blue"
)

ax.set_xlim(-1.2, 1.2)
ax.set_ylim(-1.2, 1.2)
ax.set_aspect("equal")

fig.savefig("circle.pdf")
plt.show()
