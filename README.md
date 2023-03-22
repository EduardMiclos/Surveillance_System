# Surveillance System
This project represents my thesis at the Politehnica University of Timișoara, Faculty of Automatic Control and Computer Science.

## Motivation
In modern times, it is a well-known fact that, among other rights and necessities, the sense of safety and security is one of the most essential
parts that constitute an individual's life. In order to bring day-to-day activies to an end, a person shall feel safe inside his or her
environment. By making use of current technologies and innovations, we are able to create complex surveillance systems that increase 
the levels of security of each individuals operating inside certain spaces and locations.

## Technologies
The following technologies (meaning software applications, programming languages, frameworks etc.) were used:

- Raspberry Pi OS (32-bit);
- Linux;
- Python.
- Tensorflow.
- Numpy.
- Flask.
- Gunicorn.
- Git.

## Hardware components
The following hardware components were used inside this project:

- 2x Raspberry Pi 4 B Model/4GB;
- 2x Camera module, Waveshare, 5 MP, 1080p, 31x32 mm;
- 2x MicroSD Kingston Canvas Select Plus memory card, 128GB, 100MB/s + adapter.

## Project description

### What does it do and how does it work?
The <b>Surveillance System</b> represents a set of interconnected embedded systems (i.e., Single-Board Computers) that are either part of a <b>Client</b> module or a <b>Server</b> module from the <b>Client-Server</b> architecture. 

- A client is an entity which consist of an SBC connected to a camera, whose sole purpose is to capture and send video frames to a centralized server located inside a Cloud Environment, where the Neural Network lays.
- A server is an entity which receives data from one or multiple clients. It will act as a <b>Web server</b> that the employees will be able to access by making use of their log-in credentials.

The <b>web interface</b> is provided to the end-user by the webserver. Violent actions will be detected and notified on the screen by coloring the margins of the camera-frame. The event will be saved inside the database, along with a short and representative sequence of frames, information about the time, the date and more.