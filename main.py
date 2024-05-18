from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from openai import OpenAI
import os
import json
import logging

app = FastAPI()

# Configure OpenAI API key
client = OpenAI(api_key="XXX")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def save_response(response):
    # Define the human-readable filename and JSON filename
    human_readable_filename = 'response_human_readable.txt'
    json_filename = 'response.json'

    # Extract the human-readable part and the JSON part from the response
    human_readable_part = response.split('```json')[0].strip()
    json_part = response.split('```json')[1].strip().strip('```')

    # Save the human-readable part to the file
    with open(human_readable_filename, 'w') as human_file:
        human_file.write(human_readable_part)

    # Parse the JSON part and save it to the file
    json_data = json.loads(json_part)
    with open(json_filename, 'w') as json_file:
        json.dump(json_data, json_file, indent=2)

    print(f'Successfully saved to {human_readable_filename} and {json_filename}')


@app.post("/schema/csv")
async def get_csv_schema(file: UploadFile = File(...), dev_mode: bool = Form(False)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Unsupported file type")

    if dev_mode:
        dummy_response = {
            "openai_response": json.dumps({
                "schema": {
                    "columns": ["col1", "col2", "col3"],
                    "dtypes": {"col1": "int", "col2": "float", "col3": "object"}
                },
                "rdf_representation": "<rdf>dummy rdf data</rdf>"
            }, indent=2)
        }
        return JSONResponse(content=dummy_response)

    file_content = await file.read()

    # Create instructions for OpenAI API
    instructions = (
        "Please analyze the following CSV data and provide the best possible data schema if necessary with hirachies and its RDF representation:\n\n"
        f"CSV Data:\n{file_content.decode('utf-8')}\n\n"
        "Return the schema and RDF representation in JSON format. Do not ask questions after."
    )

    # Send the CSV content to OpenAI API
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": instructions}
        ],
        max_tokens=1500
    )
    logger.info(f"CSV Schema Response (dev mode): {response}")
    openai_response = response.choices[0].message.content
    save_response(openai_response)
    return JSONResponse(content={"openai_response": openai_response})

@app.post("/schema/tab")
async def get_tab_schema(file: UploadFile = File(...), dev_mode: bool = Form(False)):
    logger.info(f"TAB Schema Response: ho")
    if not file.filename.endswith('.tab'):
        raise HTTPException(status_code=400, detail="Unsupported file type")

    if dev_mode:
        dummy_response = {
            "openai_response": json.dumps({
                "schema": {
                    "columns": ["col1", "col2", "col3"],
                    "dtypes": {"col1": "int", "col2": "float", "col3": "object"}
                },
                "rdf_representation": "<rdf>dummy rdf data</rdf>"
            }, indent=2)
        }
        return JSONResponse(content=dummy_response)

    file_content = await file.read()

    # Create instructions for OpenAI API
    instructions = (
        "Please analyze the following TAB data and provide the best possible data schema if necessary with hirachies  and its RDF representation:\n\n"
        f"TAB Data:\n{file_content.decode('utf-8')}\n\n"
        "Return the schema and RDF representation in JSON format. Do not ask questions after."
    )

    # Send the TAB content to OpenAI API
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": instructions}
        ],
        max_tokens=1500
    )
    logger.info(f"TAB Schema Response: {response}")
    openai_response = response.choices[0].message.content
    save_response(openai_response)
    return JSONResponse(content={"openai_response": openai_response})

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8010)
