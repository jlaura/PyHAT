#ifndef GUITEST_H
#define GUITEST_H

#include <QMainWindow>

namespace Ui {
class GuiTest;
}

class GuiTest : public QMainWindow
{
    Q_OBJECT

public:
    explicit GuiTest(QWidget *parent = 0);
    ~GuiTest();

private slots:
    void on_toolButton_4_clicked();

    void on_toolButton_3_clicked();

    void on_toolButton_clicked();

    void on_toolButton_2_clicked();

    void on_lineEdit_3_textChanged(const QString &arg1);

    void on_pushButton_clicked(bool checked);

    void on_pushButton_clicked();

private:
    Ui::GuiTest *ui;
};

#endif // GUITEST_H
