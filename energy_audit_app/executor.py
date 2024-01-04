import sys

from PyQt5.QtWidgets import QApplication
from .ui import EnergyAuditWindow


class EnergyAuditApp:
    TITLE = "Energy Audit"
    DEFAULT_SIZES = (100, 100, 1280, 720)

    def start(self) -> None:
        app = QApplication(sys.argv)
        main_window = EnergyAuditWindow(self.TITLE, self.DEFAULT_SIZES)
        main_window.show()
        sys.exit(app.exec_())
