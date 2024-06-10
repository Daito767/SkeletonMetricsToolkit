# -*- coding: utf-8 -*-
"""
Created on June 2024

@author: Ghimciuc Ioan
"""

from viconnexusapi import ViconNexus
import numpy


class Marker:
    def __init__(self, name: str, marker_trajectory: tuple, start_frame: int, end_frame: int):
        self.name: str = name
        self.is_exist_trajectory: list[bool] = marker_trajectory[3]
        self.trajectory = numpy.column_stack((marker_trajectory[0][start_frame - 1:end_frame],
                                             marker_trajectory[1][start_frame - 1:end_frame],
                                             marker_trajectory[2][start_frame - 1:end_frame]))

    def __str__(self) -> str:
        return self.name


class ViconNexusAPI(ViconNexus.ViconNexus):
    def __init__(self):
        super().__init__()

    def GetMarkers(self, subject_name: str) -> dict[str, Marker]:
        start_frame, end_frame = self.GetTrialRegionOfInterest()

        markers: dict[str, Marker] = {}

        for marker_name in self.GetMarkerNames(subject_name):
            marker_trajectory = self.GetTrajectory(subject_name, marker_name)
            markers[marker_name] = Marker(marker_name, marker_trajectory, start_frame, end_frame)

        return markers
