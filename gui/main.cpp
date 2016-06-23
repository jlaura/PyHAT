#include "guitest.h"
#include <QApplication>
#include <QSplashScreen>
#include <QTimer>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    QSplashScreen *splash = new QSplashScreen;
    splash->setPixmap(QPixmap("C:/Users/User/Documents/QTprograms/SplashScreen/acxiom-data-packages4.png"));
    splash->show();
    GuiTest w;
    QTimer::singleShot(2700, splash, SLOT(close()));
    QTimer::singleShot(2700, &w, SLOT(show()));
    return a.exec();
}
