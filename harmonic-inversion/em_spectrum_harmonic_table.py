#!/usr/bin/env python3
"""
Complete Harmonic Table of EM Spectrum from Fundamental Frequencies
===================================================================
Shows how every frequency in the EM spectrum emerges from the three
fundamental visible light frequencies through harmonic relationships.
"""

import numpy as np
import pandas as pd
from tabulate import tabulate


def generate_harmonic_table():
    """Generate comprehensive harmonic relationships table."""
    
    # Fundamental frequencies (THz)
    red = 430
    green = 540
    blue = 650
    
    # Convert to Hz for calculations
    red_hz = red * 1e12
    green_hz = green * 1e12
    blue_hz = blue * 1e12
    
    harmonics = []
    
    # Radio frequencies (subharmonics)
    print("RADIO FREQUENCIES (Subharmonics)")
    print("=" * 80)
    
    # AM Radio (~1 MHz)
    am_freq = 1e6
    red_ratio = red_hz / am_freq
    harmonics.append({
        'Name': 'AM Radio',
        'Frequency': '1 MHz',
        'Relationship': f'Red ÷ {red_ratio:.0f}',
        'Mechanism': 'Deep subharmonic'
    })
    
    # FM Radio (~100 MHz)
    fm_freq = 100e6
    red_ratio = red_hz / fm_freq
    harmonics.append({
        'Name': 'FM Radio',
        'Frequency': '100 MHz',
        'Relationship': f'Red ÷ {red_ratio:.0f}',
        'Mechanism': 'Subharmonic'
    })
    
    # Cellular (~1 GHz)
    cell_freq = 1e9
    red_ratio = red_hz / cell_freq
    harmonics.append({
        'Name': 'Cellular',
        'Frequency': '1 GHz',
        'Relationship': f'Red ÷ {red_ratio:.0f}',
        'Mechanism': 'Subharmonic'
    })
    
    # Microwave frequencies
    print("\nMICROWAVE FREQUENCIES (Beat frequencies)")
    print("=" * 80)
    
    # WiFi 2.4 GHz
    wifi_freq = 2.4e9
    beat = abs(blue_hz - green_hz)
    ratio = wifi_freq / beat
    harmonics.append({
        'Name': 'WiFi 2.4GHz',
        'Frequency': '2.4 GHz',
        'Relationship': f'|Blue-Green| ÷ {beat/wifi_freq:.0f}',
        'Mechanism': 'Beat frequency subharmonic'
    })
    
    # Microwave oven (2.45 GHz)
    harmonics.append({
        'Name': 'Microwave Oven',
        'Frequency': '2.45 GHz',
        'Relationship': f'|Blue-Green| ÷ {beat/2.45e9:.0f}',
        'Mechanism': 'Water resonance beat'
    })
    
    # 5G (~30 GHz)
    freq_5g = 30e9
    harmonics.append({
        'Name': '5G mmWave',
        'Frequency': '30 GHz',
        'Relationship': f'|Blue-Red| ÷ {abs(blue_hz-red_hz)/freq_5g:.0f}',
        'Mechanism': 'Difference frequency'
    })
    
    # Infrared frequencies
    print("\nINFRARED FREQUENCIES (Approaching visible)")
    print("=" * 80)
    
    # Far IR (1 THz)
    harmonics.append({
        'Name': 'Far Infrared',
        'Frequency': '1 THz',
        'Relationship': 'Red ÷ 430',
        'Mechanism': 'Subharmonic approach'
    })
    
    # Thermal IR (30 THz)
    harmonics.append({
        'Name': 'Thermal IR',
        'Frequency': '30 THz',
        'Relationship': 'Red ÷ 14.3',
        'Mechanism': 'Body heat emission'
    })
    
    # Near IR (300 THz)
    harmonics.append({
        'Name': 'Near Infrared',
        'Frequency': '300 THz',
        'Relationship': 'Red ÷ 1.43',
        'Mechanism': 'Approaching visible'
    })
    
    # Visible frequencies
    print("\nVISIBLE LIGHT (Fundamental frequencies)")
    print("=" * 80)
    
    harmonics.append({
        'Name': 'Red Light',
        'Frequency': '430 THz',
        'Relationship': 'FUNDAMENTAL',
        'Mechanism': 'Primary entropy orbit'
    })
    
    harmonics.append({
        'Name': 'Yellow',
        'Frequency': '485 THz',
        'Relationship': '(Red + Green) ÷ 2',
        'Mechanism': 'Mixing frequency'
    })
    
    harmonics.append({
        'Name': 'Green Light',
        'Frequency': '540 THz',
        'Relationship': 'FUNDAMENTAL',
        'Mechanism': 'Primary entropy orbit'
    })
    
    harmonics.append({
        'Name': 'Cyan',
        'Frequency': '595 THz',
        'Relationship': '(Green + Blue) ÷ 2',
        'Mechanism': 'Mixing frequency'
    })
    
    harmonics.append({
        'Name': 'Blue Light',
        'Frequency': '650 THz',
        'Relationship': 'FUNDAMENTAL',
        'Mechanism': 'Primary entropy orbit'
    })
    
    harmonics.append({
        'Name': 'Violet',
        'Frequency': '700 THz',
        'Relationship': 'Blue × 1.08',
        'Mechanism': 'Overtone edge'
    })
    
    # Ultraviolet frequencies
    print("\nULTRAVIOLET FREQUENCIES (Overtones)")
    print("=" * 80)
    
    harmonics.append({
        'Name': 'UV-A',
        'Frequency': '860 THz',
        'Relationship': 'Red × 2',
        'Mechanism': 'Second harmonic'
    })
    
    harmonics.append({
        'Name': 'UV-B',
        'Frequency': '1080 THz',
        'Relationship': 'Green × 2',
        'Mechanism': 'Second harmonic'
    })
    
    harmonics.append({
        'Name': 'UV-C',
        'Frequency': '1300 THz',
        'Relationship': 'Blue × 2',
        'Mechanism': 'Second harmonic'
    })
    
    harmonics.append({
        'Name': 'Extreme UV',
        'Frequency': '10 PHz',
        'Relationship': 'Blue × 15.4',
        'Mechanism': 'High harmonic'
    })
    
    # X-ray frequencies
    print("\nX-RAY FREQUENCIES (High harmonics)")
    print("=" * 80)
    
    harmonics.append({
        'Name': 'Soft X-ray',
        'Frequency': '100 PHz',
        'Relationship': 'Red × 233',
        'Mechanism': 'High harmonic generation'
    })
    
    harmonics.append({
        'Name': 'Hard X-ray',
        'Frequency': '10 EHz',
        'Relationship': 'Green × 18,519',
        'Mechanism': 'Extreme harmonic'
    })
    
    # Gamma ray frequencies
    print("\nGAMMA RAY FREQUENCIES (Singularities)")
    print("=" * 80)
    
    harmonics.append({
        'Name': 'Low Gamma',
        'Frequency': '100 EHz',
        'Relationship': 'Blue × 154,000',
        'Mechanism': 'Entropy singularity'
    })
    
    harmonics.append({
        'Name': 'High Gamma',
        'Frequency': '1 ZHz',
        'Relationship': 'Red × 2.3×10⁶',
        'Mechanism': 'Topological defect'
    })
    
    # Create and display table
    df = pd.DataFrame(harmonics)
    print("\n\nCOMPLETE ELECTROMAGNETIC SPECTRUM HARMONIC TABLE")
    print("=" * 100)
    print(tabulate(df, headers='keys', tablefmt='grid', showindex=False))
    
    # Additional relationships
    print("\n\nKEY MATHEMATICAL RELATIONSHIPS")
    print("=" * 80)
    print(f"Fundamental Ratio (Blue/Red): {blue/red:.3f}")
    print(f"Fundamental Ratio (Green/Red): {green/red:.3f}")
    print(f"Fundamental Ratio (Blue/Green): {blue/green:.3f}")
    print(f"\nDifference Frequencies:")
    print(f"  |Blue - Green| = {blue - green} THz")
    print(f"  |Blue - Red| = {blue - red} THz")
    print(f"  |Green - Red| = {green - red} THz")
    print(f"\nSum Frequencies:")
    print(f"  Red + Green = {red + green} THz")
    print(f"  Red + Blue = {red + blue} THz")
    print(f"  Green + Blue = {green + blue} THz")
    print(f"  Red + Green + Blue = {red + green + blue} THz")
    
    # Golden ratio relationships
    phi = (1 + np.sqrt(5)) / 2
    print(f"\nGolden Ratio Relationships:")
    print(f"  Green/Red ≈ {green/red:.3f} (compare to φ - 1 = {phi-1:.3f})")
    print(f"  Blue/Red ≈ {blue/red:.3f} (compare to φ = {phi:.3f})")
    
    # Musical intervals
    print(f"\nMusical Interval Approximations:")
    print(f"  Blue/Green ≈ {blue/green:.3f} (Minor third: 6/5 = 1.200)")
    print(f"  Green/Red ≈ {green/red:.3f} (Major second: 9/8 = 1.125)")
    print(f"  Blue/Red ≈ {blue/red:.3f} (Perfect fourth: 4/3 = 1.333)")
    
    return df


def generate_wavelength_table():
    """Generate wavelength equivalents."""
    print("\n\nWAVELENGTH EQUIVALENTS")
    print("=" * 80)
    
    # Speed of light
    c = 3e8  # m/s
    
    frequencies = {
        'Red (430 THz)': 430e12,
        'Green (540 THz)': 540e12,
        'Blue (650 THz)': 650e12,
        'Yellow (485 THz)': 485e12,
        'Cyan (595 THz)': 595e12,
        'Violet (700 THz)': 700e12
    }
    
    print(f"{'Color':<20} {'Wavelength (nm)':<20} {'Energy (eV)':<20}")
    print("-" * 60)
    
    h = 6.626e-34  # Planck constant
    eV = 1.602e-19  # electron volt
    
    for name, freq in frequencies.items():
        wavelength = c / freq * 1e9  # Convert to nm
        energy = h * freq / eV  # Convert to eV
        print(f"{name:<20} {wavelength:<20.1f} {energy:<20.3f}")


def main():
    """Generate complete harmonic analysis."""
    df = generate_harmonic_table()
    generate_wavelength_table()
    
    # Save to CSV
    df.to_csv('em_spectrum_harmonics.csv', index=False)
    print("\n\nTable saved to: em_spectrum_harmonics.csv")


if __name__ == "__main__":
    main()