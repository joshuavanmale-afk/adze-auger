# Ingrid 3D

Your Twine story *Ingrid* (Harlowe 3), played as a 3D scene on iPad. The story text and choices are unchanged.
Each passage is staged in one of ten low-poly 3D locations with the right characters present.

- `index.html`: the game. Host it over HTTPS (e.g. GitHub Pages), open in Safari, then Share → Add to Home Screen.
  Needs internet on first load (Three.js comes from cdnjs).
- `template.html`: the player and the 3D scenes. Edit this, not `index.html`.
- `build.py`: rebuilds `index.html` from your Twine file. It also reports broken links and passages nobody can reach.

```
python3 ingrid3d/build.py path/to/Ingrid.html
```

## Editing the story
Keep writing in Twine, publish to file, re-run `build.py`. New passages are placed in a scene guessed from their name.
To place them yourself, add a line to `STAGING` in `template.html`:

```js
"My new passage": ["forest", ["mother", "ladyUp"]],
```

## What it supports
`[[links]]` (`->`, `<-`, `|`), `(link: "…")[hook]`, `(set: $x to …)`, `(if:)`/`(unless:)` on hooks and links
(`$x`, `$x is …`, `$x is not …`), `''bold''`, `//italic//`. That is everything *Ingrid V1* uses. Other Harlowe macros
are skipped and listed in the browser console, so check there if you start using things like `(either:)` or `(display:)`.

## Controls
Drag the scene to look around. Choices are buttons in the text panel. When a choice refers to something in the scene
(the window, the orange, the rifle, the father…), a pulsing marker appears on it. Tapping a marker runs harmless "find out more" links straight away; for real story choices it highlights the matching buttons, so a stray tap never commits you to anything.
Progress is saved on the device; the title screen offers to continue.
