import csv
import os
from typing import *


def update_visibility(widgets: Dict[str, List[Any]], workout_type: str) -> None:
    """
    Updates the visibiliity of UI widgets

    Args:
        widgets (Dict[str, List[Any]]): A dictionary maps workout types to lists of widgets
        workout_type (str): The selected workout type.
    """
    for key, group in widgets.items():
        is_visible = key == workout_type
        for widget in group:
            widget.setVisible(is_visible)


def validate_positive_fields(**fields: Optional[str]) -> None:
    """
    Validates that all fields contain pos. numbers.
    
    Args:
        **fields: arguments where keys are the field names, and values are their contents.

    Raises:
        ValueError: If any field is not a positive number or is invalid.
    """
    for field_name, value in fields.items():
        if value is not None and value.strip():
            try:
                num = int(value)
                if num <= 0:
                    raise ValueError(f"{field_name} must be a positive number")
            except ValueError:
                raise ValueError(f"{field_name} must be a positive number.")


def save_workout(
    day: str,
    workout_type: str,
    cardio_intensity: Optional[str] = None,
    cardio_duration: Optional[str] = None,
    weight_exercise: Optional[str] = None,
    weight: Optional[str] = None,
    weight_sets: Optional[str] = None,
    weight_reps: Optional[str] = None,
    mobility_stretch: Optional[str] = None,
    mobility_duration: Optional[str] = None,
) -> None:
    """
    Saves a workout entry to the workout data file

    Args:
        day (str): Day of the workout
        workout_type (str): Type of worokut (Cardio, Weight Training, Mobility).
        cardio_intensity (Optional[str], optional): The intensity of the cardio workout. Defaults to None
        cardio_duration (Optional[str], optional): The duration of the cardio workout. Defaults to None.
        weight_exercise (Optional[str], optional): The weight exercise performed. Defaults to None.
        weight (Optional[str], optional): The weight used in the workout. Defaults to None.
        weight_sets (Optional[str], optional): The number of sets in the workout. Defaults to None.
        weight_reps (Optional[str], optional): The number of repetitions per set. Defaults to None.
        mobility_stretch (Optional[str], optional): The stretch performed during mobility training. Defaults to None.
        mobility_duration (Optional[str], optional): The duration of the mobility workout. Defaults to None.
    """

    validate_positive_fields(
        Duration=cardio_duration if workout_type == "Cardio" else mobility_duration,
        Weight=weight if workout_type == "Weight Training" else None,
        Sets=weight_sets if workout_type == "Weight Training" else None,
        Reps=weight_reps if workout_type == "Weight Training" else None,
    )
    data = [
        day,
        workout_type,
        cardio_intensity or "",
        cardio_duration or "",
        weight_exercise or "",
        weight or "",
        weight_reps or "",
        weight_sets or "",
        mobility_stretch or "",
        mobility_duration or "",
    ]

    with open("data/workout_data.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(data)


def clear_workouts() -> None:
    """
    Clears all workout data by deleting the workout data file if it exists.
    """
    if os.path.exists("data/workout_data.csv"):
        os.remove("data/workout_data.csv")


def read_workouts() -> Dict[str, List[str]]:
    """
    Reads all workout entries from the workout CSV file.

    Returns:
        Dict[str, List[str]]: A dictionary that maps days to a list of workout details.
    """
    workouts = {}
    with open("data/workout_data.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if not row:
                continue

            (
                day,
                workout_type,
                cardio_intensity,
                cardio_duration,
                weight_exercise,
                weight,
                weight_reps,
                weight_sets,
                mobility_stretch,
                mobility_duration,
            ) = row

            if workout_type == "Cardio":
                details = f"Cardio: Intensity {cardio_intensity}, Duration: {cardio_duration} mins"
            elif workout_type == "Weight Training":
                details = f"Weight Training: {weight_exercise}, Weight: {weight} lbs, Sets: {weight_sets}, Reps: {weight_reps}"
            elif workout_type == "Mobility":
                details = f"Mobility: Stretch: {mobility_stretch}, Duration: {mobility_duration} mins"
            else:
                continue

            if day not in workouts:
                workouts[day] = []
            workouts[day].append(details)
    return workouts


def remove_workouts(entries: List[str]) -> None:
    """
    Removes selected workout entries from the workout CSV file.

    Args:
        entries (List[str]): A List of workout details to be removed
    """

    if not os.path.exists("data/workout_data.csv"):
        return

    # sets are faster ?
    to_remove = set(entries)
    new_lines = []

    with open("data/workout_data.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if not row:
                continue

            (
                day,
                workout_type,
                cardio_intensity,
                cardio_duration,
                weight_exercise,
                weight,
                weight_reps,
                weight_sets,
                mobility_stretch,
                mobility_duration,
            ) = row

            if workout_type == "Cardio":
                details = f"Cardio: Intensity {cardio_intensity}, Duration: {cardio_duration} mins"
            elif workout_type == "Weight Training":
                details = (
                    f"Weight Training: {weight_exercise}, Weight: {weight} lbs, "
                    f"Sets: {weight_sets}, Reps: {weight_reps}"
                )
            elif workout_type == "Mobility":
                details = f"Mobility: Stretch: {mobility_stretch}, Duration: {mobility_duration} mins"
            else:
                details = None

            if details not in to_remove:
                new_lines.append(row)

    with open("data/workout_data.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(new_lines)
