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

private:
    Ui::GuiTest *ui;
};

#endif // GUITEST_H
