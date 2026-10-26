# Text Adventure → 3D (iPad)

A single-file engine that turns a room/exit/item text adventure into a walkable 3D world, playable in Safari on iPad.

## Play
Open `game3d/index.html` over HTTPS (e.g. GitHub Pages), then Share → Add to Home Screen for full-screen.
Needs internet on first load (Three.js r128 comes from cdnjs).

- Left third of the screen: drag to walk (virtual joystick)
- Elsewhere: drag to look
- Tap an object to pick it up, tap a locked door to unlock it, tap an inventory item to examine it
- Desktop testing: WASD / arrow keys, mouse-drag to look, click to interact

## Converting your game
Edit the `GAME` object at the top of the script:

```js
rooms: {
  hall: { name, desc, color, exits: { north: "library" }, items: ["key"],
          locked: { north: "key" }, lockedText: "The door is locked." }
},
items: { key: { name, desc, color, shape: "box|sphere|cone|torus|cylinder" } },
win:   { room: "library", needs: ["key"], hint, text }
```

## Limits (by design, keep in mind)
- Only north/south/east/west exits. `up`/`down`/`in`/`out` are skipped with a warning on the start screen.
- Rooms are placed on a flat grid by following exits from the start room. Maps that don't fit a grid
  (e.g. "north then south leads somewhere else") get walled off, with a warning.
- Supported verbs: walk, take, unlock-with-key, examine. Anything else your text game does (talking to NPCs,
  combining items, puzzles beyond keys) needs code added to `interact()`.
