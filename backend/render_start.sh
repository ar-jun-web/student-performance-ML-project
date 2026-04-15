#!/bin/bash
cp ../MLmodels/enhanced_model.pkl ./enhanced_model.pkl 2>/dev/null || true
uvicorn app.main:app --host 0.0.0.0 --port $PORT
