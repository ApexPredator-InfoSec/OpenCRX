# OpenCRX
OpenCRX Exploit

This is a python exploit for OpenCRX to gain a reverse shell if the DB password is known. The Offensive-Secuirty Andvanced Web Attacks and Exploitation course covers finding Authentication Bypass vulenrabilities and information disclosure/arbitrary file access vulnerabilities in OpenCRX that can lead to disclosing the DB password. The course then uses the hsqldb.jar GUI to interact with the DB to gain remote code execution.

This script provides a means to interact with the DB, upload a reverse shell, and execute the reverse shell connection without using the hsqldb GUI. It requires you to already know the DB password.
