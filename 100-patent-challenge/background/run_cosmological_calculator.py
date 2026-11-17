#!/usr/bin/env python3
# Run both cosmological constant calculators and compare their results

import time
import os
import numpy as np
import matplotlib.pyplot as plt
from cosmological_constant_calculator import CosmologicalConstantCalculator
from cosmological_constant_calculator_v2 import CosmologicalConstantCalculatorV2
import mpmath as mp

def run_comparison(timeout=300):  # Default timeout of 5 minutes
    """Run both calculators and compare their results"""
    print("=" * 80)
    print("COSMOLOGICAL CONSTANT CALCULATOR COMPARISON")
    print("=" * 80)
    
    # Create output directory
    os.makedirs('comparison_results', exist_ok=True)
    
    # --- Original Calculator ---
    print("\n\n" + "=" * 50)
    print("RUNNING ORIGINAL CALCULATOR")
    print("=" * 50)
    
    # Start timer
    start_time = time.time()
    
    # Run original calculator without optimization
    calc1 = CosmologicalConstantCalculator()
    lambda_v1_pre = calc1.calculate_lambda()
    ratio_v1_pre = lambda_v1_pre / calc1.lambda_observed
    
    # Calculate with quantum corrections
    lambda_v1_post = calc1.calculate_with_quantum_corrections(qc_level=3)
    ratio_v1_post = lambda_v1_post / calc1.lambda_observed
    
    # Generate visualization
    calc1.visualize_contributions()
    
    # End timer
    time_v1 = time.time() - start_time
    
    # --- Enhanced Calculator ---
    print("\n\n" + "=" * 50)
    print("RUNNING ENHANCED CALCULATOR V2")
    print("=" * 50)
    
    # Start timer
    start_time = time.time()
    
    # Run enhanced calculator without optimization
    calc2 = CosmologicalConstantCalculatorV2()
    lambda_v2_pre = calc2.calculate_lambda()
    ratio_v2_pre = lambda_v2_pre / calc2.lambda_observed
    
    # Calculate with quantum corrections
    lambda_v2_post = calc2.calculate_with_quantum_corrections(qc_level=3)
    ratio_v2_post = lambda_v2_post / calc2.lambda_observed
    
    # Generate visualization
    calc2.visualize_contributions()
    
    # End timer
    time_v2 = time.time() - start_time
    
    # --- Comparison ---
    print("\n\n" + "=" * 50)
    print("COMPARISON OF RESULTS")
    print("=" * 50)
    
    print(f"\nPerformance:")
    print(f"  Original calculator time: {time_v1:.2f} seconds")
    print(f"  Enhanced calculator time: {time_v2:.2f} seconds")
    
    print(f"\nBefore quantum corrections:")
    print(f"  Original calculator: {float(lambda_v1_pre):.4e} m^-2 (ratio to observed: {float(ratio_v1_pre):.4e})")
    print(f"  Enhanced calculator: {float(lambda_v2_pre):.4e} m^-2 (ratio to observed: {float(ratio_v2_pre):.4e})")
    
    print(f"\nAfter quantum corrections:")
    print(f"  Original calculator: {float(lambda_v1_post):.4e} m^-2 (ratio to observed: {float(ratio_v1_post):.4e})")
    print(f"  Enhanced calculator: {float(lambda_v2_post):.4e} m^-2 (ratio to observed: {float(ratio_v2_post):.4e})")
    
    print(f"\nImprovement in accuracy (ratio closer to 1.0):")
    improvement_pre = abs(float(mp.log10(abs(float(ratio_v2_pre)))) - float(mp.log10(abs(float(ratio_v1_pre)))))
    improvement_post = abs(float(mp.log10(abs(float(ratio_v2_post)))) - float(mp.log10(abs(float(ratio_v1_post)))))
    
    print(f"  Before corrections: {improvement_pre:.2f} orders of magnitude")
    print(f"  After corrections: {improvement_post:.2f} orders of magnitude")
    
    # Create comparison visualization
    create_comparison_visualization(
        calc1, calc2, 
        lambda_v1_pre, lambda_v2_pre,
        ratio_v1_pre, ratio_v2_pre,
        time_v1, time_v2
    )
    
    print("\nComparison completed. Visualization saved to 'comparison_results/comparison.png'")
    
    return {
        'original': {
            'lambda_pre': float(lambda_v1_pre),
            'lambda_post': float(lambda_v1_post),
            'ratio_pre': float(ratio_v1_pre),
            'ratio_post': float(ratio_v1_post),
            'time': time_v1
        },
        'enhanced': {
            'lambda_pre': float(lambda_v2_pre),
            'lambda_post': float(lambda_v2_post),
            'ratio_pre': float(ratio_v2_pre),
            'ratio_post': float(ratio_v2_post),
            'time': time_v2
        }
    }

def create_comparison_visualization(calc1, calc2, lambda_v1, lambda_v2, ratio_v1, ratio_v2, time_v1, time_v2):
    """Create a visualization comparing the two calculators"""
    plt.figure(figsize=(16, 12))
    
    # --- Plot 1: Ratios (log scale) ---
    plt.subplot(2, 2, 1)
    labels = ['Original', 'Enhanced v2']
    ratios = [float(ratio_v1), float(ratio_v2)]
    colors = ['skyblue', 'orange']
    
    # Convert to log scale for bar height
    log_ratios = [float(mp.log10(abs(float(r)))) for r in ratios]
    
    bars = plt.bar(labels, log_ratios, color=colors)
    plt.axhline(y=0, color='green', linestyle='--', label='Perfect match (ratio=1)')
    
    # Add value labels
    for bar, ratio in zip(bars, ratios):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                 f'{ratio:.2e}', ha='center', va='bottom', rotation=0)
    
    plt.title('Log10 of Ratio to Observed Value')
    plt.ylabel('Log10(Calculator/Observed)')
    plt.grid(axis='y', alpha=0.3)
    
    # --- Plot 2: Computation Time ---
    plt.subplot(2, 2, 2)
    times = [time_v1, time_v2]
    
    plt.bar(labels, times, color=colors)
    plt.title('Computation Time')
    plt.ylabel('Seconds')
    plt.grid(axis='y', alpha=0.3)
    
    # --- Plot 3: Correlation with observed value ---
    plt.subplot(2, 2, 3)
    x = np.linspace(-60, -40, 100)  # Log scale for cosmological constant
    y1 = np.linspace(-60, -40, 100)  # Perfect correlation
    
    # Log of values
    log_lambda_v1 = float(mp.log10(abs(float(lambda_v1))))
    log_lambda_v2 = float(mp.log10(abs(float(lambda_v2))))
    log_lambda_obs = float(mp.log10(abs(float(calc1.lambda_observed))))
    
    plt.plot(x, y1, 'g--', label='Perfect correlation')
    plt.scatter([log_lambda_obs], [log_lambda_obs], color='red', s=100, marker='*', label='Observed value')
    plt.scatter([log_lambda_v1], [log_lambda_obs], color='skyblue', s=80, label='Original calculator')
    plt.scatter([log_lambda_v2], [log_lambda_obs], color='orange', s=80, label='Enhanced calculator')
    
    plt.title('Correlation with Observed Value (Log Scale)')
    plt.xlabel('Log10(Calculated Value)')
    plt.ylabel('Log10(Observed Value)')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # --- Plot 4: Parameter comparison (if available) ---
    plt.subplot(2, 2, 4)
    
    # Get parameters from both calculators
    params1 = [
        float(calc1.r0), float(calc1.alpha), float(calc1.c0), 
        float(calc1.beta), float(calc1.gamma), float(calc1.lambda_ord)
    ]
    
    params2 = [
        float(calc2.r0), float(calc2.alpha), float(calc2.c0), 
        float(calc2.beta), float(calc2.gamma), float(calc2.lambda_ord)
    ]
    
    param_names = ['r0', 'alpha', 'c0', 'beta', 'gamma', 'lambda_ord']
    
    # Plot parameters as radar chart
    angles = np.linspace(0, 2*np.pi, len(params1), endpoint=False).tolist()
    angles += angles[:1]  # Close the loop
    
    # Normalize parameters for radar chart
    max_values = [max(p1, p2) for p1, p2 in zip(params1, params2)]
    norm_params1 = [p1/max_val if max_val > 0 else 0 for p1, max_val in zip(params1, max_values)]
    norm_params2 = [p2/max_val if max_val > 0 else 0 for p2, max_val in zip(params2, max_values)]
    
    # Close the loop
    norm_params1 += norm_params1[:1]
    norm_params2 += norm_params2[:1]
    
    # Create radar chart
    ax = plt.subplot(2, 2, 4, polar=True)
    ax.plot(angles, norm_params1, 'o-', linewidth=2, color='skyblue', label='Original')
    ax.plot(angles, norm_params2, 'o-', linewidth=2, color='orange', label='Enhanced')
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(param_names)
    ax.set_title('Parameter Comparison (Normalized)')
    ax.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    
    plt.tight_layout()
    plt.savefig('comparison_results/comparison.png', dpi=300)

if __name__ == "__main__":
    results = run_comparison() 