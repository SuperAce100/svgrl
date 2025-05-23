from pathlib import Path
from rich.console import Console
import argparse
from viewer.viewer import Viewer
from typing import List
class ShaderViewer(Viewer):
    """
    A specialized viewer for SVG files.
    """
    def __init__(self, 
                 shader_folder: str, 
                 output_path: str = None, 
                 title: str = "Shader Viewer", 
                 port: int = 8002, 
                 console: Console = None,
                 concept: str = "shader",
                 used_examples: List[str] = None):
        """
        Initialize the ShaderViewer.
        
        Args:
            shader_folder (str): Path to the folder containing shader files
            output_path (str, optional): Path to save the selected object
            title (str, optional): Title for the viewer
            port (int, optional): Port to run the server on
            console (Console, optional): Rich console for output
        """
        
        super().__init__(
            data_folder=str(shader_folder),
            output_path=output_path,
            concept=concept,
            title=title,
            port=port,
            console=console,
            custom_scripts_path="domains/shaders/shader_scripts.js",
            used_examples=used_examples
        )
    
    
    
        


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Shader Viewer Example')
    parser.add_argument('--data-dir', type=str, default='../.data/shaders/results/elephant', 
                        help='Directory containing shader files')
    parser.add_argument('--output-dir', type=str, default='../.data/shaders/examples', 
                        help='Directory to save selected files')
    parser.add_argument('--port', type=int, default=8002, 
                        help='Port to run the server on')
    args = parser.parse_args()
    
    console = Console()
    
    data_dir = Path(args.data_dir)
    data_dir.mkdir(parents=True, exist_ok=True)
    
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    
    viewer = ShaderViewer(
        shader_folder=str(data_dir),
        output_path=str(output_dir),
        concept="examples",
        title="Shader Viewer",
        port=args.port,
        console=console
    )

    feedback_data = viewer.run()
    
    console.print(feedback_data)

if __name__ == "__main__":
    main() 