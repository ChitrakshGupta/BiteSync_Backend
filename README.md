# HealthX FastAPI Backend

Production-ready FastAPI backend scaffold for:
- Mobile/Web friendly auth (`email` or `phone` login)
- AI food image analysis + meal storage
- Manual meal entry + calorie/macros tracking
- 30-second workout video form analysis
- MongoDB Atlas cloud support
- Swagger/OpenAPI docs for Postman testing

## 1. Tech Stack
- FastAPI
- MongoDB Atlas (`motor` async driver)
- JWT auth
- Google Gemini API (`google-generativeai`)

## 2. Folder Structure
```bash
app/
  api/
    deps.py
    v1/
      auth_routes.py
      meal_routes.py
      form_routes.py
      router.py
  core/
    config.py
  db/
    mongo.py
  models/
    serializers.py
  schemas/
    auth.py
    meal.py
    analysis.py
  services/
    auth_service.py
    meal_service.py
    gemini_service.py
  utils/
    common.py
    security.py
  main.py
```

## 3. Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Update `.env` with your own values:
- `MONGODB_URI`: Atlas cloud URI
- `JWT_SECRET_KEY`
- `GEMINI_API_KEY`

## 4. Run Server
```bash
uvicorn app.main:app --reload
```

## 5. API Docs
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`
- OpenAPI JSON: `http://127.0.0.1:8000/openapi.json`

Import `openapi.json` in Postman to get all endpoints automatically.

## 6. API Endpoints (v1)
Base URL: `http://127.0.0.1:8000/api/v1`

### Auth

#### `POST /auth/signup`
Input:
```json
{
  "full_name": "John Doe",
  "email": "john@example.com",
  "phone": "+919999999999",
  "password": "secret123"
}
```
Output:
```json
{
  "access_token": "<jwt>",
  "token_type": "bearer",
  "user_id": "665...."
}
```

#### `POST /auth/login`
Input:
```json
{
  "identifier": "john@example.com",
  "password": "secret123",
  "device_type": "android",
  "device_id": "pixel-8-pro"
}
```
Output:
```json
{
  "access_token": "<jwt>",
  "token_type": "bearer",
  "user_id": "665...."
}
```

#### `GET /auth/me`
Header: `Authorization: Bearer <jwt>`

Output:
```json
{
  "id": "665....",
  "full_name": "John Doe",
  "email": "john@example.com",
  "phone": "+919999999999"
}
```

### Meals

#### `POST /meals/analyze-image`
- `multipart/form-data`
- Key: `image` (file)
- Header: `Authorization: Bearer <jwt>`

Output:
```json
{
  "meal_name": "Paneer Salad",
  "description": "Fresh salad with paneer cubes and vegetables",
  "estimated_weight_grams": 280,
  "calories": 420,
  "protein_grams": 22,
  "carbs_grams": 18,
  "fats_grams": 28,
  "confidence": 0.86
}
```
This also auto-saves the meal in `meals` collection.

#### `POST /meals/manual`
Input:
```json
{
  "meal_name": "Oats",
  "weight_grams": 80,
  "calories": 300,
  "protein_grams": 10,
  "carbs_grams": 48,
  "fats_grams": 6
}
```
Output: Saved meal object.

#### `GET /meals/summary?date=2026-05-29`
Output:
```json
{
  "date": "2026-05-29",
  "total_meals": 3,
  "total_calories": 1110,
  "total_protein_grams": 65,
  "total_carbs_grams": 120,
  "total_fats_grams": 41,
  "meals": []
}
```

### Workout Form Analysis

#### `POST /form/analyze-video`
- `multipart/form-data`
- Key: `video` (file, recommend <= 30 sec)
- Header: `Authorization: Bearer <jwt>`

Output:
```json
{
  "exercise_name": "Squat",
  "summary": "Good control but depth is inconsistent",
  "what_is_good": ["Stable knees", "Neutral spine"],
  "what_is_missing": ["Reach parallel depth", "Drive hips up evenly"],
  "risk_flags": ["Mild lower-back rounding at bottom"],
  "recommendations": ["Reduce load", "Use tempo reps 3-1-2"],
  "confidence": 0.81
}
```

## 7. MongoDB Collections
- `users`
- `meals`

Indexes created on startup:
- `users.email` unique sparse
- `users.phone` unique sparse
- `meals.user_id + meals.created_at`

## 8. Notes for Mobile App Integration
- `identifier` supports both email and phone for one-login API.
- Keep JWT in secure storage on device (Keychain/Keystore).
- Send `device_type` and `device_id` during login for device-aware sessions.

## 9. Next Suggested Improvements
- Refresh token flow
- Phone OTP verification
- Background processing for larger videos
- Role-based access (admin/nutritionist/coach)
# health_backend
