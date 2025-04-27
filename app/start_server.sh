#!/bin/bash

echo "Starte Easy Learn Server auf http://localhost:8000 ..."
uvicorn main:app --reload --host 0.0.0.0 --port 8000