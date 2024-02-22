VENV_PATH="${VENV_PATH:-venv}"
BUILD_PATH=./build
DIST_PATH=./dist
GAME_SPEC_PATH=./game.spec

VENV_PATH=$VENV_PATH sh ./scripts/install.sh

rm -rf $BUILD_PATH $DIST_PATH $GAME_SPEC_PATH

if [[ -n "$ONEFILE" ]]; then
  echo "Y" | "./$VENV_PATH/Scripts/python.exe" -m PyInstaller ./game.py --noconsole --onefile --icon="assets/images/icon.ico"
  cp -r ./assets $DIST_PATH
  mv $DIST_PATH/game.exe "$DIST_PATH/Smash Ninja.exe"
else
  echo "Y" | "./$VENV_PATH/Scripts/python.exe" -m PyInstaller ./game.py --icon="./assets/images/icon.ico" --noconsole 
  cp -r ./assets $DIST_PATH/game
  # mv $DIST_PATH/game/game.exe "$DIST_PATH/game/Smash Ninja.exe"
fi
