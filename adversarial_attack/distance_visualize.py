""" Visualize distances of HSJA manually """

# -*- coding: utf-8 -*-
import os

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams

TARGET_MODEL = "inception"
ATTACK_METHOD = "hsj"
BUDGET_LEVEL = 1
SAVE_DIST_PLOT = True

THRESHOLD = {
  1: 64 / 255,
  2: 72 / 255,
  3: 80 / 255,
  4: 88 / 255,
}

DIST_FILE_PATH = os.path.join(
  "hsja_dists",
  TARGET_MODEL,
  "hsja_{:.3f}_dist.txt".format(THRESHOLD[BUDGET_LEVEL]),
)
# DIST_FILE_PATH = "hsja_{:.3f}_dist.txt".format(THRESHOLD[BUDGET_LEVEL])

DIST_PLOT_SAVE_PATH = os.path.join("dist_plots", TARGET_MODEL)
DIST_PLOT_SAVE_NAME = "{}_level{}_dist".format(ATTACK_METHOD, BUDGET_LEVEL)


def plot_distances(distances, save_plot=False):
  """ Plot distances between adversaries and originals for HSJA. """

  rcParams["font.family"] = "monospace"
  cmap = plt.cm.Dark2

  indice = np.arange(0, len(distances), 1)
  plt.scatter(
    indice, distances, c=[cmap(i) for i in np.linspace(0, 1, len(distances))],
  )
  plt.axhline(y=THRESHOLD[BUDGET_LEVEL], color=cmap(0))

  plt.ylabel("Distance")
  # plt.ylim(0, THRESHOLD[BUDGET_LEVEL] * 1.2)
  plt.ylim(0, 0.6)

  plt.xlabel("Adversaries")
  plt.title(
    "Attack: {} - Level: {} - Threshold: {:.5f}".format(
      ATTACK_METHOD, BUDGET_LEVEL, THRESHOLD[BUDGET_LEVEL]
    )
  )
  plt.grid(axis="y")

  if save_plot:
    if not os.path.exists(DIST_PLOT_SAVE_PATH):
      os.makedirs(DIST_PLOT_SAVE_PATH)
    plt.savefig(
      os.path.join(DIST_PLOT_SAVE_PATH, DIST_PLOT_SAVE_NAME), dpi=100,
    )

  plt.show()


def main():
  """ Read file and plot! """
  dist_str = []

  # Read HSJA distance file
  with open(DIST_FILE_PATH, "r") as f:
    for line in f.readlines():
      dist_str.append(line)

  dists = np.array(dist_str).astype(np.float32)
  plot_distances(dists, save_plot=SAVE_DIST_PLOT)


if __name__ == "__main__":
  main()
