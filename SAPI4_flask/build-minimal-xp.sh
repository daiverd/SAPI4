#!/bin/bash
# Build minimal Windows XP compatible executable
# This version excludes problematic modules for better XP compatibility

set -e

echo "Building minimal SAPI4 Flask executable for Windows XP compatibility..."

# Check if SAPI4 files exist
SAPI4_FILES=("sapi4out.exe" "sapi4limits.exe" "sapi4.dll")
for file in "${SAPI4_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        echo "ERROR: Missing required file: $file"
        echo "Please ensure all SAPI4 files are in the current directory"
        exit 1
    fi
done

# Create dist directory
mkdir -p dist

echo "Building with minimal dependencies for maximum XP compatibility..."
docker run --rm \
    -v "$(pwd):/src/" \
    cdrx/pyinstaller-windows:python2 \
    "pyinstaller --onefile sapi4_flask_minimal.spec"

# Check if build was successful
if [ -f "dist/sapi4_flask_minimal.exe" ]; then
    echo ""
    echo "✓ Minimal XP build successful!"
    echo "✓ Executable: dist/sapi4_flask_minimal.exe"
    echo "✓ Size: $(du -h dist/sapi4_flask_minimal.exe | cut -f1)"
    echo ""
    echo "This build excludes modules that may cause XP compatibility issues:"
    echo "- SSL/TLS modules"
    echo "- Threading and async modules" 
    echo "- XML parsing modules"
    echo "- Network modules beyond basic HTTP"
    echo ""
    echo "To test on Windows XP:"
    echo "1. Copy dist/sapi4_flask_minimal.exe to XP machine"
    echo "2. Run the executable"
    echo "3. Access http://localhost:23451 in browser"
else
    echo "✗ Build failed!"
    exit 1
fi