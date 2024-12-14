import csv
import os
import typing


def toggle_visibility(widgets, workout_type: str) -> None:
    """
    Toggles the visibiliity of UI widgets

    Args:
        widgets:  list of widgets
        workout_type: Selected workout type.
    """
    for key, group in widgets.items():
        is_visible = key == workout_type
        for widget in group:
            widget.setVisible(is_visible)


def validate_fields(**fields: str) -> None:
    """
    Validates that all fields contain pos. numbers.
    
    Args:
        **fields: field names and their values.

    Raises:
        ValueError: If a field is invalid or negative.
    """
    for field_name, value in fields.items():
        if value is not None:
            value = str(value).strip()
            try:
                num = int(value)
                if num <= 0:
                    raise ValueError(f"{field_name} must be a positive number")
            except ValueError:
                raise ValueError(f"{field_name} must be a positive number.")


def save_workout(
    day: str,
    workout_type :str,
    cardio_intensity: str = None,
    cardio_duration: str = None,
    weight_exercise: str = None,
    weight: str = None,
    weight_sets: str = None,
    weight_reps: str = None,
    mobility_stretch: str = None,
    mobility_duration: str = None,
) -> None:
    """
    Saves a workout entry to the workout data file

    Args:
        day: Day of the workout
        workout_type: Type of worokut (Cardio, Weight Training, Mobility).
        cardio_intensity: Intensity of the cardio.
        cardio_duration: Duration of cardio (mins)
        weight_exercise: Exercise performed (Weight Training)
        weight: Weight used (lbs)
        weight_sets: Number of sets.
        weight_reps: Number of reps.
        mobility_stretch: Strecth name (Mobilty)
        mobility_duration: Duration of workout (mins)
    """

    validate_fields(
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
    Deletes all workouts
    """
    if os.path.exists("data/workout_data.csv"):
        os.remove("data/workout_data.csv")


def read_workouts() -> None:
    """
    Reads the workout entries from the CSV file.

    Returns:
        workouts: a list of workout details.
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
            workouts.setdefault(day, []).append(details)
    return workouts


def remove_workouts(entries: str) -> None:
    """
    Removes the selected workout entries from the workout CSV file.

    Args:
        entries: List of workouts to be removed
    """

    if not os.path.exists("data/workout_data.csv"):
        return

    to_remove = [(day, workout) for day, workout in entries]
    new_lines = []

    with open("data/workout_data.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if not row:
                continue

            day = row[0]
            workout_type = row[1]

            if workout_type == "Cardio":
                details = f"Cardio: Intensity {row[2]}, Duration: {row[3]} mins"
            elif workout_type == "Weight Training":
                details = f"Weight Training: {row[4]}, Weight: {row[5]} lbs, Sets: {row[6]}, Reps: {row[7]}"
            elif workout_type == "Mobility":
                details = f"Mobility: Stretch: {row[8]}, Duration {row[9]} mins"
            else:
                details = None

            if (day, details) not in to_remove:
                new_lines.append(row)

    with open("data/workout_data.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(new_lines)
