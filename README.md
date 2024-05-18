# CSV Schema API

This is a simple Flask API with Swagger integration that takes a CSV file and returns the data schema (column names and data types).

## Installation

1. Clone the repository or download the script.
2. Navigate to the directory containing `app.py`.
3. Create a directory named `static` in the same directory as `app.py`.
4. Install the required packages:

    ```bash
    pip install Flask Flask-RESTful flask-swagger-ui pandas
    ```

## Usage

1. Run the Flask application:

    ```bash
    python app.py
    ```

2. Open your browser and go to `http://127.0.0.1:5000/swagger` to access the Swagger UI.

3. Use the Swagger UI to upload a CSV file and get back its schema.

## API Endpoints

### POST /schema

#### Description

Upload a CSV file and get its schema (column names and data types).

#### Parameters

- `file`: (required) The CSV file to upload.

#### Responses

- `200 OK`: Returns the schema of the CSV file.
  - `columns`: List of column names.
  - `dtypes`: Dictionary of column data types.
- `400 Bad Request`: Returns an error message if the file is not provided or is of an unsupported type.

## Example Request

```bash
curl -X POST "http://127.0.0.1:5000/schema" -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "file=@yourfile.csv"
