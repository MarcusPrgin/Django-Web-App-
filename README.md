# 🧩 Django Web Application Project

## Overview

This is a full-stack web application built using **Django** with **JavaScript-enhanced UI**. The goal is to explore modern web development, cybersecurity best practices, and self-hosted vs SaaS architecture options. The project also introduces advanced features like location awareness and peer tracking.

---

## 🚀 Features

- Django-powered dynamic web app
- SQLite (default), with optional PostgreSQL or MongoDB support
- Enhanced frontend with JavaScript (optionally React or Vue)
- Cybersecurity hardening (OWASP, Cloudflare, SQLi protection)
- Mobile-friendly design and optional location features
- Peer proximity tracking using BLE (e.g., Tile, AirTag)
- Map integration with Google Maps or Leaflet/OpenStreetMap
- Optional Firebase implementation for SaaS comparison

---

## 📦 Setup & Installation

```bash
# Clone repo and setup virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run initial migrations and start server
python manage.py migrate
python manage.py runserver
