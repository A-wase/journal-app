import base64

# Input and output file paths
input_path = "REPLACE"
output_path = r"C:\Users\YOURNAME\folder\decoded_backup.json"

# Read and decode Base64 (the magic)
with open(input_path, "r", encoding="utf-8") as file:
    encoded_data = file.read()

decoded_bytes = base64.b64decode(encoded_data)

# Save the decoded result
with open(output_path, "wb") as out_file:
    out_file.write(decoded_bytes)

print("Decoded file saved to:", output_path)
