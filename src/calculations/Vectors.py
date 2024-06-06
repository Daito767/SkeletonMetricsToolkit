# -*- coding: utf-8 -*-
"""
Created on June 2024

@author: Ghimciuc Ioan
"""

import numpy
from ViconNexus import Marker


def unit_vector(vector) -> numpy.ndarray:
    return vector / numpy.linalg.norm(vector)


def get_angle_between_vectors(vector1: numpy.ndarray, vector2: numpy.ndarray) -> float:
    unit_vector1 = unit_vector(vector1)
    unit_vector2 = unit_vector(vector2)

    return numpy.arccos(numpy.dot(unit_vector1, unit_vector2))


def get_all_angles_between_vectors(vectors1: numpy.ndarray, vectors2: numpy.ndarray) -> list[float]:
    angle_between_vectors: list[float] = []

    for vector1, vector2 in zip(vectors1, vectors2):
        angle = get_angle_between_vectors(vector1, vector2)
        angle = (360 * angle) / (2 * numpy.pi)
        angle_between_vectors.append(angle)

    return angle_between_vectors


def get_normal_to_plane(vector1: numpy.ndarray, vector2: numpy.ndarray) -> numpy.ndarray:
    return unit_vector(numpy.cross(vector1, vector2))


def get_vector_projection(vector1: numpy.ndarray, vector2: numpy.ndarray) -> numpy.ndarray:
    vector2 = unit_vector(vector2)
    return vector2 * numpy.dot(vector1, vector2)
