#include "guitest.h"
#include "ui_guitest.h"

GuiTest::GuiTest(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::GuiTest)
{
    ui->setupUi(this);
}

GuiTest::~GuiTest()
{
    delete ui;
}
