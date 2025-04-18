from generate_svg import generate_svg_multiple, collect_examples, save_svgs, load_svgs_from_feedback
from lib.viewer.svg_viewer import SVGViewer
import argparse
import random
import time
import os
import tkinter as tk

def name_output_dir(concept: str, output_dir: str):
    timestamp = int(time.time())
    random_suffix = random.randint(1000, 9999)
    return f"{output_dir}/{concept}_{timestamp}_{random_suffix}"

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--concept", type=str, default="cow")
    parser.add_argument("--style", type=str, default="flat")
    parser.add_argument("--examples_dir", type=str, default="examples")
    parser.add_argument("--n", type=int, default=10)
    parser.add_argument("--output_dir", type=str, default="results/")
    parser.add_argument("--n_examples", type=int, default=10)
    return parser.parse_args()

def main():
    args = parse_args()
    concept = args.concept
    style = args.style

    examples_dir = os.path.join(".data", style, args.examples_dir)
    results_dir = os.path.join(".data", style, args.output_dir)

    os.makedirs(examples_dir, exist_ok=True)
    os.makedirs(results_dir, exist_ok=True)

    examples, example_names = collect_examples(concept, examples_dir, args.n_examples)
    print(f"Collected {len(example_names)} examples for concept: {concept}: {', '.join(example_names)}")

    print(f"Generating {args.n} SVGs for concept: {args.concept}")

    svgs = generate_svg_multiple(concept, examples, args.n)

    output_dir = name_output_dir(concept, results_dir)

    save_svgs(concept, svgs, output_dir)

    print(f"Saved {len(svgs)} SVGs to {output_dir}")

    viewer = SVGViewer(output_dir, examples_dir, concept, f"{concept.capitalize()} made with {args.n_examples} examples")
    feedback_data = viewer.run()

    if not feedback_data: return

    feedback_examples = load_svgs_from_feedback(concept, feedback_data, output_dir)

    print(f"Feedback examples: {feedback_examples}")

    svgs = generate_svg_multiple(concept, feedback_examples, args.n)

    output_dir = os.path.join(output_dir, "feedback")

    save_svgs(concept, svgs, output_dir)

    print(f"Saved {len(svgs)} SVGs after reflection to {output_dir}")

    viewer = SVGViewer(output_dir, examples_dir, concept, f"{concept.capitalize()} made with {args.n_examples} examples post reflection", port=8002)
    feedback_data = viewer.run()
    

if __name__ == "__main__":
    main()
