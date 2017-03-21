# -*- coding: utf-8 -*-
"""
Created on Fri Oct 28 10:40:30 2016

@author: rbanderson
"""
from PyQt4 import QtGui


def make_combobox(choices):
    combo=QtGui.QComboBox()
    combo.setMaximumWidth(200)
    font = QtGui.QFont()
    font.setPointSize(10)
    combo.setFont(font)
    for i,choice in enumerate(choices):
        combo.addItem("")
        combo.setItemText(i,choice)
        
    return combo

    
def make_listwidget(choices):
    listwidget=QtGui.QListWidget()
    listwidget.setItemDelegate
    for item in choices:
        item = QtGui.QListWidgetItem(item)
        listwidget.addItem(item)
    return listwidget