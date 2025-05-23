import json
from tqdm import tqdm
from domains.svg.prompts import *
from models.models import llm_call, text_model
from lib.utils import parse_svg
import os
import concurrent.futures
from sentence_transformers import SentenceTransformer
import numpy as np



def collect_examples(concept: str, examples_dir: str, n: int = 10):
    examples = ""
    if n == 0:
        return examples, []

    if n > len(os.listdir(examples_dir)):
        n = len(os.listdir(examples_dir))
    
    model = SentenceTransformer('all-MiniLM-L6-v2')
    all_files = [f for f in os.listdir(examples_dir) if f.endswith(".svg")]
    file_names = [os.path.splitext(f)[0] for f in all_files]
    
    concept_embedding = model.encode([concept])[0]
    filename_embeddings = model.encode(file_names)
    
    similarities = np.dot(filename_embeddings, concept_embedding)
    top_indices = np.argsort(similarities)[-n:][::-1]
    svg_files = [all_files[i] for i in top_indices]
    example_names = [file_names[i] for i in top_indices]

    for svg_file in svg_files:
        with open(os.path.join(examples_dir, svg_file), "r") as file:
            svg_content = file.read()

        example_concept = os.path.splitext(svg_file)[0]

        formatted_example = svg_examples_format.format(
            concept=example_concept, example=svg_content
        )

        examples += formatted_example

    return examples, example_names

def extract_tags(prompt: str, old_tags: list[str], model: str = text_model) -> list[str]:
    tags_xml = llm_call(svg_tags_format.format(svg=prompt, old_tags=old_tags), model=model)
    tags = [tag.strip() for tag in tags_xml.split("<tag>")[1:] if tag.strip()]
    tags = [tag.split("</tag>")[0].strip() for tag in tags]
    return tags

def generate_svg_multiple(concept: str, examples: str, old_tags: list[str], n: int = 10, model: str = text_model):
    svg_results = llm_call(svg_user_prompt.format(concept=concept), system_prompt=svg_system_prompt.format(examples=examples, n=n), model=model)

    svg_results = [p.strip() for p in svg_results.split("<result>")[1:] if p.strip()]
    svg_results = [p.split("</result>")[0].strip() for p in svg_results]

    def process_svg(svg):
        tags = extract_tags(svg, old_tags)
        return svg, tags

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_svg, svg) for svg in svg_results]
        results = [future.result() for future in tqdm(concurrent.futures.as_completed(futures), total=n, desc="Generating SVGs")]
        svgs, tags = zip(*results)

    return svgs, tags


def generate_insights(feedback: str, model: str = text_model) -> str:
    return llm_call(svg_insights_format.format(feedback=feedback), model=model)


def load_svgs_from_feedback(concept: str, feedback_data: dict[str, list], examples_dir: str):
    examples_str = ""
    for filename, feedbacks in feedback_data.items():
        with open(os.path.join(examples_dir, filename), "r") as f:
            svg = f.read()
            examples_str += svg_feedback_format.format(concept=concept, example=svg, feedback=feedbacks)

    insights = generate_insights(examples_str)

    return examples_str + "\n Here is what you need to include in every future generation: \n" + insights


def save_svgs(svgs: list, tags: list[str], output_dir: str):
    for i, svg in enumerate(svgs):
        os.makedirs(output_dir, exist_ok=True)
        with open(os.path.join(output_dir, f"{i}.json"), "w") as f:
            json.dump({"svg": svg, "tags": tags[i]}, f)

def main():
    concept = "cow"
    examples, example_names = collect_examples(concept, "examples")

    svgs, tags = generate_svg_multiple(concept, examples, 10)
    save_svgs(svgs, tags, "results/test-3")


if __name__ == "__main__":
    main()
