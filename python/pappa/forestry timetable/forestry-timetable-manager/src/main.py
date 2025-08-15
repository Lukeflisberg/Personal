import sys
from PyQt5.QtWidgets import QApplication
from ui.timetable import TimetableUI
import utils.csv_handler as csv_handler

def main():
    app = QApplication(sys.argv)
    timetable_ui = TimetableUI()
    timetable_ui.showMaximized()

    def save_on_exit():
        csv_handler.save_to_csv('src/data/data.csv', timetable_ui.blocks)

    app.aboutToQuit.connect(save_on_exit)
    sys.exit(app.exec())

if __name__ == "__main__":
    main()