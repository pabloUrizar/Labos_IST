import json
from lambda_function import lambda_handler

# Simulate an event, you can adjust this based on your actual event structure
sample_event = {
    "key1": "value1",
    "key2": "value2",
    "key3": "value3"
}

# Call the Lambda handler function
result = lambda_handler(sample_event, None)

# Print the result (you can customize this based on your expected return format)
print(json.dumps(result, indent=2))

