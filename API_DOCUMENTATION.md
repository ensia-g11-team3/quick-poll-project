# Quick Poll App - API Documentation

Complete API reference for the Quick Poll App backend.

## Base URL

```
http://localhost:5000/api
```

All endpoints are prefixed with `/api`

## Response Format

All responses are in JSON format.

### Success Response
```json
{
  "message": "Success message",
  "data": {...}
}
```

### Error Response
```json
{
  "error": "Error message"
}
```

## HTTP Status Codes

- `200` - OK (Success)
- `201` - Created (Resource created)
- `400` - Bad Request (Validation error)
- `401` - Unauthorized (Authentication failed)
- `404` - Not Found (Resource not found)
- `500` - Internal Server Error
- `503` - Service Unavailable (Feature not available)

---

## Polls Endpoints

### Create Poll

Create a new poll with multiple options.

**Endpoint:** `POST /api/polls`

**Request Body:**
```json
{
  "question": "What is your favorite programming language?",
  "options": ["Python", "JavaScript", "Java", "C++"],
  "creator_id": null
}
```

**Parameters:**
- `question` (string, required): Poll question text (max 255 characters)
- `options` (array, required): Array of option strings (minimum 2)
- `creator_id` (integer, optional): User ID of poll creator (null for anonymous)

**Response:** `201 Created`
```json
{
  "message": "Poll created successfully",
  "poll_id": 1,
  "poll_link": "abc123xyz789"
}
```

**Error Responses:**
- `400` - Missing question or insufficient options
- `500` - Database error

**Example (cURL):**
```bash
curl -X POST http://localhost:5000/api/polls \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is your favorite color?",
    "options": ["Red", "Blue", "Green"]
  }'
```

---

### Get Poll

Retrieve poll details including options and vote counts.

**Endpoint:** `GET /api/polls/{poll_link}`

**URL Parameters:**
- `poll_link` (string, required): Unique poll link identifier

**Response:** `200 OK`
```json
{
  "poll": {
    "poll_id": 1,
    "question": "What is your favorite color?",
    "poll_link": "abc123xyz789",
    "created_at": "2025-11-01T12:00:00",
    "options": [
      {
        "option_id": 1,
        "option_text": "Red",
        "vote_count": 5
      },
      {
        "option_id": 2,
        "option_text": "Blue",
        "vote_count": 3
      },
      {
        "option_id": 3,
        "option_text": "Green",
        "vote_count": 2
      }
    ]
  }
}
```

**Error Responses:**
- `404` - Poll not found
- `500` - Database error

**Example:**
```
GET http://localhost:5000/api/polls/abc123xyz789
```

---

### Get All Polls

Retrieve all polls in the system.

**Endpoint:** `GET /api/polls`

**Response:** `200 OK`
```json
{
  "polls": [
    {
      "poll_id": 1,
      "question": "What is your favorite color?",
      "poll_link": "abc123",
      "created_at": "2025-11-01T12:00:00",
      "options": [...]
    },
    {
      "poll_id": 2,
      "question": "Best programming language?",
      "poll_link": "xyz789",
      "created_at": "2025-11-01T13:00:00",
      "options": [...]
    }
  ]
}
```

**Example:**
```
GET http://localhost:5000/api/polls
```

---

### Get Poll Results

Get detailed poll results with vote counts and percentages.

**Endpoint:** `GET /api/polls/{poll_link}/results`

**URL Parameters:**
- `poll_link` (string, required): Unique poll link identifier

**Response:** `200 OK`
```json
{
  "poll": {
    "poll_id": 1,
    "question": "What is your favorite color?",
    "poll_link": "abc123xyz789",
    "created_at": "2025-11-01T12:00:00",
    "total_votes": 10,
    "options": [
      {
        "option_id": 1,
        "option_text": "Red",
        "vote_count": 5,
        "percentage": 50.0
      },
      {
        "option_id": 2,
        "option_text": "Blue",
        "vote_count": 3,
        "percentage": 30.0
      },
      {
        "option_id": 3,
        "option_text": "Green",
        "vote_count": 2,
        "percentage": 20.0
      }
    ]
  }
}
```

**Error Responses:**
- `404` - Poll not found
- `500` - Database error

**Example:**
```
GET http://localhost:5000/api/polls/abc123xyz789/results
```

---

## Votes Endpoints

### Submit Vote

Submit a vote for a poll option.

**Endpoint:** `POST /api/votes`

**Request Body:**
```json
{
  "poll_id": 1,
  "option_id": 2,
  "voter_id": null
}
```

**Parameters:**
- `poll_id` (integer, required): ID of the poll
- `option_id` (integer, required): ID of the selected option
- `voter_id` (integer, optional): ID of the voter (null for anonymous)

**Response:** `201 Created`
```json
{
  "message": "Vote submitted successfully",
  "vote_id": 1
}
```

**Error Responses:**
- `400` - Missing poll_id or option_id, invalid option, or duplicate vote
- `500` - Database error

**Validation:**
- Option must belong to the specified poll
- Users can only vote once per poll (if voter_id provided)
- Anonymous users can vote multiple times

**Example (cURL):**
```bash
curl -X POST http://localhost:5000/api/votes \
  -H "Content-Type: application/json" \
  -d '{
    "poll_id": 1,
    "option_id": 2,
    "voter_id": null
  }'
```

---

## Users Endpoints

**Note:** User endpoints require bcrypt installation. If bcrypt is not available, these endpoints will return `503 Service Unavailable`.

### Register User

Create a new user account.

**Endpoint:** `POST /api/users/register`

**Request Body:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepassword123"
}
```

**Parameters:**
- `username` (string, required): User's username (max 50 characters)
- `email` (string, required): User's email address (unique, max 100 characters)
- `password` (string, required): User's password (will be hashed)

**Response:** `201 Created`
```json
{
  "message": "User registered successfully",
  "user_id": 1
}
```

**Error Responses:**
- `400` - Missing fields or email already registered
- `503` - User authentication not available (bcrypt not installed)
- `500` - Database error

**Example:**
```bash
curl -X POST http://localhost:5000/api/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepassword123"
  }'
```

---

### Login User

Authenticate a user and retrieve user information.

**Endpoint:** `POST /api/users/login`

**Request Body:**
```json
{
  "email": "john@example.com",
  "password": "securepassword123"
}
```

**Parameters:**
- `email` (string, required): User's email address
- `password` (string, required): User's password

**Response:** `200 OK`
```json
{
  "message": "Login successful",
  "user": {
    "user_id": 1,
    "username": "john_doe",
    "email": "john@example.com"
  }
}
```

**Error Responses:**
- `400` - Missing email or password
- `401` - Invalid email or password
- `503` - User authentication not available (bcrypt not installed)
- `500` - Database error

**Example:**
```bash
curl -X POST http://localhost:5000/api/users/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "securepassword123"
  }'
```

---

## Data Models

### Poll
```json
{
  "poll_id": 1,
  "creator_id": null,
  "question": "Poll question text",
  "poll_link": "unique-link-identifier",
  "created_at": "2025-11-01T12:00:00"
}
```

### Option
```json
{
  "option_id": 1,
  "poll_id": 1,
  "option_text": "Option text"
}
```

### Vote
```json
{
  "vote_id": 1,
  "poll_id": 1,
  "voter_id": null,
  "option_id": 1,
  "voted_at": "2025-11-01T12:30:00"
}
```

### User
```json
{
  "user_id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "password_hash": "hashed_password"
}
```

---

## Error Handling

All errors follow a consistent format:

```json
{
  "error": "Descriptive error message"
}
```

### Common Error Scenarios

1. **Validation Errors (400)**
   - Missing required fields
   - Invalid data format
   - Business rule violations (e.g., less than 2 options)

2. **Not Found (404)**
   - Poll doesn't exist
   - Invalid poll link

3. **Unauthorized (401)**
   - Invalid login credentials

4. **Service Unavailable (503)**
   - Feature requires optional dependency (e.g., bcrypt)

5. **Server Errors (500)**
   - Database connection issues
   - Unexpected server errors

---

## Rate Limiting

Currently, there are no rate limits implemented. Consider implementing rate limiting for production use.

## CORS

The API supports Cross-Origin Resource Sharing (CORS) from all origins by default. Configure CORS settings in `backend/app.py` for production.

---

## Testing the API

### Using cURL

**Create Poll:**
```bash
curl -X POST http://localhost:5000/api/polls \
  -H "Content-Type: application/json" \
  -d '{"question": "Test?", "options": ["Yes", "No"]}'
```

**Get Poll:**
```bash
curl http://localhost:5000/api/polls/abc123
```

**Submit Vote:**
```bash
curl -X POST http://localhost:5000/api/votes \
  -H "Content-Type: application/json" \
  -d '{"poll_id": 1, "option_id": 1}'
```

### Using Browser

Simply navigate to:
- `http://localhost:5000/api/polls` - Get all polls
- `http://localhost:5000/api/polls/{poll_link}` - Get specific poll

### Using Postman/Insomnia

Import these endpoints into your API client:
1. Create collection "Quick Poll API"
2. Set base URL: `http://localhost:5000/api`
3. Add endpoints with appropriate methods and bodies

---

## Version History

- **v1.0** - Initial release
  - Poll CRUD operations
  - Voting system
  - Optional user authentication
  - SQLite database support

---

**For more information, see the main [README.md](README.md)**

