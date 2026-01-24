#include <iostream>
#include <string>
#include <thread>
#include <mutex>

using namespace std;

class Logger
{
    static int ctr;
    static Logger *loggerInstance;
    static mutex mtx;

    Logger()
    {
        ctr++;
        cout << "New instance created " << ctr << endl;
    }

public:
    static Logger *getLogger()
    {
        lock_guard<mutex> lock(mtx); // Lock to ensure thread safety
        if (loggerInstance == nullptr)
        {
            loggerInstance = new Logger();
        }

        return loggerInstance;
    }

    void log(const string &message)
    {
        cout << "Logging message: " << message << endl;
    }

    ~Logger()
    {
        delete loggerInstance;
        loggerInstance = nullptr;
    }
};

int Logger::ctr = 0;
Logger *Logger::loggerInstance = nullptr;
mutex Logger::mtx;

void user1Logs()
{
    Logger *logger1 = Logger::getLogger();
    logger1->log("This is user 1\n");
}

void user2Logs()
{
    Logger *logger2 = Logger::getLogger();
    logger2->log("This is user 2\n");
}

int main()
{
    thread t1(user1Logs);
    thread t2(user2Logs);

    t1.join();
    t2.join();
    return 0;
}
