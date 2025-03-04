import base64
from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.responses import JSONResponse, Response
import mysql.connector
from typing import List
from pydantic import BaseModel

app = FastAPI()

# Database Connection Function
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345678",
        database="unisys"
    )
class CaseCreate(BaseModel):
    case_description: str
@app.post("/create-case/")
def create_case(case: CaseCreate):
    try:
        db = get_db_connection()
        cursor = db.cursor()

        sql = "INSERT INTO crime_cases (case_description) VALUES (%s)"
        cursor.execute(sql, (case.case_description,))
        case_id = cursor.lastrowid  # Get the auto-generated case_id

        db.commit()

        return JSONResponse(content={"case_id": case_id, "message": "Case created successfully"})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        db.close()
# ✅ Upload Multiple Images for a Single Case ID
@app.post("/upload-images/{case_id}")
async def upload_images(case_id: int, files: List[UploadFile] = File(...)):
    try:
        db = get_db_connection()
        cursor = db.cursor()

        # 🔹 Check if case_id exists
        cursor.execute("SELECT case_id FROM crime_cases WHERE case_id = %s", (case_id,))
        case = cursor.fetchone()
        if not case:
            raise HTTPException(status_code=400, detail="Error: Case ID does not exist.")

        image_ids = []

        for file in files:
            file_content = await file.read()
            sql = "INSERT INTO crime_images (case_id, image_data) VALUES (%s, %s)"
            cursor.execute(sql, (case_id, file_content))
            image_ids.append(cursor.lastrowid)

        db.commit()

        return JSONResponse(content={"message": f"{len(files)} images uploaded successfully", "image_ids": image_ids})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        db.close()

@app.get("/get-images/{case_id}")
def get_images(case_id: int):
    try:
        db = get_db_connection()
        cursor = db.cursor()

        sql = "SELECT image_data FROM crime_images WHERE case_id = %s"
        cursor.execute(sql, (case_id,))
        images = cursor.fetchall()

        if not images:
            raise HTTPException(status_code=404, detail="No images found for this case ID")

        # Convert each binary image to Base64
        base64_images = [base64.b64encode(image[0]).decode('utf-8') for image in images]

        return JSONResponse(content={"images": base64_images})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        db.close()
