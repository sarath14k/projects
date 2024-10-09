#ifndef GUI_H
#define GUI_H

#include <FL/Fl.H>
#include <FL/Fl_Window.H>
#include <FL/Fl_Input.H>
#include <FL/Fl_Text_Display.H>
#include <FL/Fl_Button.H>

class MyGUI {
public:
    MyGUI();
    void show();

private:
    Fl_Window *window;                   // Main window
    Fl_Input *input;                     // Input field for plaintext or ciphertext
    Fl_Text_Display *output;             // Output field for displaying results
    Fl_Button *encryptButton;            // Button to trigger encryption
    Fl_Button *decryptButton;            // Button to trigger decryption

    static void encryptCallback(Fl_Widget *widget, void *data); // Callback for encryption
    static void decryptCallback(Fl_Widget *widget, void *data); // Callback for decryption
};

#endif // GUI_H
