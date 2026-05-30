# Interview Questions & Answers: Market Simplified (Backend C++)

## 1. "You designed a Logger module and integrated JWT. How did this reduce system errors by 30%?"
**Answer Framework:**
*   **Context:** We lacked visibility into production failures, and our authentication mechanism needed to scale securely for 2 million users.
*   **Action:** I built an asynchronous, thread-safe Logger module in C++ (likely utilizing a Singleton or Dependency Inversion pattern) to ensure writing logs didn't block the main execution thread. Simultaneously, I integrated stateless JWT (JSON Web Tokens) for authentication.
*   **Result:** The JWTs eliminated the need for constant database hits for session validation, speeding up API requests. The new Logger provided precise stack traces and context, allowing us to proactively identify and patch bugs, directly resulting in a 30% reduction in system errors.

## 2. "How did you build the RESTful Middleware APIs using TCP/IP and multithreading?"
**Answer Framework:**
*   **Context:** We needed a high-performance middleware to connect our frontend to external financial services like TCS BaNCS and Trendlyne.
*   **Action:** I developed the middleware in C++. I used raw socket programming (TCP/IP) for low-latency communication with the legacy financial systems, and exposed RESTful endpoints over HTTP for our clients. To handle high concurrent transaction volumes, I implemented a Thread Pool architecture using `std::thread`, `std::mutex`, and `std::condition_variable` to process incoming requests concurrently without exhausting system resources.
*   **Result:** This architecture efficiently handled the 15% increase in transaction volumes for the Investment Basket Place Order module.

## 3. "You mentioned GDB debugging and core dump analysis. Can you walk me through a time you solved a critical issue using core dumps?"
**Answer Framework:**
*   **Context:** In C++, segmentation faults (`SIGSEGV`) completely crash the application, and finding the root cause in a multi-threaded environment is notoriously difficult.
*   **Action:** Whenever a crash occurred in production, the system generated a core dump. I would load the core file along with the binary into GDB (`gdb ./app core`). I used `bt` (backtrace) to find the exact thread and function that crashed. Often, it was a race condition or a dangling pointer accessed by a background thread. I would inspect local variables (`info locals`) and registers to trace the exact bad memory address.
*   **Result:** This methodical debugging allowed me to resolve 95% of critical production crashes on the very first attempt.

## 4. "How did you improve database performance using Redis and Stored Procedures?"
**Answer Framework:**
*   **Context:** Our MySQL/Oracle databases were becoming a bottleneck under heavy read loads for stock data that didn't change every millisecond.
*   **Action:** I implemented a Redis caching layer in front of the database. Highly requested, static financial data was cached in memory (Redis), bypassing the database entirely. For complex write operations, instead of sending multiple queries from the C++ backend, I moved the logic directly into database Stored Procedures.
*   **Result:** This massively reduced network round-trips and DB CPU load, resulting in significantly faster API response times.
