# escape-room-ai

## How to run

1. Create a virtual environment and activate it (Linux) Optional
```
python3 -m venv venv
source venv/bin/activate
```
2. Install the requirements
```
pip install -r requirements.txt
```
3. Create .env file using .env.example as a template

4. Run the program
```
python -m uvicorn app.main:app --reload
```


## License

This project is licensed under the terms of the MIT license.
