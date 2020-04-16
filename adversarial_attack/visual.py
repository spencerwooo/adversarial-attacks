#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Visualize results from saved *.npy files.

Files:
  * Images (and adversarial examples):
    `*.npy`: visualize with the first two cells.
  * L2/L∞ norms:
    `*.npy`: scatter plot with the last few cells.

"""

# pylint: disable=invalid-name
# %%
import numpy as np
import matplotlib.pyplot as plt


def img_to_np(image):
  """ Transpose image to viewable format to plot/visualize. """
  return np.transpose(image, (1, 2, 0))


# %%
adv = np.load("adv.npy")
img = np.load("img.npy")
pert = adv - img
_l2 = np.linalg.norm(pert)

# %%
plt.figure()
plt.subplot(1, 3, 1)
plt.imshow(img_to_np(img).squeeze())
plt.subplot(1, 3, 2)
plt.imshow(img_to_np(adv).squeeze())
plt.subplot(1, 3, 3)
plt.imshow(img_to_np(adv - img).squeeze())

# %%
THRESHOLD = 4

indice = np.arange(0, 100, 1)
# dist_fgsm = np.load("dist_fgsm.npy")
# dist_deep_fool = np.load("dist_deep_fool.npy")
dist_cw = np.load("cw_dist_lim_1.npy")

fig = plt.figure()
ax = fig.add_axes([0, 0, 1, 1])
# ax.scatter(indice, dist_fgsm, label="fgsm, l2")
# ax.scatter(indice, dist_deep_fool, label="deep fool, l2")

ax.scatter(indice, dist_cw, label="cw, l2")

# ax.set_ylim(0, 8)
ax.set_ylabel("L2 norm distance")
ax.set_xlabel("Image index")
ax.legend()

plt.hlines(y=THRESHOLD, xmin=0, xmax=100, colors="r")
plt.ylim(0, THRESHOLD * 1.2)
plt.title("ResNet adversaries perturbation size (l2 norm)")
plt.show()

print(
  "L_{}: min {:.4f}, mean {:.4f}, max {:.4f}".format(
    "2", dist_cw.min(), np.median(dist_cw), dist_cw.max()
  )
)
