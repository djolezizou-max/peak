#!/bin/bash

# Check if prompt argument is provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 \"Image prompt\" \"Output filename\""
    echo "Example: $0 \"A person doing high-intensity interval training, photorealistic\" \"hiit-basics.jpg\""
    exit 1
fi

# Get the prompt and filename from arguments
PROMPT="$1"
FILENAME="$2"
SIZE="1024x1024"  # Standard size, adjust as needed
OUTPUT_DIR="assets/blog"

# Make sure output directory exists
mkdir -p "$OUTPUT_DIR"

echo "Generating image from prompt: $PROMPT"
echo "This will be saved as: $OUTPUT_DIR/$FILENAME"

# Save API response to a file for debugging
TEMP_RESPONSE="/tmp/openai_response.json"

# Call OpenAI API with gpt-image-1 model parameters
# Note: If your organization isn't verified for gpt-image-1, DALL-E 3 will be used as fallback
curl -s https://api.openai.com/v1/images/generations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d "{
    \"model\": \"gpt-image-1\",
    \"prompt\": \"$PROMPT\",
    \"n\": 1,
    \"size\": \"$SIZE\"
  }" > $TEMP_RESPONSE

echo "API Response received"

# Extract the URL using Python for more reliable JSON parsing
if command -v python3 &>/dev/null; then
    IMAGE_URL=$(python3 -c "
import json
with open('$TEMP_RESPONSE', 'r') as f:
    data = json.load(f)
    if 'data' in data and len(data['data']) > 0 and 'url' in data['data'][0]:
        print(data['data'][0]['url'])
    elif 'data' in data and len(data['data']) > 0 and 'b64_json' in data['data'][0]:
        # Handle base64 encoded images if present
        print('BASE64_ENCODED')
    else:
        print('')
" 2>/dev/null)
else
    # Fallback to grep if Python is not available
    IMAGE_URL=$(grep -o '"url":"https://[^"]*"' $TEMP_RESPONSE | sed 's/"url":"//;s/"$//')
fi

# Check if URL was successfully extracted
if [ -z "$IMAGE_URL" ]; then
    echo "Error: Failed to get image URL from API response."
    echo "API response:"
    cat $TEMP_RESPONSE
    rm $TEMP_RESPONSE
    exit 1
fi

# If we got a BASE64_ENCODED response, handle it differently
if [ "$IMAGE_URL" = "BASE64_ENCODED" ]; then
    echo "Image is base64 encoded, extracting..."
    python3 -c "
import json, base64
with open('$TEMP_RESPONSE', 'r') as f:
    data = json.load(f)
    if 'data' in data and len(data['data']) > 0 and 'b64_json' in data['data'][0]:
        b64_data = data['data'][0]['b64_json']
        image_data = base64.b64decode(b64_data)
        with open('$OUTPUT_DIR/$FILENAME', 'wb') as img_file:
            img_file.write(image_data)
" 2>/dev/null
else
    echo "Image URL extracted - first 50 chars: ${IMAGE_URL:0:50}..."
    # Download the image using curl
    curl -s "$IMAGE_URL" -o "$OUTPUT_DIR/$FILENAME"
fi

# Check if the file was created and has content
if [ -f "$OUTPUT_DIR/$FILENAME" ] && [ -s "$OUTPUT_DIR/$FILENAME" ]; then
    echo "Image successfully downloaded and saved to $OUTPUT_DIR/$FILENAME"
    echo "File size: $(du -h "$OUTPUT_DIR/$FILENAME" | cut -f1)"
    echo "Now you can use this path in your blog post front matter:"
    echo "featured_image: \"/$OUTPUT_DIR/$FILENAME\""
else
    echo "Error: Failed to download the image or the file is empty."
    exit 1
fi

# Clean up
rm $TEMP_RESPONSE 