#!/bin/bash

# Docker Multi-Platform Build Script für ContentClip Service

set -e

# Konfiguration
IMAGE_NAME="contentclip-service"
VERSION="1.0.0"
PLATFORMS="linux/amd64,linux/arm64"

echo "🐳 Building multi-platform Docker image..."
echo "Image: ${IMAGE_NAME}:${VERSION}"
echo "Platforms: ${PLATFORMS}"
echo ""

# Prüfe ob buildx verfügbar ist
if ! docker buildx version &> /dev/null; then
    echo "❌ Docker Buildx ist nicht verfügbar"
    echo "Bitte aktualisiere Docker auf eine neuere Version"
    exit 1
fi

# Erstelle Builder falls nicht vorhanden
if ! docker buildx inspect multiplatform-builder &> /dev/null; then
    echo "📦 Erstelle neuen buildx Builder..."
    docker buildx create --name multiplatform-builder --use
    docker buildx inspect --bootstrap
else
    echo "✅ Builder 'multiplatform-builder' existiert bereits"
    docker buildx use multiplatform-builder
fi

# Build und Push (oder nur Build mit --load für lokalen Test)
echo ""
echo "🔨 Starte Build..."
docker buildx build \
    --platform ${PLATFORMS} \
    --tag ${IMAGE_NAME}:${VERSION} \
    --tag ${IMAGE_NAME}:latest \
    --file dockerfile \
    --load \
    .

echo ""
echo "✅ Build erfolgreich abgeschlossen!"
echo ""
echo "Nächste Schritte:"
echo "  Container starten: docker run -d -p 8000:8000 --name contentclip ${IMAGE_NAME}:latest"
echo "  Logs anzeigen:     docker logs -f contentclip"
echo ""
echo "Für Registry Push:"
echo "  docker buildx build --platform ${PLATFORMS} --tag YOUR_REGISTRY/${IMAGE_NAME}:${VERSION} --push ."
