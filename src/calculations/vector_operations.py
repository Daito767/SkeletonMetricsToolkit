# -*- coding: utf-8 -*-
"""
Created on June 2024

@author: Ghimciuc Ioan
"""
from calculations.vicon_nexus import Marker
import numpy as np


def unit_vector(vector: np.ndarray) -> np.ndarray:
    return vector / np.linalg.norm(vector)


def get_angle_between_vectors(vector1: np.ndarray, vector2: np.ndarray) -> float:
    unit_vector1 = unit_vector(vector1)
    unit_vector2 = unit_vector(vector2)
    return np.arccos(np.dot(unit_vector1, unit_vector2))


def get_all_angles_between_vectors(vectors1: np.ndarray, vectors2: np.ndarray) -> list[float]:
    angles_between_vectors: list[float] = []

    for vector1, vector2 in zip(vectors1, vectors2):
        angle = get_angle_between_vectors(vector1, vector2)
        angle = (360 * angle) / (2 * np.pi)
        angles_between_vectors.append(angle)

    return angles_between_vectors


def normal_vector_of_plane(point1: np.ndarray, point2: np.ndarray, point3: np.ndarray) -> np.ndarray:
    # Vectori directori ai planului
    vec1 = point2 - point1
    vec2 = point3 - point1
    normal_vector = np.cross(vec1, vec2)
    return normal_vector


def project_vector_onto_vector(vector: np.ndarray, onto: np.ndarray) -> np.ndarray:
    onto_unit = unit_vector(onto)
    projection = np.dot(vector, onto_unit) * onto_unit
    return projection


def project_vector_onto_plane(vector: np.ndarray, normal: np.ndarray) -> np.ndarray:
    normal_unit = unit_vector(normal)
    projection = vector - np.dot(vector, normal_unit) * normal_unit
    return projection


def distance_between_points(point1: np.ndarray, point2: np.ndarray) -> float:
    return np.linalg.norm(point1 - point2)


def is_point_in_plane(point: np.ndarray, point_on_plane: np.ndarray, normal: np.ndarray) -> bool:
    # Vector de la punctul pe plan la punctul dat
    vec = point - point_on_plane

    # Produsul scalar ar trebui să fie zero dacă punctul este în plan
    return np.isclose(np.dot(vec, normal), 0)


# Exemplu de utilizare
if __name__ == "__main__":

    # Vectori pentru testare
    v1 = np.array([1, 0, 0])
    v2 = np.array([0, 1, 0])

    angle = get_angle_between_vectors(v1, v2)
    print(f"Unghiul dintre vectori: {angle} radiani")

    # Puncte pentru definirea unui plan
    p1 = np.array([0, 0, 0])
    p2 = np.array([1, 0, 0])
    p3 = np.array([0, 1, 0])

    normal = normal_vector_of_plane(p1, p2, p3)
    print(f"Vectorul normal al planului: {normal}")

    # Proiecția unui vector pe alt vector
    vector = np.array([2, 3, 4])
    onto = np.array([1, 0, 0])

    projection_vector = project_vector_onto_vector(vector, onto)
    print(f"Proiecția vectorului {vector} pe vectorul {onto}: {projection_vector}")

    # Proiecția unui vector pe un plan
    normal = np.array([0, 0, 1])
    projection_plane = project_vector_onto_plane(vector, normal)
    print(f"Proiecția vectorului {vector} pe planul cu normalul {normal}: {projection_plane}")

    # Verificarea dacă un punct este în plan
    point = np.array([1, 1, 0])
    point_in_plane = is_point_in_plane(point, p1, normal)
    print(f"Punctul {point} este în plan: {point_in_plane}")
