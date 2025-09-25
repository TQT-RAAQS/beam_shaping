from dataclasses import dataclass

@dataclass
class BeamShape:

    radius_x: float
    radius_y: float
    orientation: float # In radians between -90 degrees (exclusive) to +90 degrees (exclusive)
    ellipticity: float