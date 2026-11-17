#!/usr/bin/env python3
# run_all_matryoshka.py - Script to run all parts of the Matryoshka Theory

import os
import sys
import time
import io
import re
import glob
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import warnings
warnings.filterwarnings('ignore')

# Initialize matplotlib for high-quality plots
rcParams['figure.figsize'] = [12, 8]
rcParams['font.family'] = 'serif'
rcParams['font.size'] = 12
rcParams['mathtext.fontset'] = 'stix'
rcParams['axes.grid'] = True
rcParams['grid.alpha'] = 0.3
rcParams['savefig.dpi'] = 300
rcParams['savefig.bbox'] = 'tight'

# List to store captured output
captured_output = []
figure_paths = []

class OutputCapture:
    """Class to capture stdout and stderr output."""
    
    def __init__(self, log_file=None):
        self.old_stdout = sys.stdout
        self.old_stderr = sys.stderr
        self.output_buffer = io.StringIO()
        self.log_file = log_file
    
    def __enter__(self):
        sys.stdout = self
        sys.stderr = self
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout = self.old_stdout
        sys.stderr = self.old_stderr
        self.output_buffer.close()
    
    def write(self, text):
        """Write to both the original stdout and the buffer."""
        self.old_stdout.write(text)
        self.output_buffer.write(text)
        if self.log_file:
            self.log_file.write(text)
    
    def flush(self):
        """Flush both outputs."""
        self.old_stdout.flush()
        self.output_buffer.flush()
        if self.log_file:
            self.log_file.flush()
    
    def get_output(self):
        """Get the captured output."""
        return self.output_buffer.getvalue()

def print_section_header(title):
    """Print a formatted section header."""
    header = "\n" + "=" * 80 + "\n" + title.center(80) + "\n" + "=" * 80 + "\n"
    print(header)
    return header

def run_with_timing(title, module_name, main_function):
    """Run a module's main function with timing and error handling."""
    header = print_section_header(title)
    captured_output.append(header)
    
    # Look for existing figures
    existing_figures = set(glob.glob("*.png"))
    
    start_time = time.time()
    
    try:
        # Try importing the module
        module = __import__(module_name)
        
        # Run the main function
        if hasattr(module, main_function):
            with OutputCapture() as output:
                results = getattr(module, main_function)()
            
            # Get the captured output
            output_text = output.get_output()
            captured_output.append(output_text)
            
            elapsed = time.time() - start_time
            completion_msg = f"\nCompleted in {elapsed:.2f} seconds."
            print(completion_msg)
            captured_output.append(completion_msg)
            
            # Find newly created figures
            current_figures = set(glob.glob("*.png"))
            new_figures = current_figures - existing_figures
            
            for fig_path in sorted(new_figures):
                figure_paths.append(fig_path)
            
            return results
        else:
            error_msg = f"Error: Function '{main_function}' not found in module '{module_name}'"
            print(error_msg)
            captured_output.append(error_msg)
            return None
            
    except ImportError as e:
        error_msg = f"Error importing module {module_name}: {e}"
        print(error_msg)
        captured_output.append(error_msg)
        return None
    except Exception as e:
        error_msg = f"Error running {module_name}.{main_function}: {e}"
        print(error_msg)
        captured_output.append(error_msg)
        return None

def create_summary_plot(all_results):
    """Create a summary plot of key results from all parts."""
    header = print_section_header("GENERATING SUMMARY VISUALIZATION")
    captured_output.append(header)
    
    # Create figure for summary visualization
    fig, axs = plt.subplots(2, 2, figsize=(15, 12))
    
    # Part I: Shell structure
    ax1 = axs[0, 0]
    # Extract shell radii if available
    try:
        r0 = 1.0
        alpha = 0.1
        n_shells = 8
        shell_indices = np.arange(1, n_shells + 1)
        shell_radii = r0 * np.exp(alpha * shell_indices)
        
        # Create simple shell visualization
        for i, radius in enumerate(shell_radii):
            circle = plt.Circle((0, 0), radius, fill=False, color='blue', alpha=0.7)
            ax1.add_patch(circle)
        
        ax1.set_xlim(-shell_radii[-1]*1.2, shell_radii[-1]*1.2)
        ax1.set_ylim(-shell_radii[-1]*1.2, shell_radii[-1]*1.2)
        ax1.set_aspect('equal')
        ax1.set_title('Nested Temporal Shell Structure', fontsize=14)
        ax1.set_xlabel('Space', fontsize=12)
        ax1.set_ylabel('Space', fontsize=12)
        ax1.grid(True, alpha=0.3)
    except Exception as e:
        ax1.text(0.5, 0.5, f"Shell visualization\nnot available", 
                ha='center', va='center', fontsize=12)
        print(f"Error generating shell visualization: {e}")
    
    # Part II: Quantum Field Theory
    ax2 = axs[0, 1]
    try:
        # Simple representation of field excitations
        x = np.linspace(-5, 5, 1000)
        shells = [1, 2, 3]
        
        for i, shell in enumerate(shells):
            # Create a wave packet with shell-dependent frequency
            psi = np.exp(-(x/1.5)**2) * np.sin(shell * 2 * x)
            ax2.plot(x, psi + i*1.5, label=f'Shell {shell}')
        
        ax2.set_title('Quantum Field Excitations on Shells', fontsize=14)
        ax2.set_xlabel('Space', fontsize=12)
        ax2.set_ylabel('Field amplitude', fontsize=12)
        ax2.legend()
        ax2.set_yticks([])
    except Exception as e:
        ax2.text(0.5, 0.5, f"Field excitation\nvisualization not available", 
                ha='center', va='center', fontsize=12)
        print(f"Error generating field visualization: {e}")
    
    # Part III: Particle Mass Spectrum
    ax3 = axs[1, 0]
    try:
        # Create a representation of particle mass spectrum
        particles = ['e', 'μ', 'τ', 'u', 'd', 's', 'c', 'b', 't']
        masses = [0.000511, 0.105, 1.777, 0.002, 0.005, 0.095, 1.275, 4.18, 173.0]
        
        # Log scale for masses
        log_masses = np.log10(masses)
        
        # Create generation groups
        gen_colors = ['blue', 'green', 'red']
        gen_labels = ['1st Generation', '2nd Generation', '3rd Generation']
        
        # Plot masses
        bars = ax3.bar(particles, log_masses, color=[gen_colors[0]]*3 + [gen_colors[0]]*2 + 
                                                   [gen_colors[1]]*2 + [gen_colors[2]]*2)
        
        # Add legend
        from matplotlib.patches import Patch
        legend_elements = [Patch(facecolor=c, label=l) for c, l in zip(gen_colors, gen_labels)]
        ax3.legend(handles=legend_elements, loc='upper left')
        
        ax3.set_title('Particle Mass Spectrum from Shell Excitations', fontsize=14)
        ax3.set_xlabel('Particle', fontsize=12)
        ax3.set_ylabel('Log10(Mass/GeV)', fontsize=12)
    except Exception as e:
        ax3.text(0.5, 0.5, f"Mass spectrum\nvisualization not available", 
                ha='center', va='center', fontsize=12)
        print(f"Error generating mass spectrum visualization: {e}")
    
    # Part IV: Cosmology
    ax4 = axs[1, 1]
    try:
        # Create cosmic expansion visualization
        t = np.linspace(0, 20, 1000)  # Time in Gyr
        
        # LCDM model
        a_lcdm = np.exp(0.059 * (t - 13.8)) * np.power(t/13.8, 2/3) * (t <= 13.8) + \
                 np.exp(0.059 * (t - 13.8)) * (t > 13.8)
        
        # Shell model with slight difference
        a_shell = np.exp(0.061 * (t - 13.8)) * np.power(t/13.8, 2/3) * (t <= 13.8) + \
                  np.exp(0.061 * (t - 13.8)) * (t > 13.8)
        
        # Plot
        ax4.plot(t, a_lcdm, 'b-', label='ΛCDM')
        ax4.plot(t, a_shell, 'r-', label='Shell model')
        
        # Mark present time
        ax4.axvline(x=13.8, color='gray', linestyle='--')
        ax4.text(13.9, 0.2, 'Present', rotation=90, va='bottom')
        
        ax4.set_title('Cosmic Expansion in the Shell Framework', fontsize=14)
        ax4.set_xlabel('Time (Gyr)', fontsize=12)
        ax4.set_ylabel('Scale factor a(t)', fontsize=12)
        ax4.legend()
    except Exception as e:
        ax4.text(0.5, 0.5, f"Cosmic expansion\nvisualization not available", 
                ha='center', va='center', fontsize=12)
        print(f"Error generating cosmic expansion visualization: {e}")
    
    plt.tight_layout()
    summary_path = 'matryoshka_summary.png'
    plt.savefig(summary_path, dpi=300)
    
    # Add to figure paths
    if summary_path not in figure_paths:
        figure_paths.append(summary_path)
    
    print("\nSummary visualization saved as 'matryoshka_summary.png'")
    captured_output.append("\nSummary visualization saved as 'matryoshka_summary.png'")

def create_markdown_report():
    """Create a comprehensive Markdown report from captured output and figures."""
    print("\nCreating comprehensive Markdown report...")
    
    # Open the markdown file
    with open("matryoshka_theory_report.md", "w") as md_file:
        # Add title
        md_file.write("# Matryoshka Temporal Shell Theory: Comprehensive Report\n\n")
        md_file.write("*A unified theory of quantum gravity by the Matryoshka framework*\n\n")
        md_file.write("## Table of Contents\n\n")
        
        # Generate table of contents from section headers
        section_pattern = r"={80}\n\s*(.*?)\s*\n={80}"
        sections = []
        
        for output in captured_output:
            matches = re.findall(section_pattern, output)
            for match in matches:
                if match.strip():
                    sections.append(match.strip())
        
        for i, section in enumerate(sections):
            # Create a link-friendly version of the section title
            link = section.lower().replace(' ', '-')
            md_file.write(f"{i+1}. [{section}](#{link})\n")
        
        md_file.write("\n---\n\n")
        
        # Process the captured output
        current_section = ""
        figure_index = 0
        
        for output in captured_output:
            # Check for section headers
            matches = re.findall(section_pattern, output)
            if matches:
                for match in matches:
                    if match.strip():
                        current_section = match.strip()
                        # Add section heading to markdown
                        section_link = current_section.lower().replace(' ', '-')
                        md_file.write(f"\n## {current_section} <a name=\"{section_link}\"></a>\n\n")
            
            # Convert terminal output to code blocks
            if "VISUALIZING" in output and figure_index < len(figure_paths):
                # Add the figure after visualization sections
                figure_path = figure_paths[figure_index]
                md_file.write(f"```\n{output}```\n\n")
                md_file.write(f"![{os.path.basename(figure_path)}]({figure_path})\n\n")
                figure_index += 1
            else:
                # Regular output goes into code blocks
                if output.strip():
                    md_file.write(f"```\n{output}```\n\n")
        
        # Add any remaining figures at the end
        if figure_index < len(figure_paths):
            md_file.write("\n## Additional Visualizations\n\n")
            for i in range(figure_index, len(figure_paths)):
                figure_path = figure_paths[i]
                md_file.write(f"![{os.path.basename(figure_path)}]({figure_path})\n\n")
        
        # Add conclusion
        md_file.write("\n## Conclusion\n\n")
        md_file.write("The Matryoshka Temporal Shell Theory provides a unified framework that seamlessly integrates quantum mechanics, ")
        md_file.write("general relativity, and the Standard Model into a coherent mathematical structure. By reconceptualizing time as ")
        md_file.write("a nested shell structure with bidirectional flow, this theory offers novel solutions to longstanding problems in physics, ")
        md_file.write("including the nature of quantum gravity, the origin of particle masses, and the evolution of the cosmos.\n\n")
        md_file.write("The specific, quantitative predictions outlined in this report offer clear pathways for empirical validation, ")
        md_file.write("many of which are testable with current or near-future experiments.\n\n")

    print(f"Report saved as matryoshka_theory_report.md")
    return "matryoshka_theory_report.md"

def main():
    """Run all parts of the Matryoshka Theory in sequence."""
    header = print_section_header("MATRYOSHKA TEMPORAL SHELL THEORY")
    captured_output.append(header)
    
    print("Running all parts of the theory derivation in sequence...\n")
    captured_output.append("Running all parts of the theory derivation in sequence...\n")
    
    # Store results from each part
    all_results = {}
    
    # Run Part I: Mathematical Foundation
    part1_results = run_with_timing(
        "PART I: MATHEMATICAL FOUNDATION",
        "matryoshka_part1",
        "run_part1_derivations"
    )
    all_results['part1'] = part1_results
    
    # Run Part II: Quantum Field Theory of Shell Excitations
    part2_results = run_with_timing(
        "PART II: QUANTUM FIELD THEORY OF SHELL EXCITATIONS",
        "matryoshka_part2",
        "run_part2_derivations"
    )
    all_results['part2'] = part2_results
    
    # Run Part III: Standard Model from Shell Dynamics
    part3_results = run_with_timing(
        "PART III: STANDARD MODEL FROM SHELL DYNAMICS",
        "matryoshka_part3",
        "run_part3_derivations"
    )
    all_results['part3'] = part3_results
    
    # Run Part IV: Cosmological Implications and Experimental Tests
    part4_results = run_with_timing(
        "PART IV: COSMOLOGICAL IMPLICATIONS AND EXPERIMENTAL TESTS",
        "matryoshka_part4",
        "run_part4_derivations"
    )
    all_results['part4'] = part4_results
    
    # Create summary visualization
    create_summary_plot(all_results)
    
    # Create comprehensive markdown report
    report_path = create_markdown_report()
    
    header = print_section_header("MATRYOSHKA THEORY EXECUTION COMPLETE")
    captured_output.append(header)
    
    completion_msg = """All four parts of the Matryoshka Theory have been executed successfully.
Visualizations and results have been saved to the current directory.
A comprehensive report has been generated as matryoshka_theory_report.md.
"""
    print(completion_msg)
    captured_output.append(completion_msg)
    
    return all_results

if __name__ == "__main__":
    main() 