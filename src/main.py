from generate_svg import generate_svg_multiple, collect_examples, save_svgs
from lib.svg_viewer import SVGViewer
import argparse
import random
import time
import tkinter as tk
def name_output_dir(concept: str, output_dir: str):
    
    timestamp = int(time.time())
    random_suffix = random.randint(1000, 9999)
    return f"{output_dir}/{concept}_{timestamp}_{random_suffix}"

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--concept", type=str, default="cow")
    parser.add_argument("--examples_dir", type=str, default="examples")
    parser.add_argument("--n", type=int, default=10)
    parser.add_argument("--output_dir", type=str, default="results/")
    return parser.parse_args()

def main():
    args = parse_args()
    concept = "cow"
    examples = collect_examples(concept, "examples")

    print(f"Generating {args.n} SVGs for concept: {args.concept}")

    svgs = generate_svg_multiple(concept, examples, args.n)

    output_dir = name_output_dir(concept, args.output_dir)

    save_svgs(concept, svgs, output_dir)

    root = tk.Tk()

    svg_viewer = SVGViewer(root, output_dir, args.examples_dir, concept)
    root.mainloop()


if __name__ == "__main__":
    main()
