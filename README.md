# Testowanie i Optymalizacja Kodu Load Tests

This repository contains a collection of performance and load tests for the purpose of the "Testowanie i Optymalizacja Kodu" (Testing and Code Optimization) subject at the University of Economics. These tests are designed to evaluate the performance and scalability of various software components and systems.
And increase knowledge students knowledge in the subject.

## How to run?

Firstly what is needed, are the requirements installed and then a simple command:

```bash
locust --host http://localhost:8080 -f locustfile.py
```

Of course host should be adjusted to the needs, this particular locustfile, was created for purpose of testing mine [Things](https://culturedcode.com/things/) clone api server. 