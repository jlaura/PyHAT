/****************************************************************************
** Meta object code from reading C++ file 'guitest.h'
**
** Created by: The Qt Meta Object Compiler version 67 (Qt 5.7.0)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include "../../src/PYSAT_GUI/guitest.h"
#include <QtCore/qbytearray.h>
#include <QtCore/qmetatype.h>
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'guitest.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 67
#error "This file was generated using the moc from 5.7.0. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

QT_BEGIN_MOC_NAMESPACE
struct qt_meta_stringdata_GuiTest_t {
    QByteArrayData data[15];
    char stringdata0[223];
};
#define QT_MOC_LITERAL(idx, ofs, len) \
    Q_STATIC_BYTE_ARRAY_DATA_HEADER_INITIALIZER_WITH_OFFSET(len, \
    qptrdiff(offsetof(qt_meta_stringdata_GuiTest_t, stringdata0) + ofs \
        - idx * sizeof(QByteArrayData)) \
    )
static const qt_meta_stringdata_GuiTest_t qt_meta_stringdata_GuiTest = {
    {
QT_MOC_LITERAL(0, 0, 7), // "GuiTest"
QT_MOC_LITERAL(1, 8, 21), // "on_toolButton_clicked"
QT_MOC_LITERAL(2, 30, 0), // ""
QT_MOC_LITERAL(3, 31, 23), // "on_toolButton_2_clicked"
QT_MOC_LITERAL(4, 55, 23), // "on_toolButton_3_clicked"
QT_MOC_LITERAL(5, 79, 23), // "on_toolButton_4_clicked"
QT_MOC_LITERAL(6, 103, 23), // "on_actionExit_triggered"
QT_MOC_LITERAL(7, 127, 24), // "on_pushButton_13_clicked"
QT_MOC_LITERAL(8, 152, 21), // "on_pushButton_clicked"
QT_MOC_LITERAL(9, 174, 6), // "labels"
QT_MOC_LITERAL(10, 181, 7), // "QLabel*"
QT_MOC_LITERAL(11, 189, 4), // "size"
QT_MOC_LITERAL(12, 194, 9), // "spinright"
QT_MOC_LITERAL(13, 204, 9), // "QSpinBox*"
QT_MOC_LITERAL(14, 214, 8) // "spinleft"

    },
    "GuiTest\0on_toolButton_clicked\0\0"
    "on_toolButton_2_clicked\0on_toolButton_3_clicked\0"
    "on_toolButton_4_clicked\0on_actionExit_triggered\0"
    "on_pushButton_13_clicked\0on_pushButton_clicked\0"
    "labels\0QLabel*\0size\0spinright\0QSpinBox*\0"
    "spinleft"
};
#undef QT_MOC_LITERAL

static const uint qt_meta_data_GuiTest[] = {

 // content:
       7,       // revision
       0,       // classname
       0,    0, // classinfo
      10,   14, // methods
       0,    0, // properties
       0,    0, // enums/sets
       0,    0, // constructors
       0,       // flags
       0,       // signalCount

 // slots: name, argc, parameters, tag, flags
       1,    0,   64,    2, 0x08 /* Private */,
       3,    0,   65,    2, 0x08 /* Private */,
       4,    0,   66,    2, 0x08 /* Private */,
       5,    0,   67,    2, 0x08 /* Private */,
       6,    0,   68,    2, 0x08 /* Private */,
       7,    0,   69,    2, 0x08 /* Private */,
       8,    0,   70,    2, 0x08 /* Private */,
       9,    1,   71,    2, 0x08 /* Private */,
      12,    1,   74,    2, 0x08 /* Private */,
      14,    1,   77,    2, 0x08 /* Private */,

 // slots: parameters
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    0x80000000 | 10, QMetaType::Int,   11,
    0x80000000 | 13, QMetaType::Int,   11,
    0x80000000 | 13, QMetaType::Int,   11,

       0        // eod
};

void GuiTest::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    if (_c == QMetaObject::InvokeMetaMethod) {
        GuiTest *_t = static_cast<GuiTest *>(_o);
        Q_UNUSED(_t)
        switch (_id) {
        case 0: _t->on_toolButton_clicked(); break;
        case 1: _t->on_toolButton_2_clicked(); break;
        case 2: _t->on_toolButton_3_clicked(); break;
        case 3: _t->on_toolButton_4_clicked(); break;
        case 4: _t->on_actionExit_triggered(); break;
        case 5: _t->on_pushButton_13_clicked(); break;
        case 6: _t->on_pushButton_clicked(); break;
        case 7: { QLabel* _r = _t->labels((*reinterpret_cast< int(*)>(_a[1])));
            if (_a[0]) *reinterpret_cast< QLabel**>(_a[0]) = _r; }  break;
        case 8: { QSpinBox* _r = _t->spinright((*reinterpret_cast< int(*)>(_a[1])));
            if (_a[0]) *reinterpret_cast< QSpinBox**>(_a[0]) = _r; }  break;
        case 9: { QSpinBox* _r = _t->spinleft((*reinterpret_cast< int(*)>(_a[1])));
            if (_a[0]) *reinterpret_cast< QSpinBox**>(_a[0]) = _r; }  break;
        default: ;
        }
    }
}

const QMetaObject GuiTest::staticMetaObject = {
    { &QMainWindow::staticMetaObject, qt_meta_stringdata_GuiTest.data,
      qt_meta_data_GuiTest,  qt_static_metacall, Q_NULLPTR, Q_NULLPTR}
};


const QMetaObject *GuiTest::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->dynamicMetaObject() : &staticMetaObject;
}

void *GuiTest::qt_metacast(const char *_clname)
{
    if (!_clname) return Q_NULLPTR;
    if (!strcmp(_clname, qt_meta_stringdata_GuiTest.stringdata0))
        return static_cast<void*>(const_cast< GuiTest*>(this));
    return QMainWindow::qt_metacast(_clname);
}

int GuiTest::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QMainWindow::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        if (_id < 10)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 10;
    } else if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        if (_id < 10)
            *reinterpret_cast<int*>(_a[0]) = -1;
        _id -= 10;
    }
    return _id;
}
QT_END_MOC_NAMESPACE
