#!/bin/bash
# build_sapi4_docker.sh - One-shot SAPI4 build using Docker

echo "Building SAPI4 applications with Docker..."

# Run the build in the container and exit
docker run --rm -it -v $(pwd):/work dockcross/windows-static-x86 bash -c '

mkdir -p out

CXX="/usr/src/mxe/usr/bin/i686-w64-mingw32.static-g++"

# Common flags
CFLAGS="-O2 -D_WIN32_WINNT=0x0501 -static-libgcc -static-libstdc++ -I./sapi4_headers"
# Add more COM/OLE libraries
LIBS="-lole32 -luser32 -luuid -loleaut32"

echo "Building SAPI4 applications..."

# Build sapi4.dll (shared library) - also create import library
echo "Building sapi4.dll..."
$CXX $CFLAGS -shared sapi4.cpp $LIBS -Wl,--out-implib,out/libsapi4.a -o out/sapi4.dll
if [ $? -eq 0 ]; then
    echo "✓ sapi4.dll built successfully"
else
    echo "✗ Failed to build sapi4.dll"
    exit 1
fi

# Build sapi4out.exe
echo "Building sapi4out.exe..."
$CXX $CFLAGS sapi4out.cpp $LIBS -L./out -lsapi4 -o out/sapi4out.exe
if [ $? -eq 0 ]; then
    echo "✓ sapi4out.exe built successfully"
else
    echo "✗ Failed to build sapi4out.exe"
fi

# Build sapi4limits.exe  
echo "Building sapi4limits.exe..."
$CXX $CFLAGS sapi4limits.cpp $LIBS -L./out -lsapi4 -o out/sapi4limits.exe
if [ $? -eq 0 ]; then
    echo "✓ sapi4limits.exe built successfully"
else
    echo "✗ Failed to build sapi4limits.exe"
fi

echo "Build completed!"

rm out/libsapi4.a
'

# Check if build was successful
if [ $? -eq 0 ]; then
    echo ""
    echo "Build completed! Files ready for Windows XP:"
    ls -la out/sapi4.dll out/sapi4out.exe out/sapi4limits.exe 2>/dev/null
else
    echo "Build failed!"
    exit 1
fi