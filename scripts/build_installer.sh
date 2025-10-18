#!/usr/bin/env bash
set -e

APP_NAME="openstorm"
VERSION="0.1.0"
DIST_DIR="dist"
BUILD_DIR="../.build"

rm -rf "$BUILD_DIR" "$DIST_DIR"

echo "Building executable..."
pyinstaller --onefile ../openstorm/__main__.py \
            --name "$APP_NAME" \
            --distpath "$BUILD_DIR/dist" \
            --workpath "$BUILD_DIR/build" \
            --specpath "$BUILD_DIR/spec"

echo "Creating source archive..."
mkdir -p "$BUILD_DIR/$DIST_DIR"
tar -czf "$BUILD_DIR/$DIST_DIR/${APP_NAME}-${VERSION}.tar.gz" ../openstorm scripts README.md pyproject.toml

mv "$BUILD_DIR/dist/$APP_NAME" "$DIST_DIR/"

echo "Build completed. Files in $DIST_DIR:"
ls -l "$DIST_DIR"
