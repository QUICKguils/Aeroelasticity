"""Flutter identification with the half power point method."""

import numpy as np
import matplotlib.pyplot as plt

import labdata as ld

extracted_signals = ld.extract_accelerations(ld.EXTRACT_BOUNDS)
