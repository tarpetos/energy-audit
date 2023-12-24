import os
import pandas as pd
import flet as ft

from typing import List, Optional, Callable

from .constants import GRAPHS_PATH, TABLES_PATH


class AppUI(ft.UserControl):
    INITIAL_DATA = "initial_data"
    PIE_CHART = "pie_chart"
    OPTION_DICT = {
        INITIAL_DATA: "Первинна інформація",
        "electric_energy": "Графік середньодобового споживання електроенергії",
        "heat_energy": "Графік середньодобового споживання теплової енергії",
        "electric_to_heat_usage": "Графік середнього питомого споживання "
        "електроенергії на виробництво теплової енергії",
        "gas_energy": "Графік середньодобового споживання газу",
        "gas_to_heat_usage": "Графік середнього питомого споживання "
        "газу на виробництво теплової енергії",
        "water_usage": "Графік середньодобового споживання води",
        "water_to_electric_usage": "Графік середнього питомого споживання "
        "води на виробництво електроенергії",
        "water_to_heat_usage": "Графік середнього питомого споживання "
        "води на виробництво теплової енергії",
        "energy_costs1": "Графік витрати (млн. доларів) на електроенергію, газ та воду",
        "energy_costs2": "Графік витрати (%) на електроенергію, газ та воду",
        "average_electric_costs": "Графік середньозваженого значення тарифів на електроенергію",
        "average_heat_costs": "Графік середньозваженого значення тарифів на теплову енергію",
        "average_gas_costs": "Графік середньозваженого значення тарифів на газ",
        "average_water_costs": "Графік середньозваженого значення тарифів на воду",
        "energy_sells1": "Обсяги продажів (млн доларів) електричної та теплової енергії",
        "energy_sells2": "Обсяги продажів (%) електричної та теплової енергії",
        PIE_CHART: "Зведений енергобаланс витрат на електроенергію, газ та воду (млн доларів)",
    }

    def __init__(self, page: ft.Page) -> None:
        super().__init__()

        self.graph_selector = ft.Dropdown(
            label="Селектор",
            hint_text="Виберіть опцію для відображення",
            options=self._load_dropdown_options(),
            autofocus=True,
            on_change=self._on_selector_change,
        )

        self.data_table = ft.DataTable()
        self.data_container = ft.Column(
            [self.data_table],
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        )

        self.graph_image = ft.Image(
            src=GRAPHS_PATH,
            error_content=ft.Text(""),
            fit=ft.ImageFit.FILL,
            border_radius=ft.border_radius.all(20),
        )

        self.graph_image_container = ft.Row(
            [self.graph_image],
            alignment=ft.MainAxisAlignment.CENTER,
        )

        self.graph_image_container = ft.Column(
            controls=[self.graph_image],
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        )

        self.pie_charts_view = ft.GridView(
            runs_count=3,
        )

        self.legend_table = ft.DataTable()

        self.legend_average_value = ft.Text()
        # self.average_value_container = ft.Row(
        #     controls=[self.legend_average_value],
        #     alignment=ft.MainAxisAlignment.CENTER,
        # )

        self.legend_container = ft.Column(
            [self.legend_table],
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        )

        self._is_ascending = True

    def _calculate_average(self, file_name: str) -> Optional[float]:
        csv_path = os.path.abspath(
            os.path.join(TABLES_PATH, "with_average", f"{file_name}.csv")
        )
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            self._load_default_tooltip(df)
            return df.iloc[-1, 1:].mean()
        self.graph_image.tooltip = None
        return None

    def _load_legend_table(self, file_name: str) -> None:
        csv_average_path = os.path.abspath(
            os.path.join(TABLES_PATH, "with_average", f"{file_name}.csv")
        )
        csv_default_path = os.path.abspath(
            os.path.join(TABLES_PATH, f"{file_name}.csv")
        )
        if os.path.exists(csv_average_path):
            df = pd.read_csv(csv_average_path, header=0)
        else:
            df = pd.read_csv(csv_default_path, header=0)

        df = df.round(4)
        self._build_table(self.legend_table, df)

    @staticmethod
    def _build_table(
        table: ft.DataTable,
        df: pd.DataFrame,
        on_sort: Optional[Callable] = None,
    ) -> None:
        table.border = ft.border.all(1, "black")
        table.vertical_lines = ft.border.BorderSide(1, "black")
        table.horizontal_lines = ft.border.BorderSide(1, "black")
        table.columns = [
            ft.DataColumn(ft.Text("" if col_name == "Unnamed: 0" else col_name), on_sort=on_sort)
            for col_name in df.columns
        ]
        table.rows = [
            ft.DataRow(cells=[ft.DataCell(ft.Text(value)) for value in row])
            for row in df.values
        ]

    def _sort_cols(self, event: ft.DataColumnSortEvent, df: pd.DataFrame) -> None:
        df_sorted = df.sort_values(
            by=df.columns[event.column_index], ascending=self._is_ascending
        )
        self._is_ascending = not self._is_ascending
        self.data_table.rows = [
            ft.DataRow(cells=[ft.DataCell(ft.Text(value)) for value in row])
            for row in df_sorted.values
        ]
        self.update()

    def _load_default_tooltip(self, df: pd.DataFrame) -> None:
        max_val = df.iloc[-1, 1:].max()
        min_val = df.iloc[-1, 1:].min()
        self.graph_image.tooltip = (
            f"Максимальне значення: {max_val:.4f}\n"
            f"Мінімальне значення: {min_val:.4f}\n"
            f"Нерівномірність: {max_val / min_val:.4f}"
        )

    def _on_selector_change(self, event: ft.ControlEvent) -> None:
        self.graph_image.src = GRAPHS_PATH
        self.legend_average_value.value = ""
        self.data_table.columns = self.legend_table.columns = self.data_table.border = self.legend_table.border = None
        self.pie_charts_view.controls = None

        if self.graph_selector.value == self.INITIAL_DATA:
            csv_path = os.path.abspath(
                os.path.join(TABLES_PATH, f"{self.INITIAL_DATA}.csv")
            )
            df = pd.read_csv(csv_path, header=0)
            self._build_table(
                self.data_table, df, on_sort=lambda e: self._sort_cols(e, df)
            )
        elif self.graph_selector.value == self.PIE_CHART:
            graph_list = os.listdir(GRAPHS_PATH)
            pie_charts_list = sorted(
                [graph for graph in graph_list if graph.startswith(self.PIE_CHART)]
            )
            for pie_chart in pie_charts_list:
                self.pie_charts_view.controls.append(
                    ft.Image(
                        src=os.path.join(GRAPHS_PATH, pie_chart),
                        fit=ft.ImageFit.FILL,
                        border_radius=ft.border_radius.all(20),
                    )
                )
            self._load_legend_table(f"{self.PIE_CHART}_values")
        else:

            self.graph_image.src = os.path.join(
                GRAPHS_PATH, f"{self.graph_selector.value}.png"
            )
            self.average_value = self._calculate_average(self.graph_selector.value)
            self.legend_average_value.value = (
                f"Середнє значення: {self.average_value:.3f}"
                if self.average_value
                else ""
            )
            self._load_legend_table(self.graph_selector.value)
        self.update()

    def _load_dropdown_options(self) -> List[ft.dropdown.Option]:
        return [ft.dropdown.Option(key=k, text=v) for k, v in self.OPTION_DICT.items()]

    def build(self) -> ft.Column:
        return ft.Column(
            [
                self.graph_selector,
                self.data_container,
                self.graph_image_container,
                self.pie_charts_view,
                self.legend_container,
            ]
        )
