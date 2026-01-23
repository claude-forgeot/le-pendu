#!/bin/bash

# Script to convert all MP3 files to OGG format
# Usage: bash convert_audio_to_ogg.sh

echo "Converting MP3 files to OGG format..."
echo ""

# Check if ffmpeg is installed
if ! command -v ffmpeg &> /dev/null; then
    echo "Error: ffmpeg is not installed"
    echo "Please install it with: sudo apt install ffmpeg"
    exit 1
fi

# Navigate to assets/audios directory
cd assets/audios || exit 1

# Convert each MP3 file to OGG
for file in *.mp3; do
    if [ -f "$file" ]; then
        output="${file%.mp3}.ogg"
        echo "Converting: $file -> $output"

        # Convert with good quality (q:a 5 = ~160kbps)
        ffmpeg -i "$file" -acodec libvorbis -q:a 5 "$output" -y 2>&1 | grep -v "^frame=" | grep -v "^size="

        if [ $? -eq 0 ]; then
            echo "✓ Successfully converted $file"
        else
            echo "✗ Failed to convert $file"
        fi
        echo ""
    fi
done

echo "Conversion complete!"
echo ""
echo "OGG files created in assets/audios/"
ls -lh *.ogg 2>/dev/null || echo "No OGG files found"
