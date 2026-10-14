# Grandma's Famous Whatever

A tiny, deliberately terrible browser game for [The WORST Game Jam](https://itch.io/jam/your-worst-ideas)
(October 2026, theme: **Grandma's Instructions**). By MV2 of Munim, Inc.

Grandma left you her famous recipe. She didn't say what it is. She didn't say how much of anything.
Five steps, about two minutes, then she tastes it.

| Step | Grandma says | You have to work out |
|------|--------------|----------------------|
| Flour | "Not too much, not too little. You'll know." | how you'd know |
| Salt | "A pinch. MY pinch." | how big her pinch is |
| Stir | "Till it looks right. The other way." | looks like what, and the other way from what |
| Oven | "A nice temperature." | why "Nice" on her oven isn't nice |
| Bake | "Take it out when it's done. You'll smell it." | how you smell through a screen |

Every instruction has a fair clue somewhere in the kitchen. Some of her advice makes things worse if
you follow it. At the end, Grandma scores you out of five hearts, tells you what you actually made,
and explains what she meant for every step you got wrong.

## Bad on purpose

Made for a jam that rewards Worst Controls, Ugliest Art, Worst Sound and Creative Badness:

- Your cursor is an oven mitt that lags behind the mouse and sits a bit to the right. While stirring
  it is mirrored. The oven dial turns the wrong way and keeps spinning.
- The art wobbles, the wallpaper is mustard and teal, and everything is in Comic Sans.
- The music is an off-key kazoo, Grandma speaks in beeps, and the smoke alarm sings along.

Harmless on purpose too: no flashing lights, the sound is quiet with an on/off button (or **M**), and
nothing touches your files.

## Play

Open `index.html` in a browser. It is one self-contained file with no downloads. Keys if the mitt is
too much: **Space** pour, **S** shake, **arrow keys** stir and turn the dial, **Enter** "Done, Grandma".

`index.html#selftest` runs the built-in rule checks. `python -m unittest -v` runs the same checks
under Node.js (if installed) plus static checks: a single self-contained file, the jam's AI
disclosure, quiet sound, keyboard fallbacks and a credit bar that never blocks clicks.

## Versions

- 1.0.1: the credit bar at the bottom no longer catches clicks meant for the game (it could cover
  the bottom of the "Done, Grandma" button on short windows), and the step label sits above it.
- 1.0: first version.

## Made with AI

Made by MV2 of Munim, Inc. with AI agents (Anthropic Claude): the code, art and sound are all
AI-made. The art is drawn by code and the sound is synthesized in the browser; there are no premade
assets. Written from scratch during the jam, starting 14 October 2026.

## Licence

Apache-2.0. See `LICENSE`.
