def serialize_user(user_doc: dict) -> dict:
    return {
        "id": str(user_doc["_id"]),
        "full_name": user_doc.get("full_name"),
        "email": user_doc.get("email"),
        "phone": user_doc.get("phone"),
    }


def serialize_meal(meal_doc: dict) -> dict:
    return {
        "id": str(meal_doc["_id"]),
        "user_id": str(meal_doc["user_id"]),
        "source": meal_doc.get("source"),
        "meal_name": meal_doc.get("meal_name"),
        "weight_grams": meal_doc.get("weight_grams"),
        "calories": meal_doc.get("calories"),
        "protein_grams": meal_doc.get("protein_grams"),
        "carbs_grams": meal_doc.get("carbs_grams"),
        "fats_grams": meal_doc.get("fats_grams"),
        "description": meal_doc.get("description"),
        "created_at": meal_doc.get("created_at"),
    }
