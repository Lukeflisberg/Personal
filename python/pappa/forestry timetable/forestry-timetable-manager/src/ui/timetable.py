from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFrame, QPushButton, QLabel, QGridLayout, QMessageBox, QFileDialog, QMenu, QAction,
    QLineEdit, QComboBox, QDockWidget, QFormLayout
)
from PyQt5.QtCore import Qt, QPoint, QMimeData
from PyQt5.QtGui import QDrag
from models.block import Block
import utils.csv_handler as csv_handler

class BlockEditor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(300)
        self.layout = QVBoxLayout(self)
        self.form = QFormLayout()
        self.header_input = QLineEdit()
        self.desc_input = QLineEdit()
        self.group_input = QComboBox()
        self.time_input = QComboBox()
        self.duration_input = QLineEdit()
        self.before_input = QLineEdit()
        self.after_input = QLineEdit()
        self.form.addRow("Header", self.header_input)
        self.form.addRow("Description", self.desc_input)
        self.form.addRow("Group", self.group_input)
        self.form.addRow("Start Time", self.time_input)
        self.form.addRow("Duration", self.duration_input)
        self.form.addRow("Before T", self.before_input)
        self.form.addRow("After T", self.after_input)
        self.layout.addLayout(self.form)
        self.action_btn = QPushButton()
        self.layout.addWidget(self.action_btn)
        self.current_block = None
        self.mode = "add"
        self.action_btn.clicked.connect(self.on_action)

    def set_groups_times(self, groups, times):
        self.group_input.clear()
        self.group_input.addItems(groups)
        self.time_input.clear()
        self.time_input.addItems(times)

    def edit_block(self, block):
        self.current_block = block
        self.mode = "edit"
        self.header_input.setText(block.header)
        self.desc_input.setText(block.description)
        self.group_input.setCurrentText(block.group)
        self.time_input.setCurrentText(block.start_time)
        self.duration_input.setText(str(block.duration))
        self.before_input.setText(block.before_t)
        self.after_input.setText(block.after_t)
        self.action_btn.setText("Update")

    def add_block(self):
        self.current_block = None
        self.mode = "add"
        self.header_input.clear()
        self.desc_input.clear()
        self.group_input.setCurrentIndex(0)
        self.time_input.setCurrentIndex(0)
        self.duration_input.clear()
        self.before_input.clear()
        self.after_input.clear()
        self.action_btn.setText("Add")

    def on_action(self):
        if self.mode == "edit":
            self.parent().update_block_from_editor()
        else:
            self.parent().add_block_from_editor()

class DraggableBlock(QFrame):
    def __init__(self, block, parent=None):
        super().__init__(parent)
        self.block = block
        self.setFrameShape(QFrame.Box)
        self.setStyleSheet("background-color: #cce5ff; border: 1px solid #888;")
        layout = QVBoxLayout(self)
        header_label = QLabel(f"{block.header}")
        header_label.setAlignment(Qt.AlignCenter)
        desc_label = QLabel(f"{block.duration}\n{block.description}")
        desc_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(header_label)
        layout.addWidget(desc_label)
        self.setLayout(layout)
        self.setAcceptDrops(False)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            parent = self.parent()
            while parent and not hasattr(parent, "set_dragged_block"):
                parent = parent.parent()
            if parent:
                parent.set_dragged_block(self.block)
            drag = QDrag(self)
            mime_data = QMimeData()
            mime_data.setText(f"{self.block.group}|{self.block.start_time}")
            drag.setMimeData(mime_data)
            drag.exec_(Qt.MoveAction)
            if parent:
                parent.set_dragged_block(None)

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        edit_action = QAction("Edit", self)
        delete_action = QAction("Delete", self)
        menu.addAction(edit_action)
        menu.addAction(delete_action)

        # Connect actions
        edit_action.triggered.connect(self.edit_block)
        delete_action.triggered.connect(self.delete_block)
        menu.exec_(event.globalPos())

    def edit_block(self):
        parent = self.parent()
        while parent and not hasattr(parent, "show_editor_for_block"):
            parent = parent.parent()
        if parent:
            parent.show_editor_for_block(self.block)

    def delete_block(self):
        parent = self.parent()
        while parent and not hasattr(parent, "delete_block_by_ref"):
            parent = parent.parent()
        if parent:
            parent.delete_block_by_ref(self.block)

class DropLabel(QLabel):
    def __init__(self, group, time_period, parent=None):
        super().__init__("", parent)
        self.group = group
        self.time_period = time_period
        self.setStyleSheet("border: 1px solid #888;")
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        text = event.mimeData().text()
        src_group, src_time = text.split("|")
        self.parent().move_block(src_group, src_time, self.group, self.time_period)
        event.acceptProposedAction()

class TimetableUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Forestry Timetable Manager")
        self.layout = QVBoxLayout(self)

        self.blocks = csv_handler.load_csv('src/data/data.csv')

        self.highest_group = max(int(block.group[1:]) for block in self.blocks if block.group.startswith('G')) if self.blocks else 1
        self.groups = [f'G{i}' for i in range(1, self.highest_group+1)]
        self.time_periods = [f'T{i}' for i in range(1, 13)]

        self.dragged_block = None

        self.timetable_grid = QGridLayout()
        self.layout.addLayout(self.timetable_grid)

        self.button_layout = QHBoxLayout()
        self.layout.addLayout(self.button_layout)

        self.create_timetable()
        self.create_add_group_button()
        self.create_import_blocks_button()

        # Block editor dock
        self.editor_dock = QDockWidget("Block Editor", self)
        self.editor = BlockEditor(self)
        self.editor.set_groups_times(self.groups, self.time_periods)
        self.editor_dock.setWidget(self.editor)
        self.editor_dock.setFeatures(QDockWidget.DockWidgetClosable)
        self.editor_dock.setAllowedAreas(Qt.LeftDockWidgetArea)
        self.editor_dock.hide()
        self.layout.addWidget(self.editor)
        self.editor.hide()

        # Add "Add Block" button
        self.add_block_btn = QPushButton("Add Block")
        self.add_block_btn.clicked.connect(self.show_editor_for_add)
        self.button_layout.addWidget(self.add_block_btn)

    def show_editor_for_block(self, block):
        self.editor.set_groups_times(self.groups, self.time_periods)
        self.editor.edit_block(block)
        self.editor.show()

    def show_editor_for_add(self):
        self.editor.set_groups_times(self.groups, self.time_periods)
        self.editor.add_block()
        self.editor.show()

    def update_block_from_editor(self):
        block = self.editor.current_block
        group = self.editor.group_input.currentText()
        start_time = self.editor.time_input.currentText()
        duration = self.editor.duration_input.text()
        before_t = self.editor.before_input.text().strip() or None
        after_t = self.editor.after_input.text().strip() or None
        if not self.is_block_time_valid(group, start_time, duration, exclude_block=block, before_t=before_t, after_t=after_t):
            QMessageBox.warning(self, "Invalid Block", "The block cannot be updated due to time or constraint conflicts.")
            return
        block.header = self.editor.header_input.text()
        block.description = self.editor.desc_input.text()
        block.group = self.editor.group_input.currentText()
        block.start_time = self.editor.time_input.currentText()
        block.duration = int(self.editor.duration_input.text())
        block.before_t = self.editor.before_input.text()
        block.after_t = self.editor.after_input.text()
        self.editor.hide()
        self.create_timetable()

    def add_block_from_editor(self):
        group = self.editor.group_input.currentText()
        start_time = self.editor.time_input.currentText()
        duration = self.editor.duration_input.text()
        before_t = self.editor.before_input.text().strip() or None
        after_t = self.editor.after_input.text().strip() or None
        if not self.is_block_time_valid(group, start_time, duration, before_t=before_t, after_t=after_t):
            QMessageBox.warning(self, "Invalid Block", "The block cannot be added due to time or constraint conflicts.")
            return
        new_block = Block(
            start_time=self.editor.time_input.currentText(),
            group=self.editor.group_input.currentText(),
            duration=int(self.editor.duration_input.text()),
            header=self.editor.header_input.text(),
            description=self.editor.desc_input.text(),
            before_t=self.editor.before_input.text(),
            after_t=self.editor.after_input.text()
        )
        self.blocks.append(new_block)
        self.editor.hide()
        self.create_timetable()

    def create_timetable(self):
        # Clear previous widgets from the grid
        while self.timetable_grid.count():
            item = self.timetable_grid.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # Header row
        self.timetable_grid.addWidget(QLabel("Group/Time"), 0, 0)
        for j, time_period in enumerate(self.time_periods):
            header_label = QLabel(time_period)
            header_label.setStyleSheet("border: 1px solid #888; background: #f0f0f0;")
            header_label.setAlignment(Qt.AlignCenter)
            self.timetable_grid.addWidget(header_label, 0, j + 1)

        # Data rows
        for i, group in enumerate(self.groups):
            group_label = QLabel(group)
            group_label.setStyleSheet("border: 1px solid #888; background: #f0f0f0;")
            group_label.setAlignment(Qt.AlignCenter)
            self.timetable_grid.addWidget(group_label, i + 1, 0)

            j = 0
            while j < len(self.time_periods):
                time_period = self.time_periods[j]
                block = self.get_block_for_group_time(group, time_period)
                # Check if this cell is covered by the dragged block
                is_covered_by_dragged = False
                if self.dragged_block and group == self.dragged_block.group:
                    try:
                        drag_start = self.time_periods.index(self.dragged_block.start_time)
                        drag_duration = int(self.dragged_block.duration)
                        drag_end = drag_start + drag_duration - 1
                        if drag_start <= j <= drag_end:
                            is_covered_by_dragged = True
                    except Exception:
                        pass

                if block and not (self.dragged_block and block is self.dragged_block):
                    # Only skip if not the dragged block
                    try:
                        duration = int(block.duration)
                    except Exception:
                        duration = 1
                    block_widget = DraggableBlock(block, self)
                    self.timetable_grid.addWidget(block_widget, i + 1, j + 1, 1, duration)
                    j += duration
                else:
                    drop_label = DropLabel(group, time_period, self)
                    # Highlight invalid drop targets if dragging
                    if self.dragged_block:
                        before_t = self.dragged_block.before_t.strip() if self.dragged_block.before_t else None
                        after_t = self.dragged_block.after_t.strip() if self.dragged_block.after_t else None
                        valid = self.is_block_time_valid(
                            group, time_period, self.dragged_block.duration,
                            exclude_block=self.dragged_block,
                            before_t=before_t, after_t=after_t
                        )
                        if not valid:
                            drop_label.setStyleSheet("border: 1px solid #888; background-color: #ffcccc;")
                        else:
                            drop_label.setStyleSheet("border: 1px solid #888;")
                    self.timetable_grid.addWidget(drop_label, i + 1, j + 1)
                    j += 1

    def get_block_for_group_time(self, group, time_period):
        # Find a block that starts at this time and group
        for block in self.blocks:
            if block.group == group and block.start_time == time_period:
                return block
        return None

    def create_add_group_button(self):
        add_group_button = QPushButton("+")
        add_group_button.clicked.connect(self.add_group)
        self.button_layout.addWidget(add_group_button)

    def create_import_blocks_button(self):
        import_blocks_button = QPushButton("Import Blocks")
        import_blocks_button.clicked.connect(self.import_blocks)
        self.button_layout.addWidget(import_blocks_button)

    def add_group(self):
        new_group_number = len(self.groups) + 1
        new_group = f'G{new_group_number}'
        self.groups.append(new_group)
        self.create_timetable()
        QMessageBox.information(self, "Group Added", f"{new_group} has been added to the timetable.")

    def is_block_time_valid(self, group, start_time, duration, exclude_block=None, before_t=None, after_t=None):
        """ Check if a block can be added at the specified group and time period, with Before T and After T constraints. """
        try:
            start_idx = self.time_periods.index(start_time)
            duration = int(duration)
        except (ValueError, IndexError):
            return False

        end_idx = start_idx + duration - 1
        if end_idx >= len(self.time_periods):
            return False

        # Enforce After T constraint
        if after_t:
            try:
                after_idx = self.time_periods.index(after_t)
                if start_idx < after_idx:
                    return False
            except ValueError:
                return False

        # Enforce Before T constraint
        if before_t:
            try:
                before_idx = self.time_periods.index(before_t)
                if end_idx >= before_idx:
                    return False
            except ValueError:
                return False

        # Check for overlap with existing blocks
        for block in self.blocks:
            if block is exclude_block:
                continue
            if block.group != group:
                continue
            try:
                b_start = self.time_periods.index(block.start_time)
                b_duration = int(block.duration)
                b_end = b_start + b_duration - 1
            except (ValueError, IndexError):
                continue

            # Check for overlap
            if not (end_idx < b_start or start_idx > b_end):
                return False
        return True

    def import_blocks(self):
        imported_blocks = csv_handler.import_blocks_from_csv(self)
        if imported_blocks:
            local_highest_group = max(int(block.group[1:]) for block in imported_blocks if block.group.startswith('G'))
            for new_group in range(len(self.groups), local_highest_group + 1):
                self.groups.append(f'G{new_group}')

            self.blocks.extend(imported_blocks)
            self.create_timetable()
            QMessageBox.information(self, "Blocks Imported", f"{len(imported_blocks)} blocks have been imported successfully.")
        else:
            QMessageBox.warning(self, "No Blocks", "No blocks were imported.")

    def move_block(self, src_group, src_time, dest_group, dest_time):
        for block in self.blocks:
            if block.group == src_group and block.start_time == src_time:
                before_t = block.before_t.strip() if block.before_t else None
                after_t = block.after_t.strip() if block.after_t else None
                if not self.is_block_time_valid(dest_group, dest_time, block.duration, exclude_block=block, before_t=before_t, after_t=after_t):
                    QMessageBox.warning(self, "Invalid Move", "This block cannot be moved due to Before T/After T constraints.")
                    return
                block.group = dest_group
                block.start_time = dest_time
                break
        self.create_timetable()

    def delete_block_by_ref(self, block):
        self.blocks = [b for b in self.blocks if b is not block]
        self.create_timetable()

    def set_dragged_block(self, block):
        self.dragged_block = block
        self.create_timetable()