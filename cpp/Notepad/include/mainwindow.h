#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>

#include <QFile>
#include <QFileDialog>
#include <QTextStream>
#include <QMessageBox>
#include <QFontDialog>
#include <QFont>
#include <QColorDialog>
#include <QColor>
#include <QtPrintSupport/QPrinter>
#include <QtPrintSupport/QPrintDialog>

QT_BEGIN_NAMESPACE
namespace Ui {
class MainWindow;
}
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private slots:
    void on_actionNew_triggered();

    void on_actionOpen_triggered();

    void on_actionSave_triggered();

    void on_actionSave_As_triggered();

    void on_actionCut_triggered();

    void on_actionCopy_triggered();

    void on_actionPaste_triggered();

    void on_actionUndo_triggered();

    void on_actionRedo_triggered();

    void on_actionPrint_triggered();

    void on_actionAbout_Notepad_triggered();

    void closeTab(int index);

    void on_actionType_triggered();

    void on_actionColor_triggered();

    void on_actionBGColor_triggered();

    void on_actionBGColorWindow_triggered();

private:
    Ui::MainWindow *ui;
    QString _file_path;
    QTabWidget *tabWidget;
    QMap<int, QString>tabFilePaths;
};
#endif // MAINWINDOW_H
