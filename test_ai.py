from ai_generator import generate_manual

test_details = """
Machine Name: Electric Water Pump
Manufacturer: Not provided
Model Number: Not provided
"""

try:
    result = generate_manual(test_details)

    print("\n        MECHATLAS DETAILED MANUAL      \n")
    print(result)

except Exception as error:
    print("Error:", error)