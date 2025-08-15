import sys
import pandas as pd
import csv
import os
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QTableWidget,
    QTableWidgetItem, QFormLayout, QLineEdit, QLabel, QColorDialog, QGraphicsView,
    QGraphicsScene, QGraphicsRectItem, QGraphicsSimpleTextItem, QHBoxLayout
)
from PyQt5.QtGui import QColor, QBrush, QPen
from PyQt5.QtCore import Qt, QRectF, QPointF, pyqtSignal

FILE_PATH = 'timetable.csv'
COLUMNS = [
    "Time Start", "Group", "Duration", "Header", "Description",
    "Color", "Before T", "After T", "Before Event", "After Event"
]
DEFAULT_TIME = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
CELL_WIDTH = 100
CELL_HEIGHT = 60

class DraggableBlock(QGraphicsRectItem):
    def __init__(self, data, table_ref):
        start, group, duration, header, desc, color, *_ = data
        self.header = header
        self.group = group
        self.duration = int(duration)
        self.start = int(start)
        self.color = QColor(color)
        self.table_ref = table_ref
        self.original_data = data

        rect = QRectF(self.start * CELL_WIDTH, int(self.group) * CELL_HEIGHT, self.duration * CELL_WIDTH, CELL_HEIGHT)
        super().__init__(rect)
        self.setBrush(QBrush(self.color))
        self.setPen(QPen(Qt.black))
        self.setFlags(QGraphicsRectItem.ItemIsMovable | QGraphicsRectItem.ItemSendsGeometryChanges)

        self.text = QGraphicsSimpleTextItem(header, self)
        self.text.setPos(self.rect().x() + 5, self.rect().y() + 5)

    def mouseReleaseEvent(self, event):
        # Snap to nearest grid
        pos = self.pos()
        snapped_x = round(pos.x() / CELL_WIDTH) * CELL_WIDTH
        snapped_y = round(pos.y() / CELL_HEIGHT) * CELL_HEIGHT
        self.setPos(snapped_x, snapped_y)

        # Update the table with new position
        new_start = snapped_x // CELL_WIDTH
        new_group = snapped_y // CELL_HEIGHT

        for row in range(self.table_ref.rowCount()):
            if self.table_ref.item(row, 3) and self.table_ref.item(row, 3).text() == self.header:
                self.table_ref.setItem(row, 0, QTableWidgetItem(str(new_start)))
                self.table_ref.setItem(row, 1, QTableWidgetItem(str(new_group)))
                break
        super().mouseReleaseEvent(event)

class ClickableLabel(QLabel):
    clicked = pyqtSignal()
    def mousePressEvent(self, event):
        self.clicked.emit()

class TimetableManager(QWidget):
    def __init__(self):
        """Initialize the timetable manager with a GUI."""
        super().__init__()
        self.setWindowTitle("Timetable Manager")
        self.resize(1200, 800)

        # Main horizontal layout
        main_layout = QHBoxLayout(self)
        self.setLayout(main_layout)

        # --- Left: Edit variables (form + buttons) ---
        left_panel = QVBoxLayout()
        self.form_layout = QFormLayout()
        self.start_input = QLineEdit()
        self.group_input = QLineEdit()
        self.duration_input = QLineEdit()
        self.header_input = QLineEdit()
        self.desc_input = QLineEdit()
        self.color_display = ClickableLabel()
        self.color_display.setFixedSize(60, 30)
        self.color_display.setStyleSheet("background-color: white; border: 1px solid black;")
        self.color = QColor("white")      
        self.before_t_input = QLineEdit()
        self.after_t_input = QLineEdit()
        self.before_event_input = QLineEdit()
        self.after_event_input = QLineEdit()
        self.color_display.clicked.connect(self.select_color)  
        self.form_layout.addRow("Time Start:", self.start_input)
        self.form_layout.addRow("Group:", self.group_input)
        self.form_layout.addRow("Duration:", self.duration_input)
        self.form_layout.addRow("Header:", self.header_input)
        self.form_layout.addRow("Description:", self.desc_input)
        self.form_layout.addRow("Color:", self.color_display)  
        self.form_layout.addRow("Before T:", self.before_t_input)
        self.form_layout.addRow("After T:", self.after_t_input)
        self.form_layout.addRow("Before Event:", self.before_event_input)
        self.form_layout.addRow("After Event:", self.after_event_input)
        left_panel.addLayout(self.form_layout)

        # Buttons
        self.import_btn = QPushButton("Import CSV")
        self.export_btn = QPushButton("Export CSV")
        self.add_btn = QPushButton("Add Block")
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.import_btn)
        btn_layout.addWidget(self.export_btn)
        btn_layout.addWidget(self.add_btn)
        left_panel.addLayout(btn_layout)

        main_layout.addLayout(left_panel, 0)  # 0 = smaller stretch

        # --- Center/Right: Timetable and scene ---
        center_panel = QVBoxLayout()
        self.table = QTableWidget(0, 10)
        self.table.setHorizontalHeaderLabels([
            "Time Start", "Group", "Duration", "Header", "Description",
            "Color", "Before T", "After T", "Before Event", "After Event"
        ])
        center_panel.addWidget(self.table)

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setMinimumHeight(300)
        center_panel.addWidget(self.view)

        # --- Bottom: Placeholder for future graphs ---
        self.graph_placeholder = QLabel("Graphs will appear here.")
        self.graph_placeholder.setMinimumHeight(120)
        self.graph_placeholder.setAlignment(Qt.AlignCenter)
        # Add the graph placeholder at the bottom of the center panel
        center_panel.addWidget(self.graph_placeholder)

        main_layout.addLayout(center_panel, 1)  # 1 = larger stretch

        # Connect buttons
        self.import_btn.clicked.connect(self.import_csv)
        self.export_btn.clicked.connect(self.export_csv)
        self.add_btn.clicked.connect(self.add_block)

        self.load_from_csv(FILE_PATH)

    def select_color(self):
        """Open a color dialog to select a color."""
        color = QColorDialog.getColor(self.color, self, "Select Color")
        if color.isValid():
            self.color = color
            self.color_display.setStyleSheet(
                f"background-color: {color.name()}; border: 1px solid black;"
            )
    
    def add_block(self):
        """Add a new block to the table and scene based on input fields."""
        data = [
            self.start_input.text(), self.group_input.text(), self.duration_input.text(),
            self.header_input.text(), self.desc_input.text(), self.color.name(),
            self.before_t_input.text(), self.after_t_input.text(),
            self.before_event_input.text(), self.after_event_input.text()
        ]
        self.add_row_to_table(data)
        self.add_block_to_scene(data)

        # Clear inputs
        for field in [
            self.start_input, self.group_input, self.duration_input,
            self.header_input, self.desc_input, self.before_t_input,
            self.after_t_input, self.before_event_input, self.after_event_input
        ]:
            field.clear()
    
    def load_from_csv(self, file_path=FILE_PATH):
        """Load CSV data into the table and scene."""
        if not os.path.exists(file_path):
            # Create an empty CSV file if it doesn't exist
            with open(file_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([
                    "Time Start", "Group", "Duration", "Header", "Description",
                    "Color", "Before T", "After T", "Before Event", "After Event"
                ])
            self.table.setRowCount(0)
            self.scene.clear()
            return
        
        self.table.setRowCount(0)
        self.scene.clear()

        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader, None)  # skip header

            for row in reader:
                self.add_row_to_table(row)
                self.add_block_to_scene(row)
                print(f"Loaded row: {row}")

    def import_csv(self):
        """Import CSV data from a file dialog."""
        file_name, _ = QFileDialog.getOpenFileName(self, "Import CSV", "", "CSV File (*.csv)")
        if not file_name:
            return
        
        self.table.setRowCount(0)
        self.scene.clear()

        with open(file_name, newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # skip header
            
            print("Importing Data:")
            for row in reader:
                self.add_row_to_table(row)
                self.add_block_to_scene(row)
                print(row)

    def save_csv(self, file_path=FILE_PATH):
        """Save current table data to a CSV file."""
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                "Time Start", "Group", "Duration", "Header", "Description",
                "Color", "Before T", "After T", "Before Event", "After Event"
            ])

        for row in range(self.table.rowCount()):
            row_data = [
                self.table.item(row, col).text() if self.table.item(row, col) else ""
                for col in range(self.table.columnCount())
            ]
            writer.writerow(row_data)

    def export_csv(self):
        """Export current table data to a CSV file."""
        file_name, _ = QFileDialog.getSaveFileName(self, "Export CSV", "", "CSV Files (*.csv)")
        if not file_name:
            return

        with open(file_name, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                "Time Period Start", "Group", "Duration", "Header", "Description",
                "Color", "Before T Period", "After T Period", "Before Event", "After Event"
            ])
            
            print("Exporting Data:")
            for row in range(self.table.rowCount()):
                row_data = [
                    self.table.item(row, col).text() if self.table.item(row, col) else ""
                    for col in range(self.table.columnCount())
                ]
                writer.writerow(row_data)
                print(row_data)

    def add_row_to_table(self, row):
        """Add a row of data to the table."""
        row_index = self.table.rowCount()
        self.table.insertRow(row_index)
        for col, value in enumerate(row):
            self.table.setItem(row_index, col, QTableWidgetItem(value))

    def add_block_to_scene(self, row):
        """Add a draggable block to the scene based on the row data."""
        try:
            block = DraggableBlock(row, self.table)
            self.scene.addItem(block)
        except Exception as e:
            print(f"Error adding block to scene: {e}")

    def closeEvent(self, event):
        """Handle the close event to save data before exiting."""
        self.save_csv(FILE_PATH)
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    manager = TimetableManager()
    manager.show()
    sys.exit(app.exec_())