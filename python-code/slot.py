"""
File created by Samuel Bakker.
Contains the Slot-class used in simulation.py.
"""
#simple data container representing one time slot in the schedule. 
#It stores four things: startTime (when the slot begins
#appTime (when patients are told to arrive — this changes per rule)
#slotType (elective/urgent/overtime) and patientType. 
#The weekSchedule in the simulation is a 6×42 grid of these objects.
class Slot:
    """
    Class for a slot in the Simulation.

    Attributes
    ----------
    startTime: float
        start time of the slot (in hours)
    appTime: float
        appointment time of the slot, dependent on type and rule (in hours)
    slotType: int
        type of slot (0=none, 1=elective, 2=urgent within normal working hours, 3=urgent in overtime)
    patientType: int
        (0=none, 1=elective, 2=urgent)
    """

    startTime: float
    appTime: float
    slotType: int
    patientType: int
