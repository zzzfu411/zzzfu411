"""Make the generated statistics readable without an animation engine."""

from pathlib import Path
import sys
import xml.etree.ElementTree as ET

SVG = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG)
directory = Path(sys.argv[1])
names = ("stats-light", "stats-dark", "languages-light", "languages-dark")
cards = [(directory / f"{name}.svg", ET.parse(directory / f"{name}.svg")) for name in names]
height = max(float(tree.getroot().get("height")) for _, tree in cards)

for path, tree in cards:
    root = tree.getroot()
    width = float(root.get("width"))
    root.set("height", f"{height:g}")
    root.set("viewBox", f"0 0 {width:g} {height:g}")
    style = ET.SubElement(root, f"{{{SVG}}}style")
    style.text = """
      * { animation: none !important; }
      .stagger { opacity: 1 !important; }
      .lang-progress { width: 100%; }
    """
    tree.write(path, encoding="unicode")
    print(f"Finalized {path}")
