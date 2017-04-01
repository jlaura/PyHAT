def del_layout_(QLayout):
    to_delete = QLayout.takeAt(QLayout.count() - 1)  # remove the layout item at n-1 index
    if to_delete is not None:  # We run this method as long as there are objects
        while to_delete.count():  # while the count is not 0
            item = to_delete.takeAt(0)  # grab the layout item at 0th index
            widget = item.widget()  # get the widget at this location
            if widget is not None:  # if there is an object in this widget
                widget.deleteLater()  # delete this widget
            else:
                pass


def del_qwidget_(QWidget):
    QWidget.close()
    QWidget.deleteLater()