#include "mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    tabWidget = new QTabWidget(this);
    tabWidget->setTabsClosable(true); // Enable close buttons on tabs
    setCentralWidget(tabWidget);
    // Connect the tab close button to a custom slot
    connect(tabWidget, &QTabWidget::tabCloseRequested,
            this, &MainWindow::closeTab);
    QTextEdit *initialTextEdit = new QTextEdit(this);
    tabWidget->addTab(initialTextEdit, "New Document");
}

MainWindow::~MainWindow()
{
    delete ui;
}


void MainWindow::on_actionNew_triggered()
{
    // Create a new QTextEdit widget
    QTextEdit *newTextEdit = new QTextEdit(this);
    // Add the new text editor to a new tab in the QTabWidget
    int newTabIndex = tabWidget->addTab(newTextEdit, "Untitled");
    // Set focus to the newly created tab
    tabWidget->setCurrentIndex(newTabIndex);
    // Optionally reset the _file_path for the new tab
    _file_path = "";
}


void MainWindow::on_actionOpen_triggered()
{
    QString fileName = QFileDialog::getOpenFileName(
                        this,tr("Text Files (*.txt);;All Files (*)"));
    if (!fileName.isEmpty()){
        // Create a new QTextEdit widget for the new tab
        QTextEdit *newTextEdit = new QTextEdit(this);
        // Load the content of the file into the text editor
        QFile file(fileName);
        if (file.open(QIODevice::ReadOnly | QIODevice::Text)){
            QTextStream in(&file);
            newTextEdit->setText(in.readAll());
            file.close();
        }

        // Add the new text editor to a new tab and set the filename as the tab title
        int newTabIndex = tabWidget->addTab(newTextEdit, QFileInfo(fileName).fileName());

        // Set focus to the newly created tab
        tabWidget->setCurrentIndex(newTabIndex);

        // Update _file_path with the opened file's path
        _file_path = fileName;
    }
}

void MainWindow::closeTab(int index)
{
    // Remove the tab at the given index
    QWidget *widget = tabWidget->widget(index);
    tabWidget->removeTab(index);
    // Optionally, delete the associated widget
    delete widget;
}

void MainWindow::on_actionSave_triggered()
{
    // Get the current tab index
    int currentIndex = tabWidget->currentIndex();
    // Retrieve the QTextEdit of the current tab
    QTextEdit *currentTextEdit = qobject_cast<QTextEdit *>(tabWidget->widget(currentIndex));
    
    if (!currentTextEdit)
        return;  // No valid text editor found

    // Check if the current tab has an associated file path
    QString currentFilePath = tabFilePaths.value(currentIndex);
    
    if (currentFilePath.isEmpty()) {
        // If no file path, treat it as "Save As"
        on_actionSave_As_triggered();
        return;
    }

    // Save the file
    QFile file(currentFilePath);
    if (!file.open(QFile::WriteOnly | QFile::Text)) {
        QMessageBox::warning(this, "..", "File could not be opened for writing");
        return;
    }

    QTextStream out(&file);
    QString text = currentTextEdit->toPlainText();
    out << text;
    file.flush();
    file.close();
}

void MainWindow::on_actionSave_As_triggered()
{
    // Get the current tab index
    int currentIndex = tabWidget->currentIndex();
    // Retrieve the QTextEdit of the current tab
    QTextEdit *currentTextEdit = qobject_cast<QTextEdit *>(tabWidget->widget(currentIndex));
   
    if (!currentTextEdit)
        return;  // No valid text editor found

    // Open a file dialog to choose the save location
    QString file_name = QFileDialog::getSaveFileName(this, "Save As");
    if (file_name.isEmpty())
        return;  // User canceled the save dialog

    // Save the file path in the map for future saves
    tabFilePaths[currentIndex] = file_name;

    // Save the file
    QFile file(file_name);
    if (!file.open(QFile::WriteOnly | QFile::Text)) {
        QMessageBox::warning(this, "..", "File could not be opened for writing");
        return;
    }

    QTextStream out(&file);
    QString text = currentTextEdit->toPlainText();
    out << text;
    file.flush();
    file.close();

    // Update the tab title with the file name
    tabWidget->setTabText(currentIndex, QFileInfo(file_name).fileName());
}

void MainWindow::on_actionCut_triggered()
{
    // Get the current QTextEdit from the active tab
    QTextEdit *currentTextEdit = qobject_cast<QTextEdit *>(tabWidget->currentWidget());
    if (currentTextEdit)
        currentTextEdit->cut();  // Perform cut operation

}

void MainWindow::on_actionCopy_triggered()
{
    // Get the current QTextEdit from the active tab
    QTextEdit *currentTextEdit = qobject_cast<QTextEdit *>(tabWidget->currentWidget());
    if (currentTextEdit)
        currentTextEdit->copy();  // Perform copy operation

}

void MainWindow::on_actionPaste_triggered()
{
    // Get the current QTextEdit from the active tab
    QTextEdit *currentTextEdit = qobject_cast<QTextEdit *>(tabWidget->currentWidget());
    if (currentTextEdit)
        currentTextEdit->paste();  // Perform paste operation

}

void MainWindow::on_actionUndo_triggered()
{
    // Get the current QTextEdit from the active tab
    QTextEdit *currentTextEdit = qobject_cast<QTextEdit *>(tabWidget->currentWidget());
    if (currentTextEdit)
        currentTextEdit->undo();  // Perform undo operation

}

void MainWindow::on_actionRedo_triggered()
{
    // Get the current QTextEdit from the active tab
    QTextEdit *currentTextEdit = qobject_cast<QTextEdit *>(tabWidget->currentWidget());
    if (currentTextEdit)
        currentTextEdit->redo();  // Perform redo operation

}


void MainWindow::on_actionPrint_triggered()
{
    // Get the current QTextEdit from the active tab
    QTextEdit *currentTextEdit = qobject_cast<QTextEdit *>(tabWidget->currentWidget());

    if (currentTextEdit){
        // Create a printer object
        QPrinter printer;
        // Create a print dialog and pass the printer object to it
        QPrintDialog printDialog(&printer, this);

        // Check if the user accepted the print dialog
        if (printDialog.exec() == QDialog::Accepted)
        {
            // Print the content of the QTextEdit
            currentTextEdit->print(&printer);
        }
    } else {
        // Handle case where there's no active QTextEdit (if needed)
        QMessageBox::warning(this, "Print", "No document open to print.");
    }
}



void MainWindow::on_actionAbout_Notepad_triggered()
{
    QString about_text;
    about_text = "Author : Sarath Kumar T\n";
    about_text += "Notepad v1.0.0\n";
    about_text += "(C)Sarath\n";
    QMessageBox::about(this,"About Notepad",about_text);
}


void MainWindow::on_actionType_triggered()
{
    // Open a font selection dialog
    bool ok;
    QFont font = QFontDialog::getFont(&ok, this);

    if (ok) {
        // Get the current QTextEdit from the active tab
        QTextEdit *currentTextEdit = qobject_cast<QTextEdit *>(tabWidget->currentWidget());
        if (currentTextEdit)
        {
            // Set the selected font on the current text editor
            currentTextEdit->setFont(font);
        }
    }
}


void MainWindow::on_actionColor_triggered()
{
    QColor color = QColorDialog::getColor(Qt::white, this, "Choose Color");
    if(color.isValid()){
        QTextEdit *currentTextEdit = qobject_cast<QTextEdit *>(tabWidget->currentWidget());
        if(currentTextEdit)
            currentTextEdit->setTextColor(color);
    }
}


void MainWindow::on_actionBGColor_triggered()
{
    QColor color = QColorDialog::getColor(Qt::white, this, "Choose Color");
    if(color.isValid()){
        QTextEdit *currentTextEdit = qobject_cast<QTextEdit *>(tabWidget->currentWidget());
        if(currentTextEdit)
            currentTextEdit->setTextBackgroundColor(color);
    }
}


void MainWindow::on_actionBGColorWindow_triggered()
{
    QColor color = QColorDialog::getColor(Qt::white, this, "Choose Color");

    if (color.isValid()){
        // Get the current QTextEdit from the active tab
        QTextEdit *currentTextEdit = qobject_cast<QTextEdit *>(tabWidget->currentWidget());

        if (currentTextEdit){
            // Set the background color for the current QTextEdit
            QPalette p = currentTextEdit->palette();
            p.setColor(QPalette::Base, color);  // Set the background color
            currentTextEdit->setPalette(p);
        }
    }
}

