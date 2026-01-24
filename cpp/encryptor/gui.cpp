#include "gui.h"
#include "rsaEncryptor.h"
#include <string>
#include <FL/Fl_File_Chooser.H>

MyGUI::MyGUI() {
    window = new Fl_Window(400, 300, "Encryption Tool");
    
    // Input field for plaintext or ciphertext
    input = new Fl_Input(100, 50, 200, 30, "Input:");
    
    // Output field for displaying results
    output = new Fl_Text_Display(100, 100, 200, 100, "Output:");
    
    // Encrypt and Decrypt buttons
    encryptButton = new Fl_Button(100, 220, 80, 30, "Encrypt");
    decryptButton = new Fl_Button(200, 220, 80, 30, "Decrypt");

    // Set callbacks for buttons
    encryptButton->callback(encryptCallback, this);
    decryptButton->callback(decryptCallback, this);
    
    window->end();
}

void MyGUI::show() {
    window->show();
}

void MyGUI::encryptCallback(Fl_Widget *widget, void *data) {
    MyGUI *gui = static_cast<MyGUI *>(data);
    
    // Get the input text
    std::string plaintext = gui->input->value();
    if (plaintext.empty()) {
        gui->output->buffer()->text("Input is empty!");
        return;
    }

    // Choose public key file
    Fl_File_Chooser chooser("~", "*", Fl_File_Chooser::SINGLE, "Select Public Key");
    chooser.show();
    while (chooser.shown()) {
        Fl::wait();
    }
    
    std::string publicKeyPath = chooser.value();
    RSAEncryptor rsa;

    // Load public key
    if (rsa.loadKey(publicKeyPath, true)) {  // Pass true for public key
        std::string ciphertext = rsa.encrypt(plaintext);
        gui->output->buffer()->text(ciphertext.c_str());
    } else {
        gui->output->buffer()->text("Failed to load public key!");
    }
}

void MyGUI::decryptCallback(Fl_Widget *widget, void *data) {
    MyGUI *gui = static_cast<MyGUI *>(data);
    
    // Get the input text
    std::string ciphertext = gui->input->value();
    if (ciphertext.empty()) {
        gui->output->buffer()->text("Input is empty!");
        return;
    }

    // Choose private key file
    Fl_File_Chooser chooser("~", "*", Fl_File_Chooser::SINGLE, "Select Private Key");
    chooser.show();
    while (chooser.shown()) {
        Fl::wait();
    }
    
    std::string privateKeyPath = chooser.value();
    RSAEncryptor rsa;

    // Load private key
    if (rsa.loadKey(privateKeyPath, false)) {  // Pass false for private key
        std::string plaintext = rsa.decrypt(ciphertext);
        gui->output->buffer()->text(plaintext.c_str());
    } else {
        gui->output->buffer()->text("Failed to load private key!");
    }
}
