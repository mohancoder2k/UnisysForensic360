import os
import base64
import requests
import cv2
import numpy as np
import imutils
from skimage.measure import label, regionprops

API_KEY = "AIzaSyBeiWHaYvnICWOQfY5U2PcEr1zfyTy2M4c"
API_URL = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-pro:generateContent"

def encode_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

def analyze_wound(test_image_path, dataset_folder):
    test_image_base64 = encode_image(test_image_path)
    
    prompt_text = """
    Here is a list of 50 different types of wounds commonly recognized in forensic and medical contexts:
    1. Sharp Force Wounds (Caused by sharp objects)
    - Incised wound – A clean, straight cut.
    - Stab wound – A deep, penetrating wound.
    - Puncture wound – A small but deep wound caused by pointed objects.
    - Chop wound – Caused by heavy, sharp objects like axes.
    - Slash wound – A long, superficial cutting wound.
    - Razor wound – A thin, precise cut caused by a razor.
    - Glass wound – A cut from broken glass, often irregular.
    - Scalpel wound – A surgical-type clean incision.
    - Sword wound – A deep, clean-cut wound from a bladed weapon.
    - Self-inflicted wound – Intentional wounds, often superficial.
    
    2. Blunt Force Wounds (Caused by blunt trauma)
    - Laceration – A torn wound with irregular edges.
    - Contusion (bruise) – Skin discoloration due to bleeding under the skin.
    - Abrasion (graze, scrape) – Superficial damage to the skin.
    - Crush injury – Tissue damage due to heavy force.
    - Avulsion – Tearing away of skin or tissue.
    - Fracture wound – A bone-breaking injury caused by impact.
    - Pressure sore (bed sore) – Skin ulceration from prolonged pressure.
    - Degloving injury – Skin torn off from underlying tissue.
    - Hematoma – A large, localized blood collection under the skin.
    - Road rash – Skin abrasion caused by friction with the road.
    
    3. Gunshot Wounds (Caused by firearms)
    - Entry gunshot wound – Small, circular wound at the bullet's entry point.
    - Exit gunshot wound – Large, irregular wound where the bullet exits.
    - Graze gunshot wound – A superficial wound caused by a bullet skimming the skin.
    - Contact gunshot wound – A wound caused by a gun fired at point-blank range.
    - Distant gunshot wound – A wound caused by a gun fired from far away.
    
    4. Burns and Thermal Wounds (Caused by heat, chemicals, or electricity)
    - First-degree burn – A superficial burn affecting only the outer skin.
    - Second-degree burn – A burn affecting deeper skin layers, forming blisters.
    - Third-degree burn – A severe burn damaging all skin layers.
    - Fourth-degree burn – A burn reaching muscles or bones.
    - Chemical burn – Skin damage caused by acids or alkaline substances.
    - Friction burn – Skin damage from rubbing against a rough surface.
    - Electrical burn – Caused by high-voltage electrical exposure.
    - Radiation burn – Damage from exposure to radiation, such as X-rays.
    - Scalding wound – Caused by hot liquids or steam.
    - Sunburn – A burn caused by UV radiation exposure.
    
    5. Specialized Wounds (Unique forensic cases)
    - Torture wound – Wounds inflicted during acts of torture.
    - Defensive wound – Found on hands/arms, indicating self-defense.
    - Hesitation wound – Multiple shallow cuts, often in suicide cases.
    - Bite wound – Caused by human or animal teeth.
    - Strangulation marks – Ligature or manual strangulation wounds.
    - Ligature mark – Circular marks on the neck due to strangulation.
    - Gunpowder tattooing – Small burns caused by close-range gunshots.
    - Suffocation marks – Facial bruising from asphyxiation.
    - Injection wound – Small puncture wounds from syringes or needles.
    - Taser wound – Small, electrical burn marks from stun guns.
    - Explosive injury – Wounds caused by blasts or shrapnel.
    - Dismemberment wound – Wounds caused by body part removal.
    - Scalping wound – Removal of the scalp, often seen in historical warfare.
    - Postmortem wound – Wounds inflicted after death.
    - Decomposition-related wound – Skin degradation due to decomposition.

    Analyze the wound in the provided image and determine which type it matches from the above list. Return only the wound name
    """
    
    request_data = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"inline_data": {"mime_type": "image/jpeg", "data": test_image_base64}},
                    {"text": prompt_text}
                ]
            }
        ]
    }

    response = requests.post(f"{API_URL}?key={API_KEY}", json=request_data)
    
    if response.status_code == 200:
        api_result = response.json()
        wound_info = api_result['candidates'][0]['content']['parts'][0]['text']
        print(f"Identified Wound Info: {wound_info}")
        
        best_match = match_wound_in_dataset(wound_info.split("\n")[0], dataset_folder)
        return wound_info, best_match
    else:
        print(f"Error: {response.text}")
        return None, None

def match_wound_in_dataset(wound_type, dataset_folder):
    wound_type_lower = wound_type.lower()
    best_match = None

    for img_name in os.listdir(dataset_folder):
        if wound_type_lower in img_name.lower():
            best_match = img_name
            break

    return best_match if best_match else "No match found"

def estimate_wound_dimensions(image_path, reference_length_mm=10):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    contours = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)

    if not contours:
        return "No wound detected"

    wound_contour = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(wound_contour)

    reference_object = None
    for cnt in contours:
        if cnt is not wound_contour:
            if reference_object is None or cv2.contourArea(cnt) > cv2.contourArea(reference_object):
                reference_object = cnt

    if reference_object is None:
        return "Reference object not found!"

    ref_x, ref_y, ref_w, ref_h = cv2.boundingRect(reference_object)
    pixel_per_mm = ref_w / reference_length_mm 
    wound_width_mm = w / pixel_per_mm
    wound_depth_mm = h / pixel_per_mm

    return round(wound_width_mm, 2), round(wound_depth_mm, 2)
