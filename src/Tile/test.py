import Tileset
from PIL import Image

t = Tileset.Tileset(Image.open("tileset.png"), 64, 64)

t.generateTileset()





