import os
import sys
from typing import Tuple, List

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QScrollArea,
    QGridLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QHBoxLayout,
    QFileDialog,
)

from .image_to_docx_converter import DOCXConverter


def get_dist_path() -> str:
    data_path = os.path.join("energy_audit_app", "graphs_data")

    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, data_path)
    return os.path.join(data_path)


class EnergyAuditWindow(QMainWindow):
    GRAPHS_PATH = get_dist_path()
    AVERAGE_VALUES_GRAPHS_PATH = os.path.join(GRAPHS_PATH, "average_values")
    SPECIFIC_VALUES_GRAPHS_PATH = os.path.join(GRAPHS_PATH, "specific_values")
    ENERGY_BALANCE_GRAPHS_PATH = os.path.join(GRAPHS_PATH, "energy_balance")
    IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png")
    DOC_EXTENSIONS = (".docx", ".doc")
    NAMES_FILE = "names.txt"
    COMMENTS_FILE = "comments.txt"

    def __init__(self, title: str, sizes: Tuple[int, int, int, int]) -> None:
        super().__init__()
        self.setWindowTitle(title)
        self.setGeometry(*sizes)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        self.top_layout = QHBoxLayout()
        locality_label = QLabel("Енергетичний аудит міста **********")
        self.top_layout.addWidget(locality_label)

        self.average_values_button = QPushButton("Первинна інформація")
        self.average_values_button.clicked.connect(
            lambda: self.load_data_from_path(self.AVERAGE_VALUES_GRAPHS_PATH, 270)
        )
        self.top_layout.addWidget(self.average_values_button)

        self.specific_values_button = QPushButton("Питоме споживання")
        self.specific_values_button.clicked.connect(
            lambda: self.load_data_from_path(self.SPECIFIC_VALUES_GRAPHS_PATH, 270)
        )
        self.top_layout.addWidget(self.specific_values_button)

        self.energy_balance_button = QPushButton("Енергетичний баланс")
        self.energy_balance_button.clicked.connect(
            lambda: self.load_data_from_path(self.ENERGY_BALANCE_GRAPHS_PATH, 470)
        )
        self.top_layout.addWidget(self.energy_balance_button)

        self.report_button = QPushButton("Звіт")
        self.report_button.clicked.connect(self.get_docx)
        self.top_layout.addWidget(self.report_button)

        self.main_layout.addLayout(self.top_layout)

        self.scroll_area = QScrollArea(self.central_widget)
        self.scroll_area.setWidgetResizable(True)
        self.main_layout.addWidget(self.scroll_area)

        self.scroll_area_widget = QWidget()
        self.scroll_area.setWidget(self.scroll_area_widget)
        self.grid_layout = QGridLayout(self.scroll_area_widget)

        self.scroll_area.setWidget(self.scroll_area_widget)

        self.load_and_display_graphs(self.AVERAGE_VALUES_GRAPHS_PATH, 270)

    @staticmethod
    def clear_layout(layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def load_and_display_graphs(self, data_path, fixed_row_height):
        graph_names_file = os.path.join(data_path, self.NAMES_FILE)
        with open(graph_names_file, "r", encoding="utf-8") as file:
            graph_names = file.readlines()

        comments_file = os.path.join(data_path, self.COMMENTS_FILE)
        with open(comments_file, "r", encoding="utf-8") as file:
            comments = file.readlines()

        self.grid_layout.setColumnStretch(0, 1)
        self.grid_layout.setColumnStretch(1, 6)
        self.grid_layout.setColumnStretch(2, 3)

        for i, (graph_name, comment) in enumerate(zip(graph_names, comments), start=1):
            graph_name = graph_name.strip().replace("\\n", "\n")
            graph_name_label = QLabel(graph_name)
            graph_name_label.setWordWrap(True)
            graph_name_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
            graph_name_label.setFixedHeight(fixed_row_height)
            self.grid_layout.addWidget(graph_name_label, i, 0)

            image_path = os.path.join(data_path, f"{i}.png")
            image_label = QLabel()
            image_label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Fixed)
            image_label.setFixedHeight(fixed_row_height)
            image_label.setScaledContents(True)

            if os.path.exists(image_path):
                pixmap = QPixmap(image_path)
                image_label.setPixmap(pixmap)
                image_label.setProperty("imagePath", image_path)
            else:
                image_label.setText("Image not found")

            self.grid_layout.addWidget(image_label, i, 1)

            comment = comment.strip().replace("\\n", "\n")
            comment_label = QLabel(comment)
            comment_label.setWordWrap(True)
            comment_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
            comment_label.setFixedHeight(fixed_row_height)
            self.grid_layout.addWidget(comment_label, i, 2)

    def load_data_from_path(self, data_path, fixed_row_height):
        self.clear_layout(self.grid_layout)
        self.load_and_display_graphs(data_path, fixed_row_height)

    def get_docx(self) -> None:
        graph_categories = [
            (
                self.AVERAGE_VALUES_GRAPHS_PATH,
                "1. Середньодобові значення споживання електроенергії, газу та води",
            ),
            (
                self.SPECIFIC_VALUES_GRAPHS_PATH,
                "2. Середні за рік значення питомого споживання електроенергії, газу та води",
            ),
            (self.ENERGY_BALANCE_GRAPHS_PATH, "3. Енергетичний баланс і тарифи"),
        ]

        graph_data = []

        for category_path, category_title in graph_categories:
            category_graph_data = []
            graph_names_file = os.path.join(category_path, self.NAMES_FILE)
            comments_file = os.path.join(category_path, self.COMMENTS_FILE)

            with open(graph_names_file, "r", encoding="utf-8") as file:
                graph_names = file.readlines()

            with open(comments_file, "r", encoding="utf-8") as file:
                comments = file.readlines()

            for i, (graph_name, comment) in enumerate(
                    zip(graph_names, comments), start=1
            ):
                graph_name = graph_name.strip().replace("\\n", "\n")
                comment = comment.strip().replace("\\n", "\n")
                image_path = os.path.join(category_path, f"{i}.png")
                if not os.path.exists(image_path):
                    image_path = "Image not found"

                category_graph_data.append((image_path, graph_name, comment))

            graph_data.append((category_title, category_graph_data))
        self._convert_into_path(graph_data)

    def _convert_into_path(
            self, static_data: List[Tuple[str, List[Tuple[str, str, str]]]]
    ) -> None:
        image_to_docx_converter = DOCXConverter()
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save file",
            "",
            "Word files(*.docx *.doc)",
            options=options,
        )

        user_path, user_extension = os.path.splitext(file_path)
        if not user_extension or user_extension == ".":
            file_path = f"{user_path}{self.DOC_EXTENSIONS[0]}"

        if os.path.exists(os.path.dirname(file_path)):
            image_to_docx_converter.convert(file_path, static_data)
