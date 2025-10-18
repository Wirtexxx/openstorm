#!/usr/bin/env bash
set -e

APP_NAME="openstorm"
VERSION="0.1.0"
DIST_DIR="dist"
BUILD_DIR="../.build"

rm -rf "$BUILD_DIR" "$DIST_DIR"

echo "Building executable..."
source ../.venv/bin/activate

# build with pyinstaller
pyinstaller --onefile -m ../openstorm \
            --name "$APP_NAME" \
            --distpath "$BUILD_DIR/dist" \
            --workpath "$BUILD_DIR/build" \
            --specpath "$BUILD_DIR/spec" \
            --hidden-import=typer \
            --hidden-import=pydantic_settings \
            --hidden-import=pymongo \
            --hidden-import=pymongo.errors \
            --hidden-import=rich \
            --hidden-import=rich.markup

#mkdir -p "$DIST_DIR"
#
#mv "$BUILD_DIR/dist/$APP_NAME" "$DIST_DIR/"

mkdir -p "$BUILD_DIR/$DIST_DIR"
tar -czf "$BUILD_DIR/$DIST_DIR/${APP_NAME}-${VERSION}.tar.gz" \
    -C .. openstorm scripts README.md pyproject.toml

echo "Build completed. Files in $DIST_DIR:"
ls -l "$DIST_DIR"
