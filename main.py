import sys
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from pyqtgraph import *
import matplotlib
from calculations import get_results
from math import *

matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import matplotlib.pyplot as plt


def to_radian(angle):
    return angle / 180.0 * 3.141593


class MainWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)

        # Drop-down menus
        self.trans_config_menu = QComboBox()
        self.polarity_menu = QComboBox()
        self.load_config_menu = QComboBox()

        # Graph
        self.graphWidget = plt.figure()
        self.canvas = FigureCanvasQTAgg(self.graphWidget)
        self.ax = None

        # Input side objects
        self.input_label = None
        self.cal_button = QPushButton("Calculate", self)

        # Input edit text
        self.vMag_input = QLineEdit()
        self.vAng_input = QLineEdit()
        self.impMag_input = QLineEdit()
        self.impAng_input = QLineEdit()
        self.turnsRatioNum_input = QLineEdit()
        self.turnsRatioDen_input = QLineEdit()
        self.kva_input = QLineEdit()
        self.ro2_input = QLineEdit()
        self.xo2_input = QLineEdit()

        # Input Labels
        self.v_label = QLabel("V Line")
        self.imp_label = QLabel("Impedance")
        self.turnsRatio_label = QLabel("Turns Ratio")
        self.kva_label = QLabel("KVA Rating")
        self.ro2_label = QLabel("Ro2")
        self.xo2_label = QLabel("Xo2")

        # Circuit Diagram
        self.circuit_dgm = QLabel()

        # Output Params
        self.vol_reg_out = QLabel("Nil")
        self.primMag_out = QLabel("Nil")
        self.primAngle_out = QLabel("Nil")
        self.secMag_out = QLabel("Nil")
        self.secAngle_out = QLabel("Nil")

        # Main window Init
        self.setWindowTitle("Test")
        geometry = self.screen().availableGeometry()
        self.setGeometry(100, 100, geometry.width() * 0.9, geometry.height() * 0.9)
        self.init_ui()
        self.showMaximized()

    def init_ui(self):

        # Drop-down Menus
        menu_ar = [self.trans_config_menu, self.polarity_menu, self.load_config_menu]
        menu_str = [['Transformer config', 'DD', 'DY', 'YY', 'YD'], [], ['Load Config', 'D', 'Y']]

        menu_layout = QHBoxLayout()

        for i, menu in enumerate(menu_ar):

            for item in menu_str[i]:
                menu.addItem(item)

            menu.setPlaceholderText("Select Polarity")
            menu.setStyleSheet("QComboBox {border: 1px solid black;"
                               "border-radius: 7px;"
                               "padding: 8px;"
                               "font: 18px Ariral;"
                               "margin: 10px;}"
                               "QComboBox::drop-down {border: 0px;"
                               "margin-right: 20px;"
                               "padding: 10px;}"
                               "QComboBox::down-arrow {image: url(./icons/ic_arrow_drop_down_black_24dp.png);"
                               "height: 36px;"
                               "width: 36px;"
                               "padding: 10px;}"
                               "QComboBox QAbstractItemView {border: 1px solid black;"
                               "border-radius: 7px;"
                               "padding: 4px;"
                               "background: white;}")

            menu_layout.addWidget(menu)

        self.trans_config_menu.currentIndexChanged.connect(self.trans_config_chng)

        circuit_layout = QVBoxLayout()
        circuit_layout.addLayout(menu_layout)

        # Circuit Image
        pixmp = QPixmap('img/Select.png')
        pixmp = pixmp.scaled(600, 300, aspectMode=QtCore.Qt.KeepAspectRatio, mode=QtCore.Qt.FastTransformation)
        self.circuit_dgm.setPixmap(pixmp)
        self.circuit_dgm.setFixedSize(600, 300)
        self.circuit_dgm.setStyleSheet("QLabel {border: 1px solid grey;"
                                       "border-radius: 7px;"
                                       "padding: 8px;"
                                       "background-color: white;"
                                       "margin: 10px;"
                                       "height: 300;"
                                       "width: 500;}")

        circuit_layout.addWidget(self.circuit_dgm, alignment=QtCore.Qt.AlignCenter)

        # Input Params
        input_ar = [self.vMag_input, self.vAng_input, self.impMag_input, self.impAng_input, self.turnsRatioNum_input,
                    self.turnsRatioDen_input, self.kva_input, self.ro2_input, self.xo2_input]
        label_ar = [self.v_label, self.imp_label, self.turnsRatio_label, self.kva_label, self.ro2_label, self.xo2_label]
        hint_ar = ['Mag', 'Angle', 'Mag', 'Angle', 'num', 'den', 'kva', 'Ro2', 'Xo2']

        input_layout1 = QHBoxLayout()
        input_layout2 = QHBoxLayout()

        for label in label_ar:
            label.setStyleSheet("QLabel {font: 18px Ariral;}")

        for ind, input_txt in enumerate(input_ar):
            input_txt.setStyleSheet("QLineEdit {padding: 4px; border: 1px solid black;"
                                    "border-radius :7px;"
                                    "height: 40px;"
                                    "width: 90px;"
                                    "font: 18px Ariral;}")

            input_txt.setAlignment(QtCore.Qt.AlignCenter)
            input_txt.setPlaceholderText(hint_ar[ind])

        # V Line
        v_layout = QVBoxLayout()
        v_input_layout = QHBoxLayout()
        v_slash_label = QLabel('|')
        v_slash_label.setStyleSheet("QLabel {font: 20px Ariral;}")
        v_input_layout.addWidget(self.vMag_input, alignment=QtCore.Qt.AlignCenter)
        v_input_layout.addWidget(v_slash_label, alignment=QtCore.Qt.AlignCenter)
        v_input_layout.addWidget(self.vAng_input, alignment=QtCore.Qt.AlignCenter)
        v_layout.addWidget(self.v_label, alignment=QtCore.Qt.AlignCenter)
        v_layout.addLayout(v_input_layout)
        v_layout.setContentsMargins(10, 10, 10, 10)
        input_layout1.addLayout(v_layout)

        # kva rating
        kva_layout = QVBoxLayout()
        kva_layout.addWidget(self.kva_label, alignment=QtCore.Qt.AlignCenter)
        kva_layout.addWidget(self.kva_input, alignment=QtCore.Qt.AlignCenter)
        kva_layout.setContentsMargins(10, 10, 10, 10)
        input_layout1.addLayout(kva_layout)

        # Impedance
        imp_layout = QVBoxLayout()
        imp_input_layout = QHBoxLayout()
        imp_slash_label = QLabel('|')
        imp_slash_label.setStyleSheet("QLabel {font: 20px Ariral;}")
        imp_input_layout.addWidget(self.impMag_input, alignment=QtCore.Qt.AlignCenter)
        imp_input_layout.addWidget(imp_slash_label, alignment=QtCore.Qt.AlignCenter)
        imp_input_layout.addWidget(self.impAng_input, alignment=QtCore.Qt.AlignCenter)
        imp_layout.addWidget(self.imp_label, alignment=QtCore.Qt.AlignCenter)
        imp_layout.addLayout(imp_input_layout)
        imp_layout.setContentsMargins(10, 10, 10, 10)
        input_layout1.addLayout(imp_layout)

        # Ro2 rating
        ro2_layout = QVBoxLayout()
        ro2_layout.addWidget(self.ro2_label, alignment=QtCore.Qt.AlignCenter)
        ro2_layout.addWidget(self.ro2_input, alignment=QtCore.Qt.AlignCenter)
        ro2_layout.setContentsMargins(10, 10, 10, 10)
        input_layout2.addLayout(ro2_layout)

        # Turns Ratio
        turns_ratio_layout = QVBoxLayout()
        turns_ratio_input_layout = QHBoxLayout()
        turns_ratio_slash_label = QLabel('/')
        turns_ratio_slash_label.setStyleSheet("QLabel {font: 20px Ariral;}")
        turns_ratio_input_layout.addWidget(self.turnsRatioNum_input, alignment=QtCore.Qt.AlignCenter)
        turns_ratio_input_layout.addWidget(turns_ratio_slash_label, alignment=QtCore.Qt.AlignCenter)
        turns_ratio_input_layout.addWidget(self.turnsRatioDen_input, alignment=QtCore.Qt.AlignCenter)
        turns_ratio_layout.addWidget(self.turnsRatio_label, alignment=QtCore.Qt.AlignCenter)
        turns_ratio_layout.addLayout(turns_ratio_input_layout)
        turns_ratio_layout.setContentsMargins(10, 10, 10, 10)
        input_layout2.addLayout(turns_ratio_layout)

        # xo2 rating
        xo2_layout = QVBoxLayout()
        xo2_layout.addWidget(self.xo2_label, alignment=QtCore.Qt.AlignCenter)
        xo2_layout.addWidget(self.xo2_input, alignment=QtCore.Qt.AlignCenter)
        xo2_layout.setContentsMargins(10, 10, 10, 10)
        input_layout2.addLayout(xo2_layout)

        # Calculate Button
        self.cal_button.setStyleSheet("QPushButton {border: 1px solid grey;"
                                      "border-radius: 7px;"
                                      "background-color: white;"
                                      "height: 60px;"
                                      "width: 150px;"
                                      "font: 18px Ariral;"
                                      "margin: 10px;}"
                                      "QPushButton::pressed {border: 2px solid grey;}")
        self.cal_button.animateClick()
        self.cal_button.clicked.connect(self.calculate)

        bottom_layout = QVBoxLayout()
        bottom_layout.addLayout(input_layout1)
        bottom_layout.addLayout(input_layout2)
        bottom_layout.addWidget(self.cal_button, alignment=QtCore.Qt.AlignCenter)

        input_grp = QGroupBox()
        input_grp.setLayout(bottom_layout)
        input_grp.setStyleSheet("QGroupBox {font: 20px Ariral;"
                                "background-color: #EEEEEE;"
                                "border: 1px solid grey;"
                                "border-radius: 7px;"
                                "margin: 4px;"
                                "padding: 8px;}")

        circuit_grp = QGroupBox()
        circuit_grp.setLayout(circuit_layout)
        circuit_grp.setStyleSheet("QGroupBox {font: 20px Ariral;"
                                  "background-color: #EEEEEE;"
                                  "border: 1px solid grey;"
                                  "border-radius: 7px;"
                                  "margin: 4px;"
                                  "padding-bottom: 8px;}")

        left_layout = QVBoxLayout()
        left_layout.addWidget(circuit_grp)
        left_layout.addWidget(input_grp)

        # Graph
        graph_layout = QHBoxLayout()
        self.ax = self.graphWidget.add_subplot(111, projection='polar')
        # ax.set_rticks([])
        # ax.plot([0, 45], [0, 35], 'ro-')
        graph_layout.addWidget(self.canvas)

        graph_grp = QGroupBox()
        graph_grp.setLayout(graph_layout)
        graph_grp.setStyleSheet("QGroupBox {font: 20px Ariral;"
                                "background-color: white;"
                                "border: 1px solid grey;"
                                "border-radius: 7px;"
                                "margin: 4px;"
                                "padding-bottom: 8px;}")

        # Output
        vol_reg_head = QLabel("Voltage Regulation")
        out_prim_head = QLabel("Primary Currents(Mag|Angle)")
        out_sec_head = QLabel("Secondary Currents(Mag|Angle)")

        out_prim_head.setStyleSheet("QLabel {font: 20px Ariral;"
                                    "margin: 5px;}")
        out_sec_head.setStyleSheet("QLabel {font: 20px Ariral;"
                                   "margin: 5px;}")
        vol_reg_head.setStyleSheet("QLabel {font: 20px Ariral;"
                                   "margin-bottom: 5px;"
                                   "margin-top: 11px}")

        out_prim_head.setAlignment(QtCore.Qt.AlignCenter)
        out_sec_head.setAlignment(QtCore.Qt.AlignCenter)
        vol_reg_head.setAlignment(QtCore.Qt.AlignCenter)

        out_text_ar = [self.vol_reg_out, self.primMag_out, self.primAngle_out, self.secMag_out, self.secAngle_out]
        for out_text in out_text_ar:
            out_text.setStyleSheet("QLabel {border: 1px solid grey;"
                                   "border-radius: 7px;"
                                   "font: 18px Ariral;"
                                   "background-color: #FFFFFF;"
                                   "padding: 8px;"
                                   "margin: 10px;}")

            out_text.setMinimumSize(150, 65)
            out_text.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
            out_text.setAlignment(QtCore.Qt.AlignCenter)

        out_prim_layout = QHBoxLayout()
        out_sec_layout = QHBoxLayout()

        for i in range(1, 3):
            out_prim_layout.addWidget(out_text_ar[i], alignment=QtCore.Qt.AlignCenter)

        for i in range(3, 5):
            out_sec_layout.addWidget(out_text_ar[i], alignment=QtCore.Qt.AlignCenter)

        output_layout = QVBoxLayout()
        output_layout.addWidget(vol_reg_head)
        output_layout.addWidget(self.vol_reg_out, alignment=QtCore.Qt.AlignCenter)
        output_layout.addWidget(out_prim_head, alignment=QtCore.Qt.AlignCenter)
        output_layout.addLayout(out_prim_layout)
        output_layout.addWidget(out_sec_head, alignment=QtCore.Qt.AlignCenter)
        output_layout.addLayout(out_sec_layout)

        output_grp = QGroupBox()
        output_grp.setLayout(output_layout)
        output_grp.setStyleSheet("QGroupBox {font: 20px Ariral;"
                                 "background-color: #EEEEEE;"
                                 "border: 1px solid grey;"
                                 "border-radius: 7px;"
                                 "margin: 4px;"
                                 "padding-bottom: 8px;}")

        right_layout = QVBoxLayout()
        right_layout.addWidget(graph_grp)
        right_layout.addWidget(output_grp)

        main_layout = QHBoxLayout()
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)
        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

    def trans_config_chng(self):
        self.polarity_menu.clear()
        self.polarity_menu.addItem('Select polarity')
        config = self.trans_config_menu.currentIndex()
        m1 = ['0', '6']
        m2 = ['1', '5', '7', '11']
        # ['Transformer config', 'DD', 'DY', 'YY', 'YD']
        if config == 1 or config == 3:
            for num in m1:
                self.polarity_menu.addItem(num)
        elif config != 0:
            for num in m2:
                self.polarity_menu.addItem(num)

        if config == 1:
            pixmp = QPixmap('img/DD.jpeg')
        elif config == 2:
            pixmp = QPixmap('img/DY.jpeg')
        elif config == 3:
            pixmp = QPixmap('img/YY.jpeg')
        elif config == 4:
            pixmp = QPixmap('img/YD.jpeg')
        else:
            pixmp = QPixmap('img/Select.png')

        pixmp = pixmp.scaled(550, 300, aspectMode=QtCore.Qt.KeepAspectRatio, mode=QtCore.Qt.FastTransformation)
        print(pixmp.size())
        self.circuit_dgm.setPixmap(pixmp)
        self.circuit_dgm.update()

    def calculate(self):

        try:
            trans_config_raw = self.trans_config_menu.currentText().lower()
            polarity = int(self.polarity_menu.currentText())
            load_config = self.load_config_menu.currentText().lower()
            trans_config = [trans_config_raw[0], trans_config_raw[1]]

            v_line_mag = float(self.vMag_input.text())
            v_line_angle = float(self.vAng_input.text())
            v_line = (v_line_mag, v_line_angle)

            turns_ratio_num = float(self.turnsRatioNum_input.text())
            turns_ratio_den = float(self.turnsRatioDen_input.text())
            turns_ratio = (turns_ratio_num, turns_ratio_den)

            imp_mag = float(self.impMag_input.text())
            imp_angle = float(self.impAng_input.text())
            imp = (imp_mag, imp_angle)

            ro2 = float(self.ro2_input.text())
            xo2 = float(self.xo2_input.text())

        except:
            self.vol_reg_out.setText("Invalid Inp")
            self.primMag_out.setText("Invalid Inp")
            self.primAngle_out.setText("Invalid Inp")
            self.secMag_out.setText("Invalid Inp")
            self.secAngle_out.setText("Invalid Inp")
            return False

        results = get_results(trans_config, polarity, load_config, v_line, turns_ratio, imp, ro2, xo2)
        v_reg = results[0]
        i_line_prim = results[1]
        i_line_sec = results[2]
        self.vol_reg_out.setText(str(v_reg*100))
        self.vol_reg_out.adjustSize()
        self.primMag_out.setText(str(i_line_prim[0]))
        self.primMag_out.adjustSize()
        self.primAngle_out.setText(str(i_line_prim[1])+'°')
        self.primAngle_out.adjustSize()
        self.secMag_out.setText(str(i_line_sec[0]))
        self.secMag_out.adjustSize()
        self.secAngle_out.setText(str(i_line_sec[1])+'°')
        self.secAngle_out.adjustSize()
        self.ax.cla()
        # self.ax.plot([0, 5], [0, 45], 'ro-')
        self.ax.plot([0, to_radian(i_line_prim[1])], [0, i_line_prim[0]], 'bo-', label="Prim I")
        self.ax.plot([0, to_radian(i_line_sec[1])], [0, i_line_sec[0]], 'ro-', label="Sec I")
        angle = to_radian(20)
        self.ax.legend(loc="lower left", bbox_to_anchor=(.7 + cos(angle) / 2, .7 + sin(angle) / 2))
        self.canvas.draw()
        return True


if __name__ == "__main__":
    app = QApplication()
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
