echo "Updating $CONFIG"
git -C "$CONFIG" pull

echo "Updating $SCRIPTS"
git -C "$SCRIPTS" pull --recurse-submodules
