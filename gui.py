from PyQt6.QtWidgets import (
    QWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QLabel,
    QComboBox,
    QLineEdit,
    QMessageBox,
    QTreeWidget,
    QTreeWidgetItem,
)
from PyQt6.QtCore import Qt
from logic import (
    toggle_visibility,
    save_workout,
    read_workouts,
    clear_workouts,
    remove_workouts,
)
import typing


class MainWindow(QWidget):
    """
    Main window for my Fitness App.
    Lets you navigate to the Plan Workout Window or the View Workout Window.
    """
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Fitness App")
        self.resize(600, 400)

        plan_button = QPushButton("Plan your workout")
        plan_button.clicked.connect(lambda: self.open_window(PlanWorkoutWindow))

        view_button = QPushButton("View planned workouts")
        view_button.clicked.connect(lambda: self.open_window(ViewWorkoutWindow))

        main_layout = QHBoxLayout()
        main_layout.addWidget(plan_button)
        main_layout.addWidget(view_button)

        self.setLayout(main_layout)

    def open_window(self, window) -> None:
        """
        Opens the window that is passed
        Args:
            window : The window being opened.
        """
        self.window = window()
        self.window.show()


class PlanWorkoutWindow(QWidget):
    """
    The window for planning your workout
    Lets users input workout details and save them.
    """
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Plan Workout")
        self.resize(600, 400)

        self.main_layout = QHBoxLayout()

        self.vertical_layout = QVBoxLayout()

        self.workout_form = QFormLayout()

        self.day_combo = QComboBox()
        self.day_combo.addItems(
            [
                "Sunday",
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
            ]
        )
        self.workout_form.addRow("Day:", self.day_combo)

        self.workout_type_combo = QComboBox()
        self.workout_type_combo.addItems(["Cardio", "Weight Training", "Mobility"])
        self.workout_type_combo.currentTextChanged.connect(self.workout_type_changed)
        self.workout_form.addRow("Workout Type:", self.workout_type_combo)

        self.cardio_intensity_label = QLabel("Intensity:")
        self.cardio_intensity = QComboBox()
        self.cardio_intensity.addItems(["Low", "Moderate", "High"])
        self.cardio_duration_label = QLabel("Duration (Mins):")
        self.cardio_duration = QLineEdit()

        self.weight_exercise_label = QLabel("Exercise:")
        self.weight_exercise = QComboBox()
        self.weight_exercise.addItems(
            [
                "Barbell Bench Press",
                "Deadlift",
                "Squat (Barbell or Dumbbell)",
                "Overhead Press (Barbell or Dumbbell)",
                "Bent-Over Barbell Row",
                "Dumbbell Chest Fly",
                "Dumbbell Lateral Raise",
                "Barbell Curl",
                "Tricep Pushdown",
                "Romanian Deadlift",
            ]
        )
        self.weight_weight_label = QLabel("Weight (lbs):")
        self.weight_weight = QLineEdit()
        self.weight_sets_label = QLabel("Sets:")
        self.weight_sets = QLineEdit()
        self.weight_reps_label = QLabel("Reps:")
        self.weight_reps = QLineEdit()

        self.mobility_stretch_label = QLabel("Stretch:")
        self.mobility_stretch = QComboBox()
        self.mobility_stretch.addItems(
            ["Hamstring Stretch", "Hip Flexor Stretch", "Shoulder Mobility"]
        )
        self.mobility_duration_label = QLabel("Duration (Mins):")
        self.mobility_duration = QLineEdit()

        self.workout_form.addRow(self.cardio_intensity_label, self.cardio_intensity)
        self.workout_form.addRow(self.cardio_duration_label, self.cardio_duration)
        self.workout_form.addRow(self.weight_exercise_label, self.weight_exercise)
        self.workout_form.addRow(self.weight_weight_label, self.weight_weight)
        self.workout_form.addRow(self.weight_reps_label, self.weight_reps)
        self.workout_form.addRow(self.weight_sets_label, self.weight_sets)
        self.workout_form.addRow(self.mobility_stretch_label, self.mobility_stretch)
        self.workout_form.addRow(self.mobility_duration_label, self.mobility_duration)

        self.widgets = {
            "Cardio": [
                self.cardio_intensity_label,
                self.cardio_intensity,
                self.cardio_duration_label,
                self.cardio_duration,
            ],
            "Weight Training": [
                self.weight_exercise_label,
                self.weight_exercise,
                self.weight_reps,
                self.weight_reps_label,
                self.weight_sets_label,
                self.weight_sets,
                self.weight_weight_label,
                self.weight_weight,
            ],
            "Mobility": [
                self.mobility_stretch,
                self.mobility_stretch_label,
                self.mobility_duration,
                self.mobility_duration_label,
            ],
        }
        toggle_visibility(self.widgets, "Cardio")

        self.add_workout_button = QPushButton("Add Workout")
        self.add_workout_button.clicked.connect(self.save_workout)
        self.vertical_layout.addLayout(self.workout_form)
        self.vertical_layout.addWidget(self.add_workout_button)

        self.main_layout.addStretch()
        self.main_layout.addLayout(self.vertical_layout)
        self.main_layout.addStretch()

        self.setLayout(self.main_layout)

    def workout_type_changed(self, workout_type: str) -> None:
        """
        Updates the visibility of the form entries
        Args:
            workout_type: The selected workout type
        """
        toggle_visibility(self.widgets, workout_type)

    def save_workout(self) -> None:
        """
        Validates and saves the workout data, showing success or error messages.
        """
        try:
            day = self.day_combo.currentText()
            workout_type = self.workout_type_combo.currentText()

            if workout_type == "Cardio":
                cardio_intensity = self.cardio_intensity.currentText()
                cardio_duration = self.cardio_duration.text()
                save_workout(
                    day,
                    workout_type,
                    cardio_intensity=cardio_intensity,
                    cardio_duration=cardio_duration,
                )
            elif workout_type == "Weight Training":
                weight_exercise = self.weight_exercise.currentText()
                weight = self.weight_weight.text()
                weight_sets = self.weight_sets.text()
                weight_reps = self.weight_reps.text()
                save_workout(
                    day,
                    workout_type,
                    weight_exercise=weight_exercise,
                    weight=weight,
                    weight_reps=weight_reps,
                    weight_sets=weight_sets,
                )
            elif workout_type == "Mobility":
                mobility_stretch = self.mobility_stretch.currentText()
                mobility_duration = self.mobility_duration.text()
                save_workout(
                    day,
                    workout_type,
                    mobility_stretch=mobility_stretch,
                    mobility_duration=mobility_duration,
                )

            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Success")
            msg_box.setText(
                "Workout saved successfully!\n\n\nWould you like to add another workout or exit to the main menu?"
            )
            exit_button = msg_box.addButton("Exit", QMessageBox.ButtonRole.RejectRole)
            add_another_button = msg_box.addButton(
                "Add Another", QMessageBox.ButtonRole.ActionRole
            )
            msg_box.setDefaultButton(add_another_button)

            msg_box.exec()

            if msg_box.clickedButton() == exit_button:
                self.close()
            else:
                self.clear_inputs()

        except ValueError as e:
            QMessageBox.warning(self, "Invalid Data", str(e))

    def clear_inputs(self) -> None:
        """
        Resets all input fields to the default state.
        """
        self.cardio_intensity.setCurrentIndex(0)
        self.cardio_duration.clear()
        self.weight_exercise.setCurrentIndex(0)
        self.weight_weight.clear()
        self.weight_sets.clear()
        self.weight_reps.clear()
        self.mobility_stretch.setCurrentIndex(0)
        self.mobility_duration.clear()


class ViewWorkoutWindow(QWidget):
    """
    Window for viewing and managing planned workouts.
    Allows users to view, remove selected workouts, or clear all workouts.
    """
    def __init__(self):
        super().__init__()

        self.setWindowTitle("View Workouts")
        self.resize(600, 400)

        self.main_layout = QHBoxLayout()
        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderLabels(["Day"])

        self.remove_checked_button = QPushButton("Finish Selected Workouts")
        self.remove_checked_button.clicked.connect(self.remove_checked_items)

        self.clear_button = QPushButton("Clear Workouts")
        self.clear_button.clicked.connect(self.confirm_clear_workouts)

        layout = QVBoxLayout()
        layout.addWidget(self.tree_widget)
        layout.addWidget(self.remove_checked_button)
        layout.addWidget(self.clear_button)
        self.setLayout(layout)

        self.fill_workouts()
        self.tree_widget.expandAll()
        self.tree_widget.resizeColumnToContents(0)
        self.tree_widget.resizeColumnToContents(1)

    def fill_workouts(self) -> None:
        """
        Fills the tree widget with the list of workouts grouped by day
        """
        try:
            workouts = read_workouts()

            for day, details in workouts.items():
                day_item = QTreeWidgetItem([day])
                self.tree_widget.addTopLevelItem(day_item)

                for workout in details:
                    workout_item = QTreeWidgetItem([workout])
                    workout_item.setFlags(
                        workout_item.flags() | Qt.ItemFlag.ItemIsUserCheckable
                    )
                    workout_item.setCheckState(0, Qt.CheckState.Unchecked)
                    day_item.addChild(workout_item)

        except FileNotFoundError:
            no_workouts_item = QTreeWidgetItem(["No workouts found"])
            self.tree_widget.addTopLevelItem(no_workouts_item)

    def confirm_clear_workouts(self) -> None:
        """
        Shows a confirmation box before clearing all the workouts
        """
        reply = QMessageBox.question(
            self,
            "Clear Workouts",
            "Are you sure you want to clear all workouts? This cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.clear_workouts()

    def clear_workouts(self):
        """
        Clears all workouts from the CSV and the tree widget, then refreshes the tree.
        """
        clear_workouts()
        self.tree_widget.clear()

    def remove_checked_items(self):
        """
        Removes selected workouts from the tree widget and updates the tree.
        """
        entries = []

        for i in range(self.tree_widget.topLevelItemCount()):
            day_item = self.tree_widget.topLevelItem(i)
            for j in range(day_item.childCount()):
                workout_item = day_item.child(j)
                if workout_item.checkState(0) == Qt.CheckState.Checked:
                    entry_str = workout_item.text(0)
                    day_str = day_item.text(0)
                    entries.append((day_str,entry_str))
        remove_workouts(entries)

        self.tree_widget.clear()
        self.fill_workouts()
        self.tree_widget.expandAll()
