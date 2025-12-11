#!/bin/bash
cd backend
uvicorn main:app --reload --host 127.0.0.1 --port 8600
