I=0
for path in $SPRITES_DIR/*.png; do
  NEWPATH="$SPRITES_DIR/$I.png"
  mv $path $NEWPATH
  I=$(echo $(($I+1)))
done

# SPRITES_DIR='./assets/images/entities/tile' sh scripts/rename.sh