from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, Response
import mysql.connector
from typing import List

app = FastAPI()

# Database Connection Function
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345678",
        database="unisys"
    )

# Upload Multiple Images for a Single Image ID
@app.post("/upload-images/")
async def upload_images(files: List[UploadFile] = File(...)):
    try:
        db = get_db_connection()
        cursor = db.cursor()

        image_ids = []  # Store generated image IDs

        for file in files:
            file_content = await file.read()

            # Insert image into MySQL (without specifying image_id explicitly)
            sql = "INSERT INTO crime_images (image_data) VALUES (%s)"
            cursor.execute(sql, (file_content,))
            image_ids.append(cursor.lastrowid)  # Get the auto-generated image_id

        db.commit()

        return JSONResponse(content={"message": f"{len(files)} images uploaded successfully", "image_ids": image_ids})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        db.close()

# Fetch All Images for Given Image IDs
@app.get("/get-images/{image_id}")
def get_images(image_id: int):
    try:
        db = get_db_connection()
        cursor = db.cursor()

        sql = "SELECT image_data FROM crime_images WHERE id = %s"
        cursor.execute(sql, (image_id,))
        image = cursor.fetchone()

        if image:
            return Response(content=image[0], media_type="image/jpeg")
        else:
            raise HTTPException(status_code=404, detail="No image found for this image ID")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        db.close()
