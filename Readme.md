# Forensic 360 - Crime Investigation Platform

Forensic 360 is a crime investigation platform that integrates advanced forensic techniques with a 3D visualization system. The project utilizes FastAPI for the backend, a React-based frontend with Three.js (Three Fiber), and a MySQL database for structured crime data storage.

## 🚀 Project Overview
Forensic 360 provides:
- **Case Management System** to store and manage crime-related data
- **3D Visualization** using GLB models for crime scene reconstruction
- **Image Processing & Analysis** with dataset integration
- **Machine Learning** to assist in forensic investigations

---

## 📅 Development Timeline

### **Day 1** - Project Setup & Planning
- Defined project requirements & scope
- Set up project structure & dependencies
- Set up of Github Collaborations for Remote work process 
- Set up FastAPI backend with MySQL
- Created base API endpoints for case creation

### **Day 2** - API & Database Implementation
- Designed MySQL schema for `crime_cases` and `crime_images`
- Implemented FastAPI endpoints:
  - `POST /create-case/` to add a case
  - `POST /upload-images/{case_id}` to upload crime scene images
  - `GET /get-images/{case_id}` to retrieve images
- Tested APIs using Postman

### **Day 3** - 3D Model Setup & Frontend Development
- Integrated Three.js (Three Fiber) for crime scene visualization
- Worked with `.glb` models for 3D representation
- Established communication between frontend and FastAPI backend

### **Day 4** - Dataset Research & GLB Model Learning
- **Searching for forensic datasets**, including:
  - Bloodstain pattern datasets
  - Crime scene images dataset
  - Fingerprint recognition dataset
  - Shoeprint & tire tread datasets
- **Learning GLB model optimizations** for rendering forensic evidence in the 3D environment

---

## 🏗️ Tech Stack
- **Backend**: FastAPI, MySQL
- **Frontend**: React, Three.js (Three Fiber)
- **Database**: MySQL
- **Tools**: Postman, Blender (for 3D models), Jupyter (for ML model training)

---

## 🔥 API Endpoints
### 1️⃣ Create a Case
```http
POST /create-case/
```
#### Request Body (JSON):
```json
{
  "case_description": "Robbery at a gas station"
}
```
#### Response:
```json
{
  "case_id": 1,
  "message": "Case created successfully"
}
```

### 2️⃣ Upload Images for a Case
```http
POST /upload-images/{case_id}
```
#### Request:
- `case_id` (Path Parameter): Case ID
- `files[]` (Multipart Form Data): Images to upload

### 3️⃣ Retrieve Images for a Case
```http
GET /get-images/{case_id}
```
#### Response:
```json
{
  "images": ["base64_encoded_image_1", "base64_encoded_image_2"]
}
```

---

## 📌 Next Steps
- 🔍 **Dataset preprocessing** for ML model training
- 🧪 **Integrating AI models** for crime scene analysis
- 🌍 **Enhancing 3D visualization** with dynamic case data

---

## 🤝 Contributors
- **Mohan B (Developer)**
- **Emmanuel Matthew (Developer)**
- **Swetha G  (Developer)**
- **Wilson Bernard (Developer)**

Let's revolutionize forensic analysis with technology! 🚀