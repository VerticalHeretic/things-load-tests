# Performance and Load Tests for "Testowanie i Optymalizacja Kodu"

This repository contains a collection of performance and load tests created for the "Testowanie i Optymalizacja Kodu" (Testing and Code Optimization) course at the University of Economics. These tests are designed to evaluate the performance and scalability of various software components and systems, and to enhance students' understanding of the subject.

## How to Run the Tests

First, ensure that all required dependencies are installed. Then, execute the following command to run the tests:

```bash
locust --host http://localhost:8080 -f locustfile.py
```

Note that the --host option should be adjusted to match your specific requirements. The provided locustfile.py is designed for testing my [Things](https://culturedcode.com/things/) clone API server, which is written in Swift.