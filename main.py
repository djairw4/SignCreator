# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import re
import shutil
import sqlite3
import sys
import os
from pathlib import Path


from PyQt5 import QtGui
from PyQt5.QtWidgets import (
    QApplication, QDialog, QMainWindow, QMessageBox, QFileDialog, QWidget
)

from SignCreator_ui import Ui_MainWindow

import pandas as pd

df = pd.read_excel(r'Proposed Dimensions.xlsx', sheet_name='All_proposed', engine='openpyxl')
print(df)

oneDriveFolder = "OneDrive - Personal"

class Window(QMainWindow, Ui_MainWindow):
    path = os.path.join(r'C:\Users', os.getlogin(), oneDriveFolder, r'Pictures\\')
    fileName = ''
    scale = 1

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connectSignalsSlots()
        self.shape = self.comboBox_shape.currentText()
        self.country = self.comboBox_country.currentText()
        self._class = self.comboBox_class.currentText()
        self.fileName = r'C:\Users\Z0171823\PycharmProjects\SignCreator\ui\resources\stop.png'
        self.name = self.lineEdit_name.text()
        self.project_path = os.getcwd()
        self.fileName = os.path.join(self.project_path, r'ui\resources\stop.png')
        self.getSignsDir()
        self.edit = False
        for cntry in os.listdir(self.signs_dir):
            try:
                os.mkdir(os.path.join(self.signs_dir, cntry, 'SignsPictures'))
            except OSError:
                pass

    def connectSignalsSlots(self):
        self.action_Image.triggered.connect(self.fileExplorer)
        self.action_Save.triggered.connect(self.save_sign)
        self.action_Open.triggered.connect(self.editFile)
        self.doubleSpinBox_XS_w.valueChanged['double'].connect(self.XS_h_scale)
        self.doubleSpinBox_XS_h.valueChanged['double'].connect(self.XS_w_scale)
        self.doubleSpinBox_S_w.valueChanged['double'].connect(self.S_h_scale)
        self.doubleSpinBox_S_h.valueChanged['double'].connect(self.S_w_scale)
        self.doubleSpinBox_M_w.valueChanged['double'].connect(self.M_h_scale)
        self.doubleSpinBox_M_h.valueChanged['double'].connect(self.M_w_scale)
        self.doubleSpinBox_L_w.valueChanged['double'].connect(self.L_h_scale)
        self.doubleSpinBox_L_h.valueChanged['double'].connect(self.L_w_scale)
        self.doubleSpinBox_XL_w.valueChanged['double'].connect(self.XL_h_scale)
        self.doubleSpinBox_XL_h.valueChanged['double'].connect(self.XL_w_scale)
        self.comboBox_shape.currentTextChanged.connect(self.shape_changed)
        self.comboBox_country.currentTextChanged.connect(self.country_changed)
        self.comboBox_class.currentTextChanged.connect(self.class_changed)
        self.checkBox.stateChanged.connect(self.checkBoxState_changed)
        self.lineEdit_name.textChanged.connect(self.name_changed)

    def fileExplorer(self):
        self.fileName, _ = QFileDialog.getOpenFileName(self, "Open Image File", self.path,
                                                       "Images (*.png *.jpg)")
        pathname, _ = os.path.splitext(self.fileName)
        self.name = os.path.basename(pathname)
        self.lineEdit_name.setText(self.name)
        self.path = str(Path(self.fileName).parent)
        print('self.filename = ', self.fileName, self.path)
        if self.fileName:
            pix = QtGui.QPixmap(self.fileName)
            self.edit = False
            self.label_image.setScaledContents(False)
            h = pix.height()
            w = pix.width()
            self.scale = h / w
            pix = pix.scaledToHeight(251) if h > w else pix.scaledToWidth(251)
            self.label_image.setPixmap(pix)
            self.lineEdit_pix_w.setText(str(w) + 'px')
            self.lineEdit_pix_h.setText(str(h) + 'px')
            if self.checkBox.isChecked():
                self.XS_h_scale()
                self.S_h_scale()
                self.M_h_scale()
                self.L_h_scale()
                self.XL_h_scale()

    def editFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Traffic Sign File",
                                                  os.path.join(self.signs_dir, self.country),
                                                  "Traffic Sign Files (*.trfsign)")
        if fileName:
            pathname, _ = os.path.splitext(fileName)
            self.name = os.path.basename(pathname)
            self.lineEdit_name.setText(self.name)
            path = str(Path(fileName).parent)
            self.country = os.path.basename(path)
            self.comboBox_country.setCurrentText(self.country)
            with open(fileName, "r") as f:
                text = f.read()
            print(text)
            self.parseParameters(text, path)

    def parseParameters(self, text, path):
        sizeXS_re = re.compile(r'(?<=Size\.XS\s=\s)\d\.\d+\s+\d\.\d+')
        sizeS_re = re.compile(r'(?<=Size\.S\s=\s)\d\.\d+\s+\d\.\d+|(?<=Size\.S\s\s=\s)\d\.\d+\s+\d\.\d+')
        sizeXL_re = re.compile(r'(?<=Size\.XL\s=\s)\d\.\d+\s+\d\.\d+')
        sizeL_re = re.compile(r'(?<=Size\.L\s=\s)\d\.\d+\s+\d\.\d+|(?<=Size\.L\s\s=\s)\d\.\d+\s+\d\.\d+')
        sizeM_re = re.compile(r'(?<=Size\.M\s=\s)\d\.\d+\s+\d\.\d+|(?<=Size\.M\s\s=\s)\d\.\d+\s+\d\.\d+')
        class_re = re.compile(r'(?<=Class\s=\s)\w+|(?<=Class=)\w+')
        shape_re = re.compile(r'(?<=Shape\s=\s)\w+|(?<=Shape=)\w+')
        texfile_re = re.compile(r'(?<=TexFile\s=\s)\w+/\w+\.\w+|(?<=TexFile\s=\s)\w+\.\w+')
        if self.checkBox.isChecked():
            self.checkBox.toggle()
        match = texfile_re.findall(text)
        print('texfile:', match)
        if match:
            match = match[0]
            print('texfile:', match)
            pic_path = os.path.join(path, match)
            self.fileName = match
            self.edit = True
            if os.path.isfile(pic_path):
                pix = QtGui.QPixmap(pic_path)
                self.label_image.setScaledContents(False)
                h = pix.height()
                w = pix.width()
                self.scale = h / w
                pix = pix.scaledToHeight(251) if h > w else pix.scaledToWidth(251)
                self.label_image.setPixmap(pix)
                self.lineEdit_pix_w.setText(str(w) + 'px')
                self.lineEdit_pix_h.setText(str(h) + 'px')
            else:
                self.label_image.clear()
                if self.doubleSpinBox_M_w.value():
                    self.scale = self.doubleSpinBox_M_h.value()/self.doubleSpinBox_M_w.value()
                else:
                    self.scale = 1
                self.lineEdit_pix_w.setText('? px')
                self.lineEdit_pix_h.setText('? px')
        match = class_re.findall(text)
        if match:
            match = match[0]
            print('class:', match)
            print(self.comboBox_class.findText(match))
            if self.comboBox_class.findText(match) == -1:
                self.comboBox_class.addItem(match)
                self.comboBox_class.setCurrentText(match)
            else:
                self.comboBox_class.setCurrentText(match)
            self._class = match
        match = shape_re.findall(text)
        if match:
            match = match[0]
            print('shape:', match)
            print(self.comboBox_shape.findText(match))
            if self.comboBox_shape.findText(match) == -1:
                self.comboBox_shape.addItem(match)
                self.comboBox_shape.setCurrentText(match)
            else:
                self.comboBox_shape.setCurrentText(match)
            self.shape = match
        match = sizeXS_re.findall(text)
        if match:
            match = match[0]
            w, h = match.split()
            self.doubleSpinBox_XS_w.setValue(float(w))
            self.doubleSpinBox_XS_h.setValue(float(h))
            print(match, '\n', w, '\n', h)
        else:
            self.doubleSpinBox_XS_w.setValue(0.0)
            self.doubleSpinBox_XS_h.setValue(0.0)
        match = sizeS_re.findall(text)
        if match:
            match = match[0]
            w, h = match.split()
            self.doubleSpinBox_S_w.setValue(float(w))
            self.doubleSpinBox_S_h.setValue(float(h))
            print(match, '\n', w, '\n', h)
        else:
            self.doubleSpinBox_S_w.setValue(0.0)
            self.doubleSpinBox_S_h.setValue(0.0)
        match = sizeM_re.findall(text)
        if match:
            match = match[0]
            w, h = match.split()
            self.doubleSpinBox_M_w.setValue(float(w))
            self.doubleSpinBox_M_h.setValue(float(h))
            print(match, '\n', w, '\n', h)
        else:
            self.doubleSpinBox_M_w.setValue(0.0)
            self.doubleSpinBox_M_h.setValue(0.0)
        match = sizeL_re.findall(text)
        if match:
            match = match[0]
            w, h = match.split()
            self.doubleSpinBox_L_w.setValue(float(w))
            self.doubleSpinBox_L_h.setValue(float(h))
            print(match, '\n', w, '\n', h)
        else:
            self.doubleSpinBox_L_w.setValue(0.0)
            self.doubleSpinBox_L_h.setValue(0.0)
        match = sizeXL_re.findall(text)
        if match:
            match = match[0]
            w, h = match.split()
            self.doubleSpinBox_XL_w.setValue(float(w))
            self.doubleSpinBox_XL_h.setValue(float(h))
            print(match, '\n', w, '\n', h)
        else:
            self.doubleSpinBox_XL_w.setValue(0.0)
            self.doubleSpinBox_XL_h.setValue(0.0)

    def XS_h_scale(self):
        if self.checkBox.isChecked():
            val = self.doubleSpinBox_XS_w.value()
            res = self.scale * val
            self.doubleSpinBox_XS_h.setValue(res)

    def XS_w_scale(self):
        if self.checkBox.isChecked():
            val = self.doubleSpinBox_XS_h.value()
            res = val / self.scale
            self.doubleSpinBox_XS_w.setValue(res)

    def S_h_scale(self):
        if self.checkBox.isChecked():
            val = self.doubleSpinBox_S_w.value()
            res = self.scale * val
            self.doubleSpinBox_S_h.setValue(res)

    def S_w_scale(self):
        if self.checkBox.isChecked():
            val = self.doubleSpinBox_S_h.value()
            res = val / self.scale
            self.doubleSpinBox_S_w.setValue(res)

    def M_h_scale(self):
        if self.checkBox.isChecked():
            val = self.doubleSpinBox_M_w.value()
            res = self.scale * val
            self.doubleSpinBox_M_h.setValue(res)

    def M_w_scale(self):
        if self.checkBox.isChecked():
            val = self.doubleSpinBox_M_h.value()
            res = val / self.scale
            self.doubleSpinBox_M_w.setValue(res)

    def L_h_scale(self):
        if self.checkBox.isChecked():
            val = self.doubleSpinBox_L_w.value()
            res = self.scale * val
            self.doubleSpinBox_L_h.setValue(res)

    def L_w_scale(self):
        if self.checkBox.isChecked():
            val = self.doubleSpinBox_L_h.value()
            res = val / self.scale
            self.doubleSpinBox_L_w.setValue(res)

    def XL_h_scale(self):
        if self.checkBox.isChecked():
            val = self.doubleSpinBox_XL_w.value()
            res = self.scale * val
            self.doubleSpinBox_XL_h.setValue(res)

    def XL_w_scale(self):
        if self.checkBox.isChecked():
            val = self.doubleSpinBox_XL_h.value()
            res = val / self.scale
            self.doubleSpinBox_XL_w.setValue(res)

    def propose_dimensions(self, result):
        if self.shape == 'Rectangular':
            if self._class == 'Supplement' and self.country == 'DEU':
                self.doubleSpinBox_XS_w.setValue(result.query('Size == "Size.XS" and Class == "Supplement"')['Width'])
                self.doubleSpinBox_S_w.setValue(result.query('Size == "Size.S" and Class == "Supplement"')['Width'])
                self.doubleSpinBox_M_w.setValue(result.query('Size == "Size.M" and Class == "Supplement"')['Width'])
                self.doubleSpinBox_L_w.setValue(result.query('Size == "Size.L" and Class == "Supplement"')['Width'])
                self.doubleSpinBox_XL_w.setValue(result.query('Size == "Size.XL" and Class == "Supplement"')['Width'])
            else:
                self.doubleSpinBox_XS_w.setValue(result.query('Size == "Size.XS" and Class != "Supplement"')['Width'])
                self.doubleSpinBox_S_w.setValue(result.query('Size == "Size.S" and Class != "Supplement"')['Width'])
                self.doubleSpinBox_M_w.setValue(result.query('Size == "Size.M" and Class != "Supplement"')['Width'])
                self.doubleSpinBox_L_w.setValue(result.query('Size == "Size.L" and Class != "Supplement"')['Width'])
                self.doubleSpinBox_XL_w.setValue(result.query('Size == "Size.XL" and Class != "Supplement"')['Width'])
        else:
            self.doubleSpinBox_XS_w.setValue(result.query('Size == "Size.XS"')['Width'])
            self.doubleSpinBox_S_w.setValue(result.query('Size == "Size.S"')['Width'])
            self.doubleSpinBox_M_w.setValue(result.query('Size == "Size.M"')['Width'])
            self.doubleSpinBox_L_w.setValue(result.query('Size == "Size.L"')['Width'])
            self.doubleSpinBox_XL_w.setValue(result.query('Size == "Size.XL"')['Width'])
        if not self.checkBox.isChecked() and self.shape != 'Rectangular':
            self.doubleSpinBox_XS_h.setValue(result.query('Size == "Size.XS"')['Height'])
            self.doubleSpinBox_S_h.setValue(result.query('Size == "Size.S"')['Height'])
            self.doubleSpinBox_M_h.setValue(result.query('Size == "Size.M"')['Height'])
            self.doubleSpinBox_L_h.setValue(result.query('Size == "Size.L"')['Height'])
            self.doubleSpinBox_XL_h.setValue(result.query('Size == "Size.XL"')['Height'])

    def shape_changed(self):
        self.shape = self.comboBox_shape.currentText()
        result = df.query(f'Shape == "{self.shape}" and Country == "{self.country}"')
        if not result.empty:
            print(result)
            self.propose_dimensions(result)

    def country_changed(self):
        self.country = self.comboBox_country.currentText()
        result = df.query(f'Shape == "{self.shape}" and Country == "{self.country}"')
        if not result.empty:
            print(result)
            self.propose_dimensions(result)

    def class_changed(self):
        self._class = self.comboBox_class.currentText()
        result = df.query(f'Shape == "{self.shape}" and Country == "{self.country}"')
        if not result.empty:
            print(result)
            self.propose_dimensions(result)

    def checkBoxState_changed(self):
        if not self.checkBox.isChecked():
            result = df.query(f'Shape == "{self.shape}" and Country == "{self.country}"')
            if not result.empty:
                print(result)
                self.propose_dimensions(result)
        else:
            self.XS_h_scale()
            self.S_h_scale()
            self.M_h_scale()
            self.L_h_scale()
            self.XL_h_scale()

    def name_changed(self):
        self.name = self.lineEdit_name.text()

    def save_sign(self):
        with open(os.path.join(self.project_path, 'Template.txt'), "r") as f:
            text = f.read()
        # print(text)
        print('signs path:', self.signs_dir)
        fileName, _ = QFileDialog.getSaveFileName(self, "Save Traffic Sign",
                                                  os.path.join(self.signs_dir, self.country, str(self.name)),
                                                  "Traffic Sign Files (*.trfsign)")
        if fileName:
            pathname, _ = os.path.splitext(fileName)
            self.name = os.path.basename(pathname)
            ext = os.path.splitext(self.fileName)[1]
            text = text.replace("_NAME_", self.name)
            text = text.replace("_CLASS_", self._class)
            text = text.replace("_SHAPE_", self.shape)
            text = text.replace("_XS_W_", str(self.doubleSpinBox_XS_w.value()))
            text = text.replace("_XS_H_", str(self.doubleSpinBox_XS_h.value()))
            text = text.replace("_S_W_", str(self.doubleSpinBox_S_w.value()))
            text = text.replace("_S_H_", str(self.doubleSpinBox_S_h.value()))
            text = text.replace("_M_W_", str(self.doubleSpinBox_M_w.value()))
            text = text.replace("_M_H_", str(self.doubleSpinBox_M_h.value()))
            text = text.replace("_L_W_", str(self.doubleSpinBox_L_w.value()))
            text = text.replace("_L_H_", str(self.doubleSpinBox_L_h.value()))
            text = text.replace("_XL_W_", str(self.doubleSpinBox_XL_w.value()))
            text = text.replace("_XL_H_", str(self.doubleSpinBox_XL_h.value()))
            if not self.edit:
                text = text.replace("_FILENAME_", 'SignsPictures/' + self.name + ext)
                pic_path = os.path.join(str(Path(fileName).parent), 'SignsPictures', self.name + ext)
                print(pic_path)
                shutil.copy2(self.fileName, pic_path)
            else:
                text = text.replace("_FILENAME_", self.fileName)
            print(text)
            with open(fileName, "w") as sign_file:
                sign_file.write(text)



    def getSignsDir(self):
        os.chdir('C:\IPG\carmaker')
        CM_last_version = os.listdir()[-1]
        self.signs_dir = os.path.join(os.getcwd(), CM_last_version, 'TrafficSigns')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())
