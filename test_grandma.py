"""Tests for Grandma's Famous Whatever (index.html).

Static checks always run. When Node.js is installed, the game rules (the <script id="logic">
block, which has no DOM) also run: a perfect run must score 5 of 5, a literal-minded run must
score badly, every score must stay in range and peak inside its band, and every cue (the dog's
sneeze, the cardigan colour, the cat at the window) must line up with the score it hints at.
"""
import json
import os
import re
import shutil
import subprocess
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "index.html"), encoding="utf-8") as f:
    HTML = f.read()
LOGIC = re.search(r'<script id="logic">(.*?)</script>', HTML, re.S).group(1)
MAIN = re.search(r'<script>\s*"use strict";(.*?)</script>', HTML, re.S).group(1)

HARNESS = """
;(function(){
  const problems=selfTestLogic();
  console.log(JSON.stringify({version:VERSION,problems:problems.slice(0,25)}));
  process.exitCode=problems.length?1:0;
})();
"""


class Static(unittest.TestCase):
    def test_single_self_contained_file(self):
        # itch.io plays one HTML file: no external scripts, styles, fonts or images
        self.assertNotRegex(HTML, r'<script[^>]+src=')
        self.assertNotRegex(HTML, r'<link[^>]+stylesheet')
        self.assertNotRegex(HTML, r'(src|href)="https?://')
        self.assertNotIn("import(", HTML)
        self.assertNotIn("fetch(", HTML)

    def test_logic_is_separate(self):
        # code use of the DOM, not the words: the game text says "...at the window. The smoke..."
        # so a property access must be a dot followed by a name, or a bracket
        for api in (r"\bdocument(\.[A-Za-z_$]|\[)", r"\bwindow(\.[A-Za-z_$]|\[)", r"\bctx\.[A-Za-z_$]",
                    r"\blocalStorage\.[A-Za-z_$]", r"\bperformance\.[A-Za-z_$]"):
            self.assertNotRegex(LOGIC, api)
        self.assertIn("selfTestLogic", MAIN)
        self.assertIn('location.hash==="#selftest"', MAIN)

    def test_credit_bar_does_not_block_clicks(self):
        # the bar overlaps the bottom of the canvas on short windows, where the DONE button sits
        self.assertRegex(HTML, r"#credit\{[^}]*pointer-events:none")
        y = int(re.search(r"LABELS\[STEPS\[step\]\],210,(\d+)", MAIN).group(1))
        self.assertLessEqual(y, 565)

    def test_every_step_has_said_and_meant(self):
        steps = json.loads(re.search(r"const STEPS=(\[[^\]]+\])", LOGIC).group(1))
        self.assertEqual(steps, ["flour", "salt", "stir", "oven", "bake"])
        for k in steps:
            self.assertRegex(LOGIC, r"\n  %s:\"[^\"]+\"" % k)
            self.assertIn("upd" + k.capitalize(), MAIN)

    def test_jam_rules(self):
        # The WORST Game Jam: disclose what was AI-made; no flashing lights; nothing harmful
        self.assertIn("Made by MV2 of Munim, Inc. with AI agents", HTML)
        self.assertIn("code, art and sound are all AI-made", HTML)
        self.assertIn("No flashing lights", HTML)
        self.assertIn("Grandma's Instructions", HTML)
        for bad in ("localStorage.clear", "indexedDB", "Notification", "requestFullscreen", "alert(", "confirm("):
            self.assertNotIn(bad, HTML)

    def test_sound_can_be_turned_off_and_stays_quiet(self):
        self.assertIn('id="snd"', HTML)
        self.assertIn("Snd.setOn(!Snd.on)", MAIN)
        self.assertIn("document.hidden", MAIN)
        self.assertRegex(MAIN, r"master\.gain\.value=this\.on\?0\.5:0")
        for vol in re.findall(r"exponentialRampToValueAtTime\((0\.\d+),", MAIN):
            self.assertLessEqual(float(vol), 0.1)

    def test_keyboard_fallbacks(self):
        for key in ('keys[" "]', "pressed.s", "keys.ArrowLeft", "pressed.ArrowRight", "pressed.Enter"):
            self.assertIn(key, MAIN)

    def test_licence_and_wording(self):
        self.assertIn("Apache-2.0", HTML)
        self.assertNotRegex(HTML, r"\bMIT\b")
        self.assertIsNone(re.search(r"MV2[^.]{0,60}\b(an AI|a bot|AI assistant)\b", HTML))


@unittest.skipUnless(shutil.which("node"), "Node.js is not installed")
class Logic(unittest.TestCase):
    def test_rules(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "grandma_logic.js")
            with open(path, "w", encoding="utf-8") as f:
                f.write(LOGIC + "\n" + HARNESS)
            out = subprocess.run(["node", path], capture_output=True, text=True, encoding="utf-8", timeout=120)
        self.assertEqual(out.returncode, 0, out.stdout[-4000:] + out.stderr[-4000:])
        report = json.loads(out.stdout[out.stdout.index("{"):])
        self.assertEqual(report["problems"], [])

    def test_main_script_parses(self):
        # catches syntax errors in the browser-only script without running it
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "grandma_main.js")
            with open(path, "w", encoding="utf-8") as f:
                f.write('"use strict";' + MAIN)
            out = subprocess.run(["node", "--check", path], capture_output=True, text=True, encoding="utf-8", timeout=60)
        self.assertEqual(out.returncode, 0, out.stderr[-4000:])


if __name__ == "__main__":
    unittest.main()
