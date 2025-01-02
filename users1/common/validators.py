#common/validators.py
import json

# Unpacks data from request based on HTTP method
def unpack_data(request):
    if request.method == 'POST':
        # For POST requests, parse JSON from request body
        data = json.loads(request.body)
    elif request.method == 'GET':
        # For GET requests, use query parameters
        data = request.GET
    else:
        # For other request methods, return empty dict
        data = {}
    return data

# Checks for missing required fields in the data
def missing_required_fields(data, required_fields):
    missing_fields = []
    # Loop through required fields and check if each exists in data
    for field in required_fields:
        if field not in data:
            missing_fields.append(field)
    return missing_fields