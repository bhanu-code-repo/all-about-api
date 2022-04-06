#!/bin/bash

start cmd.exe /k "python service_one.py"
start cmd.exe /k "python service_two.py"
start cmd.exe /k "python service_three.py"
start cmd.exe /k "python service_four.py"
start cmd.exe /k "python service_five.py"

TIMEOUT /t 10
start cmd.exe /k "python service_monitor.py"