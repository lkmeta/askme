import uvicorn

# Entry point to start the FastAPI server
if __name__ == "__main__":
    # Use Uvicorn to run the FastAPI application
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
