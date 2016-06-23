#include "guitest.h"
#include "ui_guitest.h"
#include <QString>
#include <QFile>
#include <QDir>
#include <QMessageBox>
#include <QFileDialog>

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

void GuiTest::on_toolButton_clicked()
{
    const QString &file_name = QFileDialog::getOpenFileName(this, "Open New File", QDir::homePath());
    ui->lineEdit->setText(file_name);
}

void GuiTest::on_toolButton_2_clicked()
{
    const QString &file_name = QFileDialog::getOpenFileName(this, "Open New File", QDir::homePath());
    ui->lineEdit_2->setText(file_name);
}

void GuiTest::on_toolButton_3_clicked()
{
    const QString &file_name = QFileDialog::getOpenFileName(this, "Open New File", QDir::homePath());
    ui->lineEdit_3->setText(file_name);
}

void GuiTest::on_toolButton_4_clicked()
{
    const QString &file_name = QFileDialog::getExistingDirectory(this, "Open New Directory", QDir::homePath());
    ui->lineEdit_4->setText(file_name);
}




void GuiTest::on_actionExit_triggered()
{
    this->close();
}
