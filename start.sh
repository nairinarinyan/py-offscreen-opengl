#!/bin/bash

if [ "$1" == "offscreen" ]; then
    PYOPENGL_PLATFORM=egl python main.py
else
    python main.py
fi
