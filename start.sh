#!/bin/bash
python python_sub.py &
python pc.py &
python -m streamlit run gitpod.py &