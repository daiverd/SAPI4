#!/bin/bash
# build_sapi4_docker.sh - One-shot SAPI4 build using Docker
set -euo pipefail

echo "Building SAPI4 applications with Docker..."

# Run the build in the container and exit
docker run --rm -it -v $(pwd):/work dockcross/windows-static-x86 bash -euo pipefail -c '

mkdir -p out

CXX="/usr/src/mxe/usr/bin/i686-w64-mingw32.static-g++"

CFLAGS="-O2 -D_WIN32_WINNT=0x0501 -static-libgcc -static-libstdc++ -I./sapi4_headers"
LIBS="-lole32 -luser32 -luuid -loleaut32"

echo "Building sapi4.dll..."
$CXX $CFLAGS -shared sapi4.cpp $LIBS -Wl,--out-implib,out/libsapi4.a -o out/sapi4.dll

echo "Building sapi4out.exe..."
$CXX $CFLAGS sapi4out.cpp $LIBS -L./out -lsapi4 -o out/sapi4out.exe

echo "Building sapi4limits.exe..."
$CXX $CFLAGS sapi4limits.cpp $LIBS -L./out -lsapi4 -o out/sapi4limits.exe

rm out/libsapi4.a
'

echo "Done. Output:"
ls -la out/*.{dll,exe} 2>/dev/null || exit 1