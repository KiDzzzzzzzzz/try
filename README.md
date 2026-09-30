# 1 Secret FC

Logo set for 1 Secret FC, a futsal club.

<p align="center"><img src="logo/png/1-secret-fc-stacked.png" width="260" alt="1 Secret FC stacked logo"></p>

## The idea

A plain black disc for the ball, with a number 1 cut out of it. The cut runs off the bottom edge of the disc, so it also looks like the slot of a keyhole. That covers the ball, the 1 and the secret in one shape, with nothing else added.

## Files

| File | Use it for |
| --- | --- |
| `logo/svg/1-secret-fc-mark.svg` | The mark on its own. Shirts, stickers, small spaces |
| `logo/svg/1-secret-fc-mark-white.svg` | The mark on dark backgrounds and photos |
| `logo/svg/1-secret-fc-mark-red.svg` | Accent version, use sparingly |
| `logo/svg/1-secret-fc-stacked.svg` (+ `-white`) | Mark above the name. Posters, square formats |
| `logo/svg/1-secret-fc-lockup.svg` (+ `-white`) | Mark beside the name. Headers, banners, letterheads |
| `logo/svg/1-secret-fc-icon.svg` (+ `-red`) | Social avatars, app icons, favicons |
| `logo/mockups/home-kit.svg` | Home shirt, front and back |

Every SVG has a transparent PNG in `logo/png/`. Text is converted to outlines, so no font install is needed.

## Colours

| Name | Hex | Role |
| --- | --- | --- |
| Ink | `#111111` | Mark and type |
| Bone | `#EFEBE3` | Background |
| Signal red | `#D9442B` | Only accent. Use it on one thing at a time |

## Type

[Instrument Sans](https://fonts.google.com/specimen/Instrument+Sans) (free, Google Fonts). Bold with wide letter spacing (about 0.3em) for the name, Medium for "FUTSAL CLUB".

## Using it

- Keep plenty of empty space around the mark, at least half the disc's width.
- Use one colour at a time. Don't add outlines, shadows or gradients.
- Don't put the name inside the disc or change the angle of the 1.

## Regenerating

The files are drawn by the scripts in `tools/` (Python, with `fonttools` and `shapely`):

```sh
pip install fonttools shapely
# put InstrumentSans-700.ttf and InstrumentSans-500.ttf from Google Fonts in tools/fonts/
cd tools
python3 build.py ../logo/svg
python3 kit.py ../logo/mockups/home-kit.svg
```
