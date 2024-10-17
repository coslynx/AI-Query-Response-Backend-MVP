## AI Query Response Backend - API Documentation

This document provides a comprehensive overview of the API endpoints and functionalities offered by the AI Query Response Backend MVP. It includes detailed specifications for each endpoint, covering request and response structures, authentication requirements, error handling, and other relevant information.

### 1. Overview

The AI Query Response Backend is a Python-based service that simplifies the integration of OpenAI's language models into applications. It provides a RESTful API for sending user queries, receiving AI-generated responses, and managing user accounts. 

### 2. Authentication

#### 2.1. Login Endpoint

**HTTP Method:** POST
**URL:** `/login`

**Request Body:**

```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response Body (Success):**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyQGV4YW1wbGUuY29tIiwiZXhwIjoxNjg4NjY2NDAwfQ.T4c4N_qPqU-h68oD15W4a11Y_qZ-p9_jXz6p39O6zI",
  "token_type": "bearer"
}
```

**Response Body (Failure):**

```json
{
  "detail": "Incorrect email or password"
}
```

**Description:**

The `/login` endpoint handles user authentication. It requires an email address and password in the request body. If the credentials are valid, the endpoint generates a JSON Web Token (JWT) and returns it along with the token type "bearer". The JWT can be used for authentication in subsequent API requests.

#### 2.2. Protected Endpoints

All endpoints described below require authentication. To access these endpoints, include the JWT access token in the `Authorization` header of requests, using the format `Bearer <token>`. 

### 3. Query Processing

#### 3.1. Process Query Endpoint

**HTTP Method:** POST
**URL:** `/query`

**Request Body:**

```json
{
  "query": "What is the capital of France?",
  "model": "text-davinci-003",
  "user_id": 1
}
```

**Response Body (Success):**

```json
{
  "query_id": 12345,
  "response": "Paris"
}
```

**Response Body (Failure):**

```json
{
  "detail": "Error processing query: OpenAI API error: ..."
}
```

**Description:**

The `/query` endpoint processes user queries using OpenAI's API. It requires the user's query text, the OpenAI model to use, and the user's ID in the request body. The backend sends the query to the selected OpenAI model, receives the response, and stores it in the database. The endpoint returns the query ID and the AI-generated response.

#### 3.2. Get Query Responses Endpoint

**HTTP Method:** GET
**URL:** `/query/responses`

**Query Parameters:**

- `user_id` (optional): Filter responses by user ID.

**Response Body (Success):**

```json
[
  {
    "id": 12345,
    "query": "What is the capital of France?",
    "model": "text-davinci-003",
    "response": "Paris",
    "user_id": 1,
    "created_at": "2023-10-26T12:34:56.789Z",
    "updated_at": "2023-10-26T12:34:56.789Z"
  },
  // ... more query responses
]
```

**Response Body (Failure):**

```json
{
  "detail": "Error retrieving query responses: ..."
}
```

**Description:**

The `/query/responses` endpoint retrieves a list of query responses. You can optionally filter the responses by user ID using the `user_id` query parameter. The response body includes the ID, query, model, response, user ID, and timestamps for each query response.

#### 3.3. Get Query Response Endpoint

**HTTP Method:** GET
**URL:** `/query/responses/{query_id}`

**Response Body (Success):**

```json
{
  "id": 12345,
  "query": "What is the capital of France?",
  "model": "text-davinci-003",
  "response": "Paris",
  "user_id": 1,
  "created_at": "2023-10-26T12:34:56.789Z",
  "updated_at": "2023-10-26T12:34:56.789Z"
}
```

**Response Body (Failure):**

```json
{
  "detail": "Query response not found"
}
```

**Description:**

The `/query/responses/{query_id}` endpoint retrieves a specific query response by its ID. The response body includes the details of the query response.

### 4. Database Access (Internal Endpoints)

#### 4.1. Get Query Responses (Database Endpoint)

**HTTP Method:** GET
**URL:** `/db/query_responses`

**Query Parameters:**

- `user_id` (optional): Filter responses by user ID.

**Response Body (Success):**

```json
[
  {
    "id": 12345,
    "query": "What is the capital of France?",
    "model": "text-davinci-003",
    "response": "Paris",
    "user_id": 1,
    "created_at": "2023-10-26T12:34:56.789Z",
    "updated_at": "2023-10-26T12:34:56.789Z"
  },
  // ... more query responses
]
```

**Response Body (Failure):**

```json
{
  "detail": "Error retrieving query responses: ..."
}
```

**Description:**

This endpoint allows direct database access to retrieve a list of query responses. It is an internal endpoint used for testing and debugging purposes.

#### 4.2. Get Query Response (Database Endpoint)

**HTTP Method:** GET
**URL:** `/db/query_responses/{query_id}`

**Response Body (Success):**

```json
{
  "id": 12345,
  "query": "What is the capital of France?",
  "model": "text-davinci-003",
  "response": "Paris",
  "user_id": 1,
  "created_at": "2023-10-26T12:34:56.789Z",
  "updated_at": "2023-10-26T12:34:56.789Z"
}
```

**Response Body (Failure):**

```json
{
  "detail": "Query response not found"
}
```

**Description:**

This endpoint provides direct access to a specific query response by ID within the database. It is an internal endpoint intended for testing and debugging.

#### 4.3. Get Users (Database Endpoint)

**HTTP Method:** GET
**URL:** `/db/users`

**Response Body (Success):**

```json
[
  {
    "id": 1,
    "email": "user1@example.com",
    "created_at": "2023-10-26T12:34:56.789Z",
    "updated_at": "2023-10-26T12:34:56.789Z"
  },
  // ... more users
]
```

**Response Body (Failure):**

```json
{
  "detail": "Error retrieving users: ..."
}
```

**Description:**

This endpoint retrieves a list of all users stored in the database. It is an internal endpoint used for testing and debugging purposes.

#### 4.4. Get User (Database Endpoint)

**HTTP Method:** GET
**URL:** `/db/users/{user_id}`

**Response Body (Success):**

```json
{
  "id": 1,
  "email": "user1@example.com",
  "created_at": "2023-10-26T12:34:56.789Z",
  "updated_at": "2023-10-26T12:34:56.789Z"
}
```

**Response Body (Failure):**

```json
{
  "detail": "User not found"
}
```

**Description:**

This endpoint retrieves a specific user by ID from the database. It is an internal endpoint used for testing and debugging.

### 5. Error Handling

- **HTTP Status Codes:** The API uses standard HTTP status codes to indicate success or failure. For example:
  - `200 OK`: Success
  - `400 Bad Request`: Invalid request data
  - `401 Unauthorized`: Authentication required
  - `403 Forbidden`: Access denied
  - `404 Not Found`: Resource not found
  - `500 Internal Server Error`: Unexpected server error

- **Error Messages:**  The API returns error messages in the `detail` field of the JSON response. These messages provide information about the specific error that occurred.

### 6. Rate Limiting

To prevent abuse and ensure fair usage of the OpenAI API, the backend implements rate limiting. The exact rate limits may vary depending on the OpenAI API plan.

### 7. Security

- **Input Validation:** The API performs strict validation on all incoming data to prevent common security vulnerabilities like SQL injection and cross-site scripting (XSS).
- **Data Encryption:** Sensitive data, such as passwords, is stored in the database using secure hashing algorithms.
- **Authentication:** JWT-based authentication is used to secure protected API endpoints.

### 8. Future Enhancements

- **API Versioning:** The API can be versioned for backwards compatibility as new features are added.
- **More OpenAI Models:**  The API can be extended to support other OpenAI models and features.
- **Caching:** Caching mechanisms can be implemented to improve performance.

### 9. Developer Notes

- **Dependencies:** The backend uses the following packages:
  - `fastapi` (0.115.2)
  - `uvicorn` (0.32.0)
  - `openai` (1.52.0)
  - `pydantic` (2.9.2)
  - `python-multipart` (0.0.12)
  - `python-dotenv` (1.0.1)
  - `sqlalchemy` (2.0.36)
  - `psycopg2-binary` (2.9.10)
  - `PyJWT` (2.9.0)

- **Environment Variables:**
  - `OPENAI_API_KEY`: Your OpenAI API key.
  - `DATABASE_URL`: Your PostgreSQL database connection string.
  - `JWT_SECRET_KEY`: A secret key for JWT authentication.

- **Testing:**
  - The project includes a test suite for unit testing and integration testing.

- **Documentation:**
  - This API documentation is provided in the `api/src/docs/api_docs.md` file.

This API documentation provides a complete overview of the AI Query Response Backend MVP. For more detailed information, refer to the source code and test files within the repository.