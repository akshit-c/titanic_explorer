# TailorTalk Troubleshooting Guide

This guide provides solutions to common issues you might encounter when running the TailorTalk application.

## API Key Issues

### OpenRouter API Authentication Error

If you see an error like this in your logs:
```
ValueError: Error from OpenRouter API: {"error":{"message":"No auth credentials found","code":401}}
```

**Solution:**
1. Sign up for an account at [OpenRouter](https://openrouter.ai/)
2. Generate an API key from your account dashboard
3. Open the `.env` file in the root directory of the project
4. Replace the placeholder value for `OPENROUTER_API_KEY` with your actual API key:
   ```
   OPENROUTER_API_KEY=your_actual_api_key_here
   ```
5. Restart the application using `python run.py`

## Connection Issues

### Port Already in Use

If you see an error like this:
```
Error: Address already in use
```

**Solution:**
1. Find the process using the port:
   ```
   lsof -i :<port_number>
   ```
2. Kill the process:
   ```
   kill -9 <PID>
   ```
3. Try starting the application again

### Frontend Not Accessible

If the frontend is not accessible at http://localhost:8502:

**Solution:**
1. Check if the Streamlit server is running:
   ```
   ps aux | grep streamlit
   ```
2. If not running, start it manually:
   ```
   cd frontend && streamlit run app.py
   ```
3. If running but not accessible, check for firewall issues or try a different port by modifying the `FRONTEND_PORT` in the `.env` file

### Backend Not Accessible

If the backend is not accessible at http://localhost:8000:

**Solution:**
1. Check if the backend server is running:
   ```
   ps aux | grep "python app/main.py"
   ```
2. If not running, start it manually:
   ```
   cd app && python main.py
   ```
3. If running but not accessible, check for firewall issues or try a different port by modifying the `API_PORT` in the `.env` file

## Application Errors

### Internal Server Error (500)

If you receive a 500 Internal Server Error when making API requests:

**Solution:**
1. Check the server logs for detailed error messages
2. Verify that all required environment variables are set correctly in the `.env` file
3. Ensure the database is properly initialized:
   ```
   cd app && python -c "from db.database import init_db; init_db()"
   ```

### Pydantic Warnings

If you see warnings about Pydantic configuration changes:

**Solution:**
These are warnings, not errors, and can be safely ignored. They indicate that the codebase is using older Pydantic syntax that will be deprecated in future versions.

## Data Issues

### Titanic Dataset Not Found

If the application cannot find the Titanic dataset:

**Solution:**
1. Verify that the dataset exists at the path specified in the `.env` file (`TITANIC_DATASET_PATH`)
2. If the file is missing, download it from the original source or restore it from a backup

## Still Having Issues?

If you're still experiencing problems after trying these solutions:

1. Check the application logs for more detailed error messages
2. Try running the backend and frontend separately to isolate the issue
3. Verify that all dependencies are installed correctly:
   ```
   pip install -r requirements.txt
   ```
4. Make sure your Python version is compatible (Python 3.9+ recommended)
5. If all else fails, try restarting your computer and then running the application again 