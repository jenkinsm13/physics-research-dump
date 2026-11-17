#!/usr/bin/env python3
"""
Electromagnetic Spectrum from Entropy Flow Topology
==================================================
Maps the entire EM spectrum based on fundamental qualia frequencies
emerging from temporal entropy flows.

The principle: Each frequency band corresponds to a distinct homology class
of entropy flow trajectories with characteristic periodic orbits.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal, interpolate
from matplotlib.patches import Rectangle
import sympy as sp


class ElectromagneticSpectrumFromEntropy:
    """Maps EM spectrum from fundamental entropy flow frequencies."""
    
    def __init__(self):
        # Fundamental visible qualia frequencies (THz) from entropy flows
        self.fundamental_frequencies = {
            'red': 430,      # ~700 nm wavelength
            'green': 540,    # ~555 nm wavelength  
            'blue': 650      # ~460 nm wavelength
        }
        
        # These create the basis for all EM phenomena
        self.red_basis = 430    # THz
        self.green_basis = 540  # THz
        self.blue_basis = 650   # THz
        
        # Entropy flow parameters
        self.phi_integration = 1.0  # Integrated information
        self.lambda_critical = 0.1  # Critical transition threshold
        
        # Initialize the full spectrum mapping
        self._initialize_spectrum()
        
    def _initialize_spectrum(self):
        """Initialize the complete EM spectrum from entropy flow harmonics."""
        # Frequency range: 1 Hz to 10^24 Hz (gamma rays)
        self.freq_range = np.logspace(0, 24, 10000)  # Hz
        
        # Convert fundamental frequencies to Hz
        self.red_hz = self.red_basis * 1e12
        self.green_hz = self.green_basis * 1e12
        self.blue_hz = self.blue_basis * 1e12
        
        # Generate spectrum regions based on entropy flow topology
        self.spectrum_regions = self._generate_spectrum_regions()
        
    def _generate_spectrum_regions(self):
        """Generate EM spectrum regions from entropy flow harmonics."""
        regions = {}
        
        # Radio waves: Subharmonics of fundamental frequencies
        # Created by long-period entropy flow orbits
        regions['radio'] = {
            'range': (1, 3e9),  # 1 Hz - 3 GHz
            'mechanism': 'Subharmonic resonances of fundamental entropy flows',
            'harmonics': self._calculate_subharmonics(1, 3e9)
        }
        
        # Microwaves: Beat frequencies between subharmonics
        regions['microwave'] = {
            'range': (3e9, 3e11),  # 3 GHz - 300 GHz
            'mechanism': 'Beat frequencies between radio subharmonics',
            'harmonics': self._calculate_beat_frequencies(3e9, 3e11)
        }
        
        # Infrared: Difference frequencies approaching visible
        regions['infrared'] = {
            'range': (3e11, 4.3e14),  # 300 GHz - 430 THz
            'mechanism': 'Entropy flow approaching critical transitions',
            'harmonics': self._calculate_difference_frequencies(3e11, 4.3e14)
        }
        
        # Visible: Fundamental entropy flow frequencies
        regions['visible'] = {
            'range': (4.3e14, 7.5e14),  # 430 - 750 THz
            'mechanism': 'Direct entropy flow periodic orbits creating qualia',
            'harmonics': self._calculate_visible_spectrum()
        }
        
        # Ultraviolet: Overtones of visible frequencies
        regions['ultraviolet'] = {
            'range': (7.5e14, 3e16),  # 750 THz - 30 PHz
            'mechanism': 'Overtones and sum frequencies of visible qualia',
            'harmonics': self._calculate_overtones(7.5e14, 3e16)
        }
        
        # X-rays: High-order harmonics
        regions['xray'] = {
            'range': (3e16, 3e19),  # 30 PHz - 30 EHz
            'mechanism': 'High-order entropy flow harmonics at critical transitions',
            'harmonics': self._calculate_high_harmonics(3e16, 3e19)
        }
        
        # Gamma rays: Entropy flow singularities
        regions['gamma'] = {
            'range': (3e19, 1e24),  # 30 EHz - 1 YHz
            'mechanism': 'Entropy flow singularities and topological defects',
            'harmonics': self._calculate_singularity_spectrum(3e19, 1e24)
        }
        
        return regions
    
    def _calculate_subharmonics(self, f_min, f_max):
        """Calculate subharmonics of fundamental frequencies."""
        harmonics = []
        
        # Generate subharmonics as fractions of fundamentals
        for n in range(1, 20):
            for m in range(1, 10):
                freq = self.red_hz / (n * m)
                if f_min <= freq <= f_max:
                    harmonics.append({
                        'frequency': freq,
                        'source': f'red/{n*m}',
                        'strength': 1.0 / (n * m)
                    })
                
                freq = self.green_hz / (n * m)
                if f_min <= freq <= f_max:
                    harmonics.append({
                        'frequency': freq,
                        'source': f'green/{n*m}',
                        'strength': 1.0 / (n * m)
                    })
                    
                freq = self.blue_hz / (n * m)
                if f_min <= freq <= f_max:
                    harmonics.append({
                        'frequency': freq,
                        'source': f'blue/{n*m}',
                        'strength': 1.0 / (n * m)
                    })
        
        return sorted(harmonics, key=lambda x: x['frequency'])
    
    def _calculate_beat_frequencies(self, f_min, f_max):
        """Calculate beat frequencies between fundamentals."""
        harmonics = []
        
        # Beat frequencies from mixing
        fundamentals = [self.red_hz, self.green_hz, self.blue_hz]
        
        for i, f1 in enumerate(fundamentals):
            for j, f2 in enumerate(fundamentals):
                if i != j:
                    # Difference frequencies
                    for n in range(1, 1000):
                        freq = abs(f1 - f2) / n
                        if f_min <= freq <= f_max:
                            harmonics.append({
                                'frequency': freq,
                                'source': f'|{["red","green","blue"][i]}-{["red","green","blue"][j]}|/{n}',
                                'strength': 1.0 / n
                            })
        
        return sorted(harmonics, key=lambda x: x['frequency'])
    
    def _calculate_difference_frequencies(self, f_min, f_max):
        """Calculate difference frequencies approaching visible."""
        harmonics = []
        
        # Geometric series approaching fundamentals
        for fundamental, name in [(self.red_hz, 'red'), 
                                  (self.green_hz, 'green'), 
                                  (self.blue_hz, 'blue')]:
            
            # Approach from below
            freq = f_min
            n = 1
            while freq < fundamental and freq <= f_max:
                harmonics.append({
                    'frequency': freq,
                    'source': f'{name}_approach_{n}',
                    'strength': np.exp(-n/10)
                })
                freq = fundamental * (1 - np.exp(-n/5))
                n += 1
        
        return sorted(harmonics, key=lambda x: x['frequency'])
    
    def _calculate_visible_spectrum(self):
        """Calculate the visible spectrum from entropy flow qualia."""
        harmonics = []
        
        # Continuous spectrum between fundamentals
        frequencies = np.linspace(4.3e14, 7.5e14, 1000)
        
        for freq in frequencies:
            # Calculate contribution from each fundamental
            red_contrib = np.exp(-((freq - self.red_hz)/1e13)**2)
            green_contrib = np.exp(-((freq - self.green_hz)/1e13)**2)
            blue_contrib = np.exp(-((freq - self.blue_hz)/1e13)**2)
            
            total_strength = red_contrib + green_contrib + blue_contrib
            
            if total_strength > 0.01:
                harmonics.append({
                    'frequency': freq,
                    'source': 'visible_continuum',
                    'strength': total_strength,
                    'rgb': (red_contrib, green_contrib, blue_contrib)
                })
        
        return harmonics
    
    def _calculate_overtones(self, f_min, f_max):
        """Calculate overtones of visible frequencies."""
        harmonics = []
        
        # Integer multiples of fundamentals
        for n in range(2, 50):
            for fundamental, name in [(self.red_hz, 'red'),
                                     (self.green_hz, 'green'),
                                     (self.blue_hz, 'blue')]:
                freq = fundamental * n
                if f_min <= freq <= f_max:
                    harmonics.append({
                        'frequency': freq,
                        'source': f'{name}×{n}',
                        'strength': 1.0 / n**2
                    })
        
        # Sum frequencies
        freq = self.red_hz + self.green_hz
        if f_min <= freq <= f_max:
            harmonics.append({
                'frequency': freq,
                'source': 'red+green',
                'strength': 0.5
            })
            
        freq = self.red_hz + self.blue_hz
        if f_min <= freq <= f_max:
            harmonics.append({
                'frequency': freq,
                'source': 'red+blue',
                'strength': 0.5
            })
            
        freq = self.green_hz + self.blue_hz
        if f_min <= freq <= f_max:
            harmonics.append({
                'frequency': freq,
                'source': 'green+blue',
                'strength': 0.5
            })
            
        freq = self.red_hz + self.green_hz + self.blue_hz
        if f_min <= freq <= f_max:
            harmonics.append({
                'frequency': freq,
                'source': 'red+green+blue',
                'strength': 0.8
            })
        
        return sorted(harmonics, key=lambda x: x['frequency'])
    
    def _calculate_high_harmonics(self, f_min, f_max):
        """Calculate high-order harmonics for X-ray region."""
        harmonics = []
        
        # High harmonics from nonlinear mixing
        for n in range(50, 10000):
            for fundamental, name in [(self.red_hz, 'red'),
                                     (self.green_hz, 'green'),
                                     (self.blue_hz, 'blue')]:
                freq = fundamental * n
                if f_min <= freq <= f_max:
                    harmonics.append({
                        'frequency': freq,
                        'source': f'{name}×{n}',
                        'strength': 1.0 / n**3
                    })
        
        return sorted(harmonics, key=lambda x: x['frequency'])
    
    def _calculate_singularity_spectrum(self, f_min, f_max):
        """Calculate spectrum from entropy flow singularities."""
        harmonics = []
        
        # Exponential harmonics representing topological defects
        base_freqs = [self.red_hz, self.green_hz, self.blue_hz]
        
        for base, name in zip(base_freqs, ['red', 'green', 'blue']):
            n = 1
            freq = base
            while freq <= f_max and n < 100:
                freq = base * np.exp(n/10)
                if f_min <= freq <= f_max:
                    harmonics.append({
                        'frequency': freq,
                        'source': f'{name}_singularity_{n}',
                        'strength': np.exp(-n/20)
                    })
                n += 1
        
        return sorted(harmonics, key=lambda x: x['frequency'])
    
    def calculate_entropy_flow_mapping(self, frequency):
        """Calculate the entropy flow characteristics for a given frequency."""
        # Find which region the frequency belongs to
        for region_name, region_data in self.spectrum_regions.items():
            if region_data['range'][0] <= frequency <= region_data['range'][1]:
                # Calculate entropy flow parameters
                f_norm = (frequency - region_data['range'][0]) / \
                        (region_data['range'][1] - region_data['range'][0])
                
                # Entropy production rate
                if region_name == 'visible':
                    # Peak entropy production in visible region
                    entropy_rate = 1.0
                elif region_name in ['infrared', 'ultraviolet']:
                    # Moderate entropy production
                    entropy_rate = 0.7
                elif region_name in ['radio', 'microwave']:
                    # Low entropy production
                    entropy_rate = 0.3
                else:  # X-ray, gamma
                    # Extreme entropy production
                    entropy_rate = 2.0
                
                # Calculate homology class
                homology_class = self._calculate_homology_class(frequency, region_name)
                
                return {
                    'region': region_name,
                    'mechanism': region_data['mechanism'],
                    'entropy_rate': entropy_rate,
                    'homology_class': homology_class,
                    'critical_distance': abs(entropy_rate - self.lambda_critical)
                }
        
        return None
    
    def _calculate_homology_class(self, frequency, region):
        """Calculate the homology class of the entropy flow trajectory."""
        # Simplified homology calculation based on frequency ratios
        red_ratio = frequency / self.red_hz
        green_ratio = frequency / self.green_hz
        blue_ratio = frequency / self.blue_hz
        
        # Find the simplest rational approximation
        from fractions import Fraction
        
        ratios = []
        for ratio, name in [(red_ratio, 'red'), (green_ratio, 'green'), (blue_ratio, 'blue')]:
            if 0.001 < ratio < 1000:
                frac = Fraction(ratio).limit_denominator(100)
                ratios.append((name, frac))
        
        if ratios:
            # Return the simplest ratio
            simplest = min(ratios, key=lambda x: x[1].denominator)
            return f"H_1({simplest[0]}, {simplest[1]})"
        else:
            return f"H_n({region})"
    
    def visualize_spectrum(self):
        """Create a comprehensive visualization of the EM spectrum mapping."""
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(14, 10))
        
        # Main spectrum visualization
        ax1.set_xscale('log')
        ax1.set_xlim(1, 1e24)
        ax1.set_ylim(0, 2)
        ax1.set_xlabel('Frequency (Hz)')
        ax1.set_ylabel('Entropy Production Rate')
        ax1.set_title('Electromagnetic Spectrum from Entropy Flow Topology')
        
        # Color coding for regions
        colors = {
            'radio': '#8B4513',
            'microwave': '#FF8C00',
            'infrared': '#DC143C',
            'visible': '#FFFFFF',
            'ultraviolet': '#8A2BE2',
            'xray': '#4169E1',
            'gamma': '#191970'
        }
        
        # Plot each region
        for region_name, region_data in self.spectrum_regions.items():
            f_min, f_max = region_data['range']
            
            # Create gradient for visible region
            if region_name == 'visible':
                # Sample visible spectrum
                vis_freqs = np.linspace(f_min, f_max, 100)
                for i, freq in enumerate(vis_freqs[:-1]):
                    # Calculate RGB from frequency
                    wavelength = 3e8 / freq * 1e9  # nm
                    rgb = self._wavelength_to_rgb(wavelength)
                    rect = Rectangle((freq, 0), vis_freqs[i+1]-freq, 1.5,
                                   facecolor=rgb, edgecolor='none', alpha=0.8)
                    ax1.add_patch(rect)
            else:
                rect = Rectangle((f_min, 0), f_max-f_min, 1.5,
                               facecolor=colors[region_name], alpha=0.6,
                               edgecolor='black', linewidth=1)
                ax1.add_patch(rect)
            
            # Add region label
            ax1.text(np.sqrt(f_min * f_max), 1.6, region_name.upper(),
                    ha='center', va='bottom', fontsize=8, rotation=45)
        
        # Plot entropy flow strength
        frequencies = np.logspace(0, 24, 1000)
        entropy_rates = []
        
        for freq in frequencies:
            mapping = self.calculate_entropy_flow_mapping(freq)
            if mapping:
                entropy_rates.append(mapping['entropy_rate'])
            else:
                entropy_rates.append(0)
        
        ax1.plot(frequencies, entropy_rates, 'k-', linewidth=2, alpha=0.8,
                label='Entropy Production Rate')
        ax1.axhline(y=self.lambda_critical, color='red', linestyle='--',
                   label='Critical Threshold λ_c')
        ax1.legend()
        
        # Harmonic structure visualization
        ax2.set_xscale('log')
        ax2.set_xlim(1e12, 1e16)  # Focus on IR through UV
        ax2.set_ylim(0, 1)
        ax2.set_xlabel('Frequency (Hz)')
        ax2.set_ylabel('Harmonic Strength')
        ax2.set_title('Harmonic Structure of Entropy Flow Frequencies')
        
        # Plot fundamental frequencies
        ax2.axvline(x=self.red_hz, color='red', linewidth=2, alpha=0.8, label='Red Fundamental')
        ax2.axvline(x=self.green_hz, color='green', linewidth=2, alpha=0.8, label='Green Fundamental')
        ax2.axvline(x=self.blue_hz, color='blue', linewidth=2, alpha=0.8, label='Blue Fundamental')
        
        # Plot some key harmonics
        for n in range(1, 10):
            ax2.axvline(x=self.red_hz/n, color='red', linewidth=0.5, alpha=0.3)
            ax2.axvline(x=self.green_hz/n, color='green', linewidth=0.5, alpha=0.3)
            ax2.axvline(x=self.blue_hz/n, color='blue', linewidth=0.5, alpha=0.3)
            
            if n <= 3:
                ax2.axvline(x=self.red_hz*n, color='red', linewidth=0.5, alpha=0.3)
                ax2.axvline(x=self.green_hz*n, color='green', linewidth=0.5, alpha=0.3)
                ax2.axvline(x=self.blue_hz*n, color='blue', linewidth=0.5, alpha=0.3)
        
        ax2.legend()
        
        # Homology class distribution
        ax3.set_xlabel('Frequency Region')
        ax3.set_ylabel('Number of Distinct Homology Classes')
        ax3.set_title('Topological Complexity of Entropy Flow Trajectories')
        
        regions = list(self.spectrum_regions.keys())
        homology_counts = [len(self.spectrum_regions[r]['harmonics']) for r in regions]
        
        bars = ax3.bar(regions, homology_counts, color=[colors[r] for r in regions],
                       alpha=0.7, edgecolor='black')
        
        # Add value labels on bars
        for bar, count in zip(bars, homology_counts):
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height,
                    f'{count}', ha='center', va='bottom')
        
        plt.tight_layout()
        return fig
    
    def _wavelength_to_rgb(self, wavelength):
        """Convert wavelength (nm) to RGB color."""
        # Simple approximation for visible spectrum
        if wavelength < 380:
            return (0.5, 0, 0.5)  # UV - violet
        elif wavelength < 450:
            return (0.3, 0, 0.7)  # Violet
        elif wavelength < 495:
            return (0, 0, 1)      # Blue
        elif wavelength < 570:
            return (0, 1, 0)      # Green
        elif wavelength < 590:
            return (1, 1, 0)      # Yellow
        elif wavelength < 620:
            return (1, 0.5, 0)    # Orange
        elif wavelength < 750:
            return (1, 0, 0)      # Red
        else:
            return (0.5, 0, 0)    # IR - dark red
    
    def generate_frequency_table(self):
        """Generate a detailed frequency table for key wavelengths."""
        print("\nElectromagnetic Spectrum from Entropy Flow Topology")
        print("=" * 80)
        print(f"Fundamental Frequencies (from visible qualia):")
        print(f"  Red:   {self.red_hz/1e12:.1f} THz")
        print(f"  Green: {self.green_hz/1e12:.1f} THz")
        print(f"  Blue:  {self.blue_hz/1e12:.1f} THz")
        print("\n" + "-" * 80)
        print(f"{'Region':<15} {'Frequency Range':<25} {'Mechanism':<40}")
        print("-" * 80)
        
        for region_name, region_data in self.spectrum_regions.items():
            f_min, f_max = region_data['range']
            freq_str = f"{self._format_frequency(f_min)} - {self._format_frequency(f_max)}"
            mechanism = region_data['mechanism'][:38] + '..' if len(region_data['mechanism']) > 40 else region_data['mechanism']
            print(f"{region_name.upper():<15} {freq_str:<25} {mechanism:<40}")
        
        print("\n" + "-" * 80)
        print("Key Harmonic Relationships:")
        print("-" * 80)
        
        # Calculate some key relationships
        print(f"Red/2:     {self.red_hz/2/1e12:.1f} THz  (Infrared)")
        print(f"Green/2:   {self.green_hz/2/1e12:.1f} THz (Infrared)")
        print(f"Blue/2:    {self.blue_hz/2/1e12:.1f} THz (Infrared)")
        print(f"Red×2:     {self.red_hz*2/1e12:.1f} THz  (Ultraviolet)")
        print(f"Green×2:   {self.green_hz*2/1e12:.1f} THz (Ultraviolet)")
        print(f"Blue×2:    {self.blue_hz*2/1e12:.1f} THz (Ultraviolet)")
        print(f"|Blue-Red|:   {abs(self.blue_hz-self.red_hz)/1e12:.1f} THz")
        print(f"|Green-Red|:  {abs(self.green_hz-self.red_hz)/1e12:.1f} THz")
        print(f"|Blue-Green|: {abs(self.blue_hz-self.green_hz)/1e12:.1f} THz")
    
    def _format_frequency(self, freq):
        """Format frequency with appropriate units."""
        if freq < 1e3:
            return f"{freq:.1f} Hz"
        elif freq < 1e6:
            return f"{freq/1e3:.1f} kHz"
        elif freq < 1e9:
            return f"{freq/1e6:.1f} MHz"
        elif freq < 1e12:
            return f"{freq/1e9:.1f} GHz"
        elif freq < 1e15:
            return f"{freq/1e12:.1f} THz"
        elif freq < 1e18:
            return f"{freq/1e15:.1f} PHz"
        elif freq < 1e21:
            return f"{freq/1e18:.1f} EHz"
        else:
            return f"{freq/1e21:.1f} ZHz"


def main():
    """Demonstrate the EM spectrum mapping."""
    spectrum = ElectromagneticSpectrumFromEntropy()
    
    # Generate frequency table
    spectrum.generate_frequency_table()
    
    # Create visualization
    fig = spectrum.visualize_spectrum()
    plt.savefig('electromagnetic_spectrum_from_entropy.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Example: Map specific frequencies
    print("\n" + "=" * 80)
    print("Example Frequency Mappings:")
    print("=" * 80)
    
    test_frequencies = [
        (1e6, "1 MHz (Radio)"),
        (2.4e9, "2.4 GHz (WiFi)"),
        (1e12, "1 THz (Terahertz)"),
        (5e14, "500 THz (Visible)"),
        (1e18, "1 EHz (X-ray)"),
        (1e21, "1 ZHz (Gamma)")
    ]
    
    for freq, description in test_frequencies:
        mapping = spectrum.calculate_entropy_flow_mapping(freq)
        if mapping:
            print(f"\n{description}:")
            print(f"  Region: {mapping['region'].upper()}")
            print(f"  Mechanism: {mapping['mechanism']}")
            print(f"  Entropy Production Rate: {mapping['entropy_rate']:.2f}")
            print(f"  Homology Class: {mapping['homology_class']}")
            print(f"  Distance from Critical: {mapping['critical_distance']:.3f}")


if __name__ == "__main__":
    main()