# Secret FC

Emblem for Secret FC, a futsal club.

<p align="center"><img src="logo/mockups/fabric-mockup.png" width="360" alt="Secret FC emblem on navy fabric"></p>

## The idea

A single-colour emblem in the style of a modern embroidered crest. The ball sits in the middle with a keyhole as its front panel. Swooshes wrap around it to show movement. One swoosh ends in a keyhole that breaks out of the ring. "SECRET FC" runs down the right side of the ring and "FUTSAL CLUB" sits along the bottom.

## Files

| File | Use it for |
| --- | --- |
| `logo/svg/secret-fc-emblem-cream.svg` | Main version, on navy or other dark colours |
| `logo/svg/secret-fc-emblem-navy.svg` | On cream, white or other light colours |
| `logo/svg/secret-fc-emblem-on-navy.svg` | Same as the cream one, with the navy square included (avatars, posts) |
| `logo/mockups/fabric-mockup.svg` | Emblem on a navy fabric texture |
| `logo/mockups/shirt.svg` | Navy shirt, front and back |

PNGs with transparent backgrounds are in `logo/png/`. Text is converted to outlines, so no font install is needed.

## Colours

| Name | Hex | Role |
| --- | --- | --- |
| Navy | `#101A2C` | Ground, shirts |
| Cream | `#EDE6D6` | Emblem and type |
| Gold | `#D8B26E` | Special editions |

The emblem is always one colour, which also makes it cheap to embroider or screen print.

## Type

[Saira Condensed](https://fonts.google.com/specimen/Saira+Condensed) ExtraBold (free, Google Fonts).

## Regenerating

```sh
pip install fonttools shapely
# put SairaCondensed-800.ttf from Google Fonts in tools/fonts/
cd tools
python3 build.py ../logo/svg
python3 kit.py ../logo/mockups/shirt.svg
```
