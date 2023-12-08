import json
from lambda_function import lambda_handler

# Simulate AWS Event
sample_event = {
    "key1": "value1",
    "key2": "value2",
    "key3": "value3"
}

# Call the Lambda handler function
result = lambda_handler(sample_event, None)

# Print the result
print(json.dumps(result, indent=2))
