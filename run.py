#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys
from random import randrange, randint

from PySide2.QtCore import QAbstractTableModel, QModelIndex, QRect, Qt
from PySide2.QtGui import QColor, QPainter
from PySide2.QtWidgets import (
    QApplication,
    QGridLayout,
    QHeaderView,
    QTableView,
    QWidget,
)
from PySide2.QtCharts import QtCharts


class CustomTableModel(QAbstractTableModel):
    def __init__(self):
        QAbstractTableModel.__init__(self)
        self.input_data = []
        self.mapping = {}
        self.column_count = 4
        self.row_count = randint(10, 21)

        for i in range(self.row_count):
            data_vec = [0] * self.column_count
            for k in range(len(data_vec)):
                if k % 2 == 0:
                    data_vec[k] = i * 50 + randrange(30)
                else:
                    data_vec[k] = randrange(100)
            self.input_data.append(data_vec)

    def rowCount(self, parent=QModelIndex()):
        return len(self.input_data)

    def columnCount(self, parent=QModelIndex()):
        return self.column_count

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            if section % 2 == 0:
                return "x"
            else:
                return "y"
        else:
            return "{}".format(section + 1)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return self.input_data[index.row()][index.column()]
        elif role == Qt.EditRole:
            return self.input_data[index.row()][index.column()]
        elif role == Qt.BackgroundRole:
            for color, rect in self.mapping.items():
                if rect.contains(index.column(), index.row()):
                    return QColor(color)
            # cell not mapped return white color
            return QColor(Qt.white)
        return None

    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid() and role == Qt.EditRole:
            self.input_data[index.row()][index.column()] = float(value)
            self.dataChanged.emit(index, index)
            return True
        return False

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsEditable | Qt.ItemIsSelectable

    def add_mapping(self, color, area):
        self.mapping[color] = area

    def clear_mapping(self):
        self.mapping = {}


class TableWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle('Графопостроитель')
        self.model = CustomTableModel()

        self.table_view = QTableView()
        self.table_view.setModel(self.model)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_view.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.chart = QtCharts.QChart()
        self.chart.setAnimationOptions(QtCharts.QChart.AllAnimations)

        self.series = QtCharts.QLineSeries()
        self.series.setName("Линия А")
        self.mapper = QtCharts.QVXYModelMapper(self)
        self.mapper.setXColumn(0)
        self.mapper.setYColumn(1)
        self.mapper.setSeries(self.series)
        self.mapper.setModel(self.model)
        self.chart.addSeries(self.series)

        seriesColorHex = "#000000"

        seriesColorHex = "{}".format(self.series.pen().color().name())
        self.model.add_mapping(seriesColorHex, QRect(0, 0, 2, self.model.rowCount()))

        # series 2
        self.series = QtCharts.QLineSeries()
        self.series.setName("Линия В")

        self.mapper = QtCharts.QVXYModelMapper(self)
        self.mapper.setXColumn(2)
        self.mapper.setYColumn(3)
        self.mapper.setSeries(self.series)
        self.mapper.setModel(self.model)
        self.chart.addSeries(self.series)

        seriesColorHex = "{}".format(self.series.pen().color().name())
        self.model.add_mapping(seriesColorHex, QRect(2, 0, 2, self.model.rowCount()))

        self.chart.createDefaultAxes()
        self.chart_view = QtCharts.QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        self.chart_view.setMinimumSize(640, 480)

        # Основной макет
        self.main_layout = QGridLayout()
        self.main_layout.addWidget(self.table_view, 1, 0)
        self.main_layout.addWidget(self.chart_view, 1, 1)
        self.main_layout.setColumnStretch(1, 1)
        self.main_layout.setColumnStretch(0, 0)
        self.setLayout(self.main_layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = TableWidget()
    w.show()
    sys.exit(app.exec_())
