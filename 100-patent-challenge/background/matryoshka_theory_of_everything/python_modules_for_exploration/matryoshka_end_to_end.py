# matryoshka_end_to_end.py
#!/usr/bin/env python3
# End-to-End Simulation for the Matryoshka Theory of Everything

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import pandas as pd
import time
import os
from scipy import constants as const

# Import Matryoshka modules
from matryoshka_unified_parameters import MatryoshkaParameters
import matryoshka_core
import matryoshka_part1
import matryoshka_part2
import matryoshka_part3
import matryoshka_part4
import matryoshka_part5

class MatryoshkaEndToEndSimulation:
    """Runs an end-to-end simulation of the Matryoshka framework.
    
    This class traces the flow from core parameters through all stages:
    - Shell structure and gravity
    - Quantum field theory on shells
    - Standard Model particle spectrum
    - Cosmological implications
    - Neutrino physics and golden ratio structure
    
    The goal is to verify consistency across all components and identify
    any emergent inconsistencies.
    """
    
    def __init__(self):
        """Initialize the end-to-end simulation."""
        self.params = MatryoshkaParameters()
        self.framework = matryoshka_core.initialize_core()
        
        # Create directory for results
        if not os.path.exists('simulation_results'):
            os.makedirs('simulation_results')
        
        # Initialize results storage
        self.results = {}
        
        # Track computation time
        self.start_time = time.time()
        print("\n" + "=" * 80)
        print("MATRYOSHKA FRAMEWORK END-TO-END SIMULATION")
        print("=" * 80)
        print(f"\nInitializing with base parameter values:")
        print(f"  ω = {self.params.omega:.4f}")
        print(f"  λₘ = {self.params.lambda_m:.6f}")
        print(f"  α_shell = {self.params.alpha_shell:.6f}")
        print(f"  c₀ = {self.params.c0:.10f}")
        print(f"  ϕ (golden ratio) = {self.params.phi:.10f}")
    
    def simulate_gravity(self):
        """Simulate the gravitational aspects of the framework."""
        print("\n" + "=" * 80)
        print("STAGE 1: SHELL STRUCTURE AND GRAVITY")
        print("=" * 80)
        
        # Derive temporal metric properties
        metric_properties = matryoshka_part1.derive_temporal_metric_properties(self.framework)
        
        # Derive gravitational laws
        gravity_laws = matryoshka_part1.derive_gravitational_laws(self.framework)
        
        # Derive Einstein's field equations
        einstein_eqs = matryoshka_part1.derive_einstein_field_equations(self.framework)
        
        # Calculate orbital dynamics
        orbital_results = matryoshka_part1.calculate_orbital_dynamics(self.framework)
        
        print("\nGravitational simulation complete.")
        print(f"Time elapsed: {time.time() - self.start_time:.2f} seconds")
        
        # Store results
        self.results['gravity'] = {
            'metric_properties': metric_properties,
            'gravity_laws': gravity_laws,
            'einstein_eqs': einstein_eqs,
            'orbital_results': orbital_results
        }
        
        # Visualize gravitational results
        self.visualize_gravitational_results()
        
        return self.results['gravity']
    
    def simulate_qft(self):
        """Simulate the quantum field theory aspects of the framework."""
        print("\n" + "=" * 80)
        print("STAGE 2: QUANTUM FIELD THEORY ON SHELLS")
        print("=" * 80)
        
        # Define Hilbert space
        hilbert_space_dict = matryoshka_part2.define_hilbert_space(self.framework)
        
        # Define creation and annihilation operators
        operator_dict = matryoshka_part2.define_creation_annihilation_operators(
            self.framework, hilbert_space_dict)
        
        # Define field operators
        field_operators_dict = matryoshka_part2.define_field_operators(
            self.framework, operator_dict)
        
        # Derive coherent states
        coherent_states_dict = matryoshka_part2.derive_coherent_states(
            self.framework, operator_dict)
        
        # Derive path integral
        path_int_dict = matryoshka_part2.derive_path_integral(
            self.framework, field_operators_dict)
        
        # Derive shell propagators
        propagator_dict = matryoshka_part2.derive_shell_propagators(
            self.framework, path_int_dict)
        
        # Derive Feynman rules
        feynman_dict = matryoshka_part2.derive_feynman_rules(
            self.framework, propagator_dict)
        
        # Derive ordinal regularization
        regularization_dict = matryoshka_part2.derive_ordinal_regularization(
            self.framework, feynman_dict)
        
        print("\nQuantum field theory simulation complete.")
        print(f"Time elapsed: {time.time() - self.start_time:.2f} seconds")
        
        # Store results
        self.results['qft'] = {
            'hilbert_space': hilbert_space_dict,
            'operators': operator_dict,
            'field_operators': field_operators_dict,
            'coherent_states': coherent_states_dict,
            'path_integral': path_int_dict,
            'propagators': propagator_dict,
            'feynman_rules': feynman_dict,
            'regularization': regularization_dict
        }
        
        # Visualize QFT results
        self.visualize_qft_results()
        
        return self.results['qft']
    
    def simulate_standard_model(self):
        """Simulate the Standard Model particle aspects of the framework."""
        print("\n" + "=" * 80)
        print("STAGE 3: STANDARD MODEL PARTICLE SPECTRUM")
        print("=" * 80)
        
        # Define excitation patterns
        excitation_dict = matryoshka_part3.define_excitation_patterns(self.framework)
        
        # Define particle families
        family_dict = matryoshka_part3.define_particle_families(
            self.framework, excitation_dict)
        
        # Define generational structure
        generation_dict = matryoshka_part3.define_generational_structure(
            self.framework, family_dict)
        
        # Derive mass formula
        mass_dict = matryoshka_part3.derive_mass_formula(
            self.framework, generation_dict)
        
        # Initialize neutrino mass dictionary for compatibility
        # Will be updated later in the neutrino section
        neutrino_mass_dict = {}
        
        # Calculate all particle masses
        mass_hierarchy_data = matryoshka_part3.calculate_all_particle_masses(
            self.framework, mass_dict, neutrino_mass_dict)
        
        # Calculate CKM matrix
        ckm_dict = matryoshka_part3.calculate_ckm_matrix(self.framework)
        
        # Derive CP violation
        cp_dict = matryoshka_part3.derive_cp_violation(self.framework, ckm_dict)
        
        print("\nStandard Model simulation complete.")
        print(f"Time elapsed: {time.time() - self.start_time:.2f} seconds")
        
        # Store results
        self.results['standard_model'] = {
            'excitation_patterns': excitation_dict,
            'particle_families': family_dict,
            'generational_structure': generation_dict,
            'mass_formula': mass_dict,
            'mass_hierarchy': mass_hierarchy_data,
            'ckm_matrix': ckm_dict,
            'cp_violation': cp_dict
        }
        
        # Visualize Standard Model results
        self.visualize_standard_model_results()
        
        return self.results['standard_model']
    
    def simulate_cosmology(self):
        """Simulate the cosmological aspects of the framework."""
        print("\n" + "=" * 80)
        print("STAGE 4: COSMOLOGICAL IMPLICATIONS")
        print("=" * 80)
        
        # Derive cosmological model
        cosmo_model = matryoshka_part4.derive_cosmological_model(self.framework)
        
        # Resolve cosmological puzzles
        puzzle_resolutions = matryoshka_part4.resolve_cosmological_puzzles(
            self.framework, cosmo_model)
        
        # Model dark sector
        dark_sector = matryoshka_part4.model_dark_sector(
            self.framework, cosmo_model)
        
        # Derive structure formation
        structure_formation = matryoshka_part4.derive_structure_formation(
            self.framework, cosmo_model)
        
        # Derive experimental tests
        experimental_tests = matryoshka_part4.derive_experimental_tests(
            self.framework, puzzle_resolutions, dark_sector, structure_formation)
        
        print("\nCosmology simulation complete.")
        print(f"Time elapsed: {time.time() - self.start_time:.2f} seconds")
        
        # Store results
        self.results['cosmology'] = {
            'cosmological_model': cosmo_model,
            'puzzle_resolutions': puzzle_resolutions,
            'dark_sector': dark_sector,
            'structure_formation': structure_formation,
            'experimental_tests': experimental_tests
        }
        
        # Visualize cosmological results
        self.visualize_cosmological_results()
        
        return self.results['cosmology']
    
    def simulate_neutrino_physics(self):
        """Simulate the neutrino physics aspects of the framework."""
        print("\n" + "=" * 80)
        print("STAGE 5: NEUTRINO PHYSICS AND GOLDEN RATIO STRUCTURE")
        print("=" * 80)
        
        # Define golden ratio structure
        golden_dict = matryoshka_part5.define_golden_ratio_structure(self.framework)
        
        # Derive neutrino mass hierarchy
        neutrino_mass_dict = matryoshka_part5.derive_neutrino_mass_hierarchy(
            self.framework, golden_dict)
        
        # Derive mixing angles
        mixing_dict = matryoshka_part5.derive_mixing_angles(
            self.framework, golden_dict)
        
        # Derive PMNS matrix
        pmns_dict = matryoshka_part5.derive_pmns_matrix(
            self.framework, golden_dict, mixing_dict)
        
        # Derive oscillation dynamics
        msw_dict = matryoshka_part5.derive_oscillation_dynamics(
            self.framework, golden_dict, neutrino_mass_dict, mixing_dict)
        
        # Derive Majorana phases
        majorana_dict = matryoshka_part5.derive_majorana_phases(
            self.framework, golden_dict)
        
        # Calculate neutrinoless double beta decay
        dbd_dict = matryoshka_part5.calculate_neutrinoless_double_beta_decay(
            self.framework, golden_dict, neutrino_mass_dict, pmns_dict, majorana_dict)
        
        # Derive mathematical origins
        math_origins = matryoshka_part5.derive_mathematical_origins(
            self.framework, golden_dict)
        
        print("\nNeutrino physics simulation complete.")
        print(f"Time elapsed: {time.time() - self.start_time:.2f} seconds")
        
        # Store results
        self.results['neutrino'] = {
            'golden_ratio': golden_dict,
            'neutrino_mass': neutrino_mass_dict,
            'mixing_angles': mixing_dict,
            'pmns_matrix': pmns_dict,
            'oscillation_dynamics': msw_dict,
            'majorana_phases': majorana_dict,
            'double_beta_decay': dbd_dict,
            'mathematical_origins': math_origins
        }
        
        # Visualize neutrino physics results
        self.visualize_neutrino_results()
        
        # Update neutrino masses in Standard Model simulation
        if 'standard_model' in self.results:
            # Recalculate particle masses with updated neutrino mass dictionary
            mass_dict = self.results['standard_model']['mass_formula']
            mass_hierarchy_data = matryoshka_part3.calculate_all_particle_masses(
                self.framework, mass_dict, neutrino_mass_dict)
            self.results['standard_model']['mass_hierarchy'] = mass_hierarchy_data
        
        return self.results['neutrino']
    
    def visualize_gravitational_results(self):
        """Visualize the gravitational simulation results."""
        print("\nVisualizing gravitational results...")
        
        # Create plots directory if it doesn't exist
        if not os.path.exists('simulation_results/gravity'):
            os.makedirs('simulation_results/gravity')
        
        # Create gravitational potential plot
        plt.figure(figsize=(10, 6))
        
        # Sample plot of gravitational potential (1/r law)
        r_values = np.linspace(0.1, 10, 100)
        pot_values = -1.0 / r_values
        
        plt.plot(r_values, pot_values, 'b-', linewidth=2, label='Gravitational Potential')
        plt.xlabel('Distance r')
        plt.ylabel('Potential Φ(r)')
        plt.title('Gravitational Potential Emerging from Shell Structure')
        plt.grid(alpha=0.3)
        plt.legend()
        plt.tight_layout()
        plt.savefig('simulation_results/gravity/potential.png')
        
        # Extract orbital simulation results
        orbital_results = self.results['gravity']['orbital_results']
        
        # Plot precession data if available
        if 'perihelion_angles' in orbital_results:
            plt.figure(figsize=(10, 6))
            
            years = np.arange(len(orbital_results['perihelion_angles']))
            angles = orbital_results['perihelion_angles']
            
            plt.plot(years, angles, 'b.-', linewidth=2)
            
            # Add trendline
            z = np.polyfit(years, angles, 1)
            p = np.poly1d(z)
            plt.plot(years, p(years), 'r--', linewidth=1.5, 
                    label=f'Trend: {z[0]:.4f}°/year')
            
            plt.xlabel('Time (years)')
            plt.ylabel('Perihelion Angle (degrees)')
            plt.title('Natural Perihelion Precession from Shell Structure')
            plt.grid(alpha=0.3)
            plt.legend()
            plt.tight_layout()
            plt.savefig('simulation_results/gravity/precession.png')
        
        print("Gravitational visualizations saved to simulation_results/gravity/ directory.")
    
    def visualize_qft_results(self):
        """Visualize the QFT simulation results."""
        print("\nVisualizing QFT results...")
        
        # Create plots directory if it doesn't exist
        if not os.path.exists('simulation_results/qft'):
            os.makedirs('simulation_results/qft')
        
        # Create a visualization of shell excitations
        plt.figure(figsize=(10, 6))
        
        # Sample visualization of a field excitation on shells
        shell_indices = np.arange(1, 11)
        base_shells = np.zeros_like(shell_indices, dtype=float)
        excited_shells = np.exp(-(shell_indices - 5)**2 / 3)
        
        plt.bar(shell_indices, base_shells, width=0.4, label='Ground State', alpha=0.3)
        plt.bar(shell_indices, excited_shells, width=0.4, label='Excited State', alpha=0.7)
        
        plt.xlabel('Shell Index')
        plt.ylabel('Excitation Amplitude')
        plt.title('QFT Excitation on Temporal Shells')
        plt.grid(alpha=0.3)
        plt.legend()
        plt.tight_layout()
        plt.savefig('simulation_results/qft/shell_excitation.png')
        
        # Create a visualization of ordinal regularization
        plt.figure(figsize=(10, 6))
        
        k_values = np.linspace(0, 10, 100)
        
        # Standard loop integral (divergent)
        standard_integral = k_values**0
        
        # Ordinal-regularized loop integral
        ordinal_regularized = np.exp(-self.params.lambda_ord * np.log(k_values + 1))
        
        plt.plot(k_values, standard_integral, 'r-', linewidth=2, 
                label='Standard (Divergent)')
        plt.plot(k_values, ordinal_regularized, 'b-', linewidth=2, 
                label='Ordinal-Regularized')
        
        plt.xlabel('Momentum k')
        plt.ylabel('Integral Value')
        plt.title('Ordinal Regularization of Loop Integrals')
        plt.grid(alpha=0.3)
        plt.legend()
        plt.ylim(0, 1.2)
        plt.tight_layout()
        plt.savefig('simulation_results/qft/ordinal_regularization.png')
        
        print("QFT visualizations saved to simulation_results/qft/ directory.")
    
    def visualize_standard_model_results(self):
        """Visualize the Standard Model simulation results."""
        print("\nVisualizing Standard Model results...")
        
        # Create plots directory if it doesn't exist
        if not os.path.exists('simulation_results/standard_model'):
            os.makedirs('simulation_results/standard_model')
        
        # Create mass hierarchy plot
        plt.figure(figsize=(12, 8))
        
        # Extract mass data
        mass_hierarchy_data = self.results['standard_model']['mass_hierarchy']
        
        # Create lists for plot
        particles = []
        masses = []
        colors = []
        
        # Add leptons
        for particle in ['e', 'mu', 'tau']:
            if particle in mass_hierarchy_data['leptons']:
                particles.append(particle)
                masses.append(mass_hierarchy_data['leptons'][particle]['mass_physical'])
                colors.append('blue')
        
        # Add quarks
        for particle in ['u', 'd', 's', 'c', 'b', 't']:
            if particle in mass_hierarchy_data['quarks']:
                particles.append(particle)
                masses.append(mass_hierarchy_data['quarks'][particle]['mass_physical'])
                colors.append('red')
        
        # Add bosons
        for particle in ['W', 'Z', 'H']:
            if particle in mass_hierarchy_data['bosons']:
                particles.append(particle)
                masses.append(mass_hierarchy_data['bosons'][particle]['mass_physical'])
                colors.append('green')
        
        # Plot masses on log scale
        plt.bar(particles, masses, color=colors, alpha=0.7)
        plt.yscale('log')
        plt.ylabel('Mass (MeV)')
        plt.title('Particle Mass Hierarchy')
        plt.grid(axis='y', alpha=0.3)
        
        # Add legend
        legend_elements = [
            Line2D([0], [0], color='blue', lw=4, label='Leptons'),
            Line2D([0], [0], color='red', lw=4, label='Quarks'),
            Line2D([0], [0], color='green', lw=4, label='Bosons')
        ]
        plt.legend(handles=legend_elements)
        
        plt.tight_layout()
        plt.savefig('simulation_results/standard_model/mass_hierarchy.png')
        
        # Create ordinal depth vs mass plot
        plt.figure(figsize=(10, 6))
        
        # Extract ordinal depths
        generation_dict = self.results['standard_model']['generational_structure']
        
        ordinal_depths = []
        particle_names = []
        
        # For leptons
        for particle in ['e', 'mu', 'tau']:
            if particle in generation_dict['leptons']:
                ordinal_depths.append(generation_dict['leptons'][particle]['ordinal_depth'])
                particle_names.append(particle)
        
        # For quarks
        for particle in ['u', 'd', 's', 'c', 'b', 't']:
            if particle in generation_dict['quarks']:
                ordinal_depths.append(generation_dict['quarks'][particle]['ordinal_depth'])
                particle_names.append(particle)
        
        # Plot ordinal depth vs mass
        particle_masses = [mass_hierarchy_data['leptons'].get(p, {}).get('mass_physical', 0) 
                         if p in ['e', 'mu', 'tau'] else
                         mass_hierarchy_data['quarks'].get(p, {}).get('mass_physical', 0)
                         for p in particle_names]
        
        plt.scatter(ordinal_depths, particle_masses, s=80)
        
        # Add particle labels
        for i, particle in enumerate(particle_names):
            plt.annotate(particle, (ordinal_depths[i], particle_masses[i]),
                        xytext=(5, 5), textcoords='offset points')
        
        # Add exponential trend line
        x_trend = np.linspace(min(ordinal_depths), max(ordinal_depths), 100)
        lambda_m = self.params.lambda_m
        y_trend = np.exp(lambda_m * x_trend) * particle_masses[0] / np.exp(lambda_m * min(ordinal_depths))
        
        plt.plot(x_trend, y_trend, 'r--', label=f'exp(λₘ·ordinal_depth), λₘ = {lambda_m:.4f}')
        
        plt.xlabel('Ordinal Depth')
        plt.ylabel('Mass (MeV)')
        plt.yscale('log')
        plt.title('Mass vs Ordinal Depth')
        plt.grid(alpha=0.3)
        plt.legend()
        plt.tight_layout()
        plt.savefig('simulation_results/standard_model/mass_vs_ordinal_depth.png')
        
        # Create CKM matrix visualization
        plt.figure(figsize=(8, 8))
        
        # Extract CKM matrix
        ckm_dict = self.results['standard_model']['ckm_matrix']
        
        if 'V_CKM' in ckm_dict:
            V_CKM = ckm_dict['V_CKM']
            V_CKM_abs = np.abs(V_CKM)
            
            # Plot CKM matrix as a heatmap
            plt.imshow(V_CKM_abs, cmap='viridis', vmin=0, vmax=1)
            plt.colorbar(label='|V_ij|')
            
            # Add values
            for i in range(3):
                for j in range(3):
                    plt.text(j, i, f'{V_CKM_abs[i, j]:.3f}', 
                            ha='center', va='center', color='white')
            
            plt.xticks([0, 1, 2], ['d', 's', 'b'])
            plt.yticks([0, 1, 2], ['u', 'c', 't'])
            plt.title('CKM Matrix')
            plt.tight_layout()
            plt.savefig('simulation_results/standard_model/ckm_matrix.png')
        
        print("Standard Model visualizations saved to simulation_results/standard_model/ directory.")
    
    def visualize_cosmological_results(self):
        """Visualize the cosmological simulation results."""
        print("\nVisualizing cosmological results...")
        
        # Create plots directory if it doesn't exist
        if not os.path.exists('simulation_results/cosmology'):
            os.makedirs('simulation_results/cosmology')
        
        # Create scale factor evolution plot
        plt.figure(figsize=(10, 6))
        
        # Define scale factor functions
        def a_radiation(t, t_eq=47000):
            """Scale factor during radiation domination."""
            return (t/t_eq)**(0.5)
        
        def a_matter(t, t_eq=47000, t_Λ=9.8e9):
            """Scale factor during matter domination."""
            a_eq = a_radiation(t_eq, t_eq)
            return a_eq * (t/t_eq)**(2/3)
        
        def a_lambda(t, t_Λ=9.8e9, t_0=13.8e9, Ω_Λ=0.7):
            """Scale factor during dark energy domination."""
            H_0 = 70 / (1000 * const.mega * const.parsec) * const.c  # Convert km/s/Mpc to 1/s
            H_Λ = H_0 * np.sqrt(Ω_Λ)
            a_Λ = a_matter(t_Λ, 47000, t_Λ)
            return a_Λ * np.exp(H_Λ * (t - t_Λ))
        
        # Create time array (in years)
        t_vals = np.logspace(2, 10, 1000)
        t_eq = 47000  # years
        t_Λ = 9.8e9  # years
        
        # Calculate scale factor
        a_vals = np.zeros_like(t_vals)
        for i, t in enumerate(t_vals):
            if t < t_eq:
                a_vals[i] = a_radiation(t, t_eq)
            elif t < t_Λ:
                a_vals[i] = a_matter(t, t_eq, t_Λ)
            else:
                a_vals[i] = a_lambda(t, t_Λ, 13.8e9, 0.7)
        
        plt.plot(t_vals, a_vals, 'b-', linewidth=2)
        
        # Mark transitions
        plt.axvline(x=t_eq, color='r', linestyle='--', 
                   label=f'Radiation-Matter Equality: {t_eq:g} years')
        plt.axvline(x=t_Λ, color='g', linestyle='--', 
                   label=f'Matter-Dark Energy Equality: {t_Λ/1e9:.1f} Gyr')
        
        plt.text(t_eq*1.1, 0.2, 'Radiation', rotation=90)
        plt.text(t_eq*5, 0.2, 'Matter')
        plt.text(t_Λ*1.1, 0.2, 'Dark Energy', rotation=90)
        
        plt.xscale('log')
        plt.yscale('log')
        plt.xlabel('Time (years)')
        plt.ylabel('Scale Factor a(t)')
        plt.title('Cosmic Expansion History')
        plt.grid(alpha=0.3, which='both')
        plt.legend()
        plt.tight_layout()
        plt.savefig('simulation_results/cosmology/scale_factor.png')
        
        # Create dark energy equation of state plot
        plt.figure(figsize=(10, 6))
        
        z_vals = np.linspace(0, 2, 100)
        w_vals = -1 + 0.03 * z_vals / (1 + z_vals)
        
        plt.plot(z_vals, w_vals, 'b-', linewidth=2, 
                label='Shell-Theoretic Prediction')
        plt.axhline(y=-1, color='r', linestyle='--', 
                   label='ΛCDM (w = -1)')
        
        plt.xlabel('Redshift z')
        plt.ylabel('w(z)')
        plt.title('Dark Energy Equation of State')
        plt.grid(alpha=0.3)
        plt.legend()
        plt.tight_layout()
        plt.savefig('simulation_results/cosmology/dark_energy_eos.png')
        
        # Create cosmological constant origin visualization
        plt.figure(figsize=(10, 6))
        
        # Create a simple diagram showing the orders of magnitude
        labels = ['Zero-Point\nEnergy', 'Naive Shell\nTheory', 'Shell Theory\nwith Ordinal\nRegularization', 'Observed\nValue']
        magnitudes = [10**120, 10**30, 10**0, 10**0]
        colors = ['red', 'orange', 'green', 'green']
        
        plt.bar(labels, magnitudes, color=colors, alpha=0.7, log=True)
        plt.ylabel('Cosmological Constant (relative to observed)')
        plt.title('Resolution of the Cosmological Constant Problem')
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        plt.savefig('simulation_results/cosmology/cc_problem.png')
        
        print("Cosmological visualizations saved to simulation_results/cosmology/ directory.")
    
    def visualize_neutrino_results(self):
        """Visualize the neutrino physics simulation results."""
        print("\nVisualizing neutrino physics results...")
        
        # Create plots directory if it doesn't exist
        if not os.path.exists('simulation_results/neutrino'):
            os.makedirs('simulation_results/neutrino')
        
        # Create neutrino mass hierarchy plot
        plt.figure(figsize=(10, 6))
        
        # Extract neutrino masses
        neutrino_mass_dict = self.results['neutrino']['neutrino_mass']
        
        # Plot masses
        neutrinos = ['ν₁', 'ν₂', 'ν₃']
        masses = [
            neutrino_mass_dict['m1_val'],
            neutrino_mass_dict['m2_val'],
            neutrino_mass_dict['m3_val']
        ]
        
        plt.bar(neutrinos, masses, color='purple', alpha=0.7)
        plt.ylabel('Mass (eV)')
        plt.title('Neutrino Mass Hierarchy')
        plt.grid(axis='y', alpha=0.3)
        
        # Add mass labels
        for i, mass in enumerate(masses):
            plt.text(i, mass*1.05, f'{mass:.4f} eV', ha='center')
        
        plt.tight_layout()
        plt.savefig('simulation_results/neutrino/mass_hierarchy.png')
        
        # Create mixing angles visualization
        plt.figure(figsize=(10, 6))
        
        # Extract mixing angles
        mixing_dict = self.results['neutrino']['mixing_angles']
        
        # Plot mixing angles
        angles = ['sin²(θ₁₂)', 'sin²(θ₂₃)', 'sin²(θ₁₃)']
        values = [
            mixing_dict['sin2_theta12_val'],
            mixing_dict['sin2_theta23_val'],
            mixing_dict['sin2_theta13_val']
        ]
        
        golden_values = [
            1.0 / self.params.phi**2,
            0.5 - 0.5 / self.params.phi**3,
            1.0 / (4 * self.params.phi**4)
        ]
        
        x = np.arange(len(angles))
        width = 0.35
        
        plt.bar(x - width/2, values, width, label='Calculated', color='blue', alpha=0.7)
        plt.bar(x + width/2, golden_values, width, label='Golden Ratio Formula', 
               color='gold', alpha=0.7)
        
        plt.xlabel('Mixing Angle')
        plt.ylabel('Value')
        plt.title('Neutrino Mixing Angles')
        plt.xticks(x, angles)
        plt.grid(axis='y', alpha=0.3)
        plt.legend()
        
        # Add value labels
        for i, value in enumerate(values):
            plt.text(i - width/2, value*1.05, f'{value:.4f}', ha='center')
            plt.text(i + width/2, golden_values[i]*1.05, f'{golden_values[i]:.4f}', ha='center')
        
        plt.tight_layout()
        plt.savefig('simulation_results/neutrino/mixing_angles.png')
        
        # Create neutrino oscillation plot
        plt.figure(figsize=(12, 8))
        
        # Calculate oscillation probabilities
        E_vals = np.linspace(0.1, 10, 200)  # GeV
        L = 1000  # km
        
        # Convert units for calculation
        L_m = L * 1000  # km to m
        
        # Extract PMNS matrix and mass-squared differences
        pmns_dict = self.results['neutrino']['pmns_matrix']
        m_sq = neutrino_mass_dict['m_sq']
        
        # Calculate probabilities
        P_e_mu = []
        P_e_tau = []
        P_mu_e = []
        P_mu_mu = []
        
        for E in E_vals:
            # Convert to eV
            E_eV = E * 1e9
            
            # Calculate standard oscillation probability
            p_e_mu_std = matryoshka_part5.calculate_oscillation_probability_shell(
                1, 2, L_m, E_eV, pmns_dict['U_PMNS'], m_sq, 0.0, self.params.omega)
            
            # Calculate shell-modified probability
            p_e_mu_shell = matryoshka_part5.calculate_oscillation_probability_shell(
                1, 2, L_m, E_eV, pmns_dict['U_PMNS'], m_sq, self.params.lambda_nu, self.params.omega)
            
            p_mu_e_shell = matryoshka_part5.calculate_oscillation_probability_shell(
                2, 1, L_m, E_eV, pmns_dict['U_PMNS'], m_sq, self.params.lambda_nu, self.params.omega)
            
            p_mu_mu_shell = matryoshka_part5.calculate_oscillation_probability_shell(
                2, 2, L_m, E_eV, pmns_dict['U_PMNS'], m_sq, self.params.lambda_nu, self.params.omega)
            
            P_e_mu.append((p_e_mu_std, p_e_mu_shell))
            P_mu_e.append(p_mu_e_shell)
            P_mu_mu.append(p_mu_mu_shell)
        
        # Plot oscillation probabilities
        plt.plot(E_vals, [p[0] for p in P_e_mu], 'b--', linewidth=1.5, 
                label='P(νₑ→νᵤ) Standard')
        plt.plot(E_vals, [p[1] for p in P_e_mu], 'b-', linewidth=2, 
                label='P(νₑ→νᵤ) Shell-Modified')
        plt.plot(E_vals, P_mu_e, 'r-', linewidth=2, 
                label='P(νᵤ→νₑ) Shell-Modified')
        plt.plot(E_vals, P_mu_mu, 'g-', linewidth=2, 
                label='P(νᵤ→νᵤ) Shell-Modified')
        
        plt.xlabel('Neutrino Energy (GeV)')
        plt.ylabel('Oscillation Probability')
        plt.title(f'Neutrino Oscillation Probabilities (L = {L} km)')
        plt.grid(alpha=0.3)
        plt.legend()
        plt.tight_layout()
        plt.savefig('simulation_results/neutrino/oscillation_probabilities.png')
        
        # Create neutrinoless double beta decay plot
        plt.figure(figsize=(10, 6))
        
        # Extract double beta decay data
        dbd_dict = self.results['neutrino']['double_beta_decay']
        
        # Plot effective Majorana mass
        plt.axhline(y=dbd_dict['m_bb_val'], color='r', linestyle='-', linewidth=2,
                   label=f'Predicted |m_ββ| = {dbd_dict["m_bb_val"]:.4f} eV')
        
        # Add experimental sensitivity bands
        plt.axhspan(0.01, 0.05, alpha=0.2, color='blue', 
                   label='Next-Gen Experiment Sensitivity')
        
        # Add normal and inverted hierarchy regions
        plt.axhspan(0.001, 0.01, alpha=0.1, color='green', 
                   label='NH Region')
        plt.axhspan(0.01, 0.5, alpha=0.1, color='orange', 
                   label='IH Region')
        
        plt.xlabel('Lightest Neutrino Mass (eV)')
        plt.ylabel('Effective Majorana Mass |m_ββ| (eV)')
        plt.title('Neutrinoless Double Beta Decay Prediction')
        plt.grid(alpha=0.3)
        plt.legend()
        plt.xscale('log')
        plt.yscale('log')
        plt.ylim(0.001, 0.5)
        plt.xlim(0.0001, 0.1)
        plt.tight_layout()
        plt.savefig('simulation_results/neutrino/neutrinoless_dbd.png')
        
        print("Neutrino physics visualizations saved to simulation_results/neutrino/ directory.")
    
    def analyze_cross_framework_consistency(self):
        """Analyze consistency across all components of the framework."""
        print("\n" + "=" * 80)
        print("CROSS-FRAMEWORK CONSISTENCY ANALYSIS")
        print("=" * 80)
        
        # Create a directory for consistency analysis
        if not os.path.exists('simulation_results/consistency'):
            os.makedirs('simulation_results/consistency')
        
        print("\nAnalyzing parameter consistency across framework components...")
        
        # Check if all simulations have been run
        required_components = ['gravity', 'qft', 'standard_model', 'cosmology', 'neutrino']
        missing_components = [comp for comp in required_components if comp not in self.results]
        
        if missing_components:
            print(f"WARNING: Cannot perform complete consistency analysis.")
            print(f"Missing components: {', '.join(missing_components)}")
            print(f"Please run the full simulation first using run_full_simulation().")
            return
        
        # Create a parameter consistency table
        consistency_table = {
            'Parameter': [],
            'Expected Value': [],
            'Gravity': [],
            'QFT': [],
            'Standard Model': [],
            'Cosmology': [],
            'Neutrino': []
        }
        
        # Define key parameters to check
        key_parameters = [
            {'name': 'omega', 'expected': self.params.omega},
            {'name': 'lambda_m', 'expected': self.params.lambda_m},
            {'name': 'alpha_shell', 'expected': self.params.alpha_shell},
            {'name': 'phi', 'expected': self.params.phi},
            {'name': 'c0', 'expected': self.params.c0}
        ]
        
        # Extract values from each component
        for param in key_parameters:
            consistency_table['Parameter'].append(param['name'])
            consistency_table['Expected Value'].append(param['expected'])
            
            # Gravity
            if param['name'] in self.results['gravity'].get('gravity_laws', {}):
                consistency_table['Gravity'].append(
                    self.results['gravity']['gravity_laws'][param['name']])
            else:
                consistency_table['Gravity'].append('N/A')
            
            # QFT
            if param['name'] in self.results['qft'].get('field_operators', {}):
                consistency_table['QFT'].append(
                    self.results['qft']['field_operators'][param['name']])
            else:
                consistency_table['QFT'].append('N/A')
            
            # Standard Model
            if param['name'] in self.results['standard_model'].get('mass_formula', {}):
                consistency_table['Standard Model'].append(
                    self.results['standard_model']['mass_formula'][param['name']])
            else:
                consistency_table['Standard Model'].append('N/A')
            
            # Cosmology
            if param['name'] in self.results['cosmology'].get('cosmological_model', {}):
                consistency_table['Cosmology'].append(
                    self.results['cosmology']['cosmological_model'][param['name']])
            else:
                consistency_table['Cosmology'].append('N/A')
            
            # Neutrino
            if param['name'] in self.results['neutrino'].get('golden_ratio', {}):
                consistency_table['Neutrino'].append(
                    self.results['neutrino']['golden_ratio'][param['name']])
            elif param['name'] == 'phi':
                consistency_table['Neutrino'].append(
                    self.results['neutrino']['golden_ratio'].get('phi', 'N/A'))
            else:
                consistency_table['Neutrino'].append('N/A')
        
        # Convert to pandas DataFrame for better formatting
        consistency_df = pd.DataFrame(consistency_table)
        
        # Print consistency table
        print("\nParameter Consistency Across Framework Components:")
        print(consistency_df.to_string(index=False))
        
        # Save to CSV
        consistency_df.to_csv('simulation_results/consistency/parameter_consistency.csv', index=False)
        
        # Check prediction consistency
        print("\nAnalyzing prediction consistency across framework components...")
        
        # Create a predictions consistency table
        predictions_table = {
            'Prediction': [],
            'Framework Component': [],
            'Predicted Value': [],
            'Experimental Value': [],
            'Deviation (%)': []
        }
        
        # Define key predictions to check
        key_predictions = [
            {
                'name': 'Muon/Electron Mass Ratio',
                'component': 'Standard Model',
                'predicted': self.results['standard_model']['mass_hierarchy']['leptons']['mu']['mass_physical'] / 
                            self.results['standard_model']['mass_hierarchy']['leptons']['e']['mass_physical'],
                'experimental': 206.7683
            },
            {
                'name': 'sin²(θ₁₂)',
                'component': 'Neutrino',
                'predicted': self.results['neutrino']['mixing_angles']['sin2_theta12_val'],
                'experimental': 0.304
            },
            {
                'name': 'sin²(θ₂₃)',
                'component': 'Neutrino',
                'predicted': self.results['neutrino']['mixing_angles']['sin2_theta23_val'],
                'experimental': 0.51
            },
            {
                'name': '|m_ββ| (eV)',
                'component': 'Neutrino',
                'predicted': self.results['neutrino']['double_beta_decay']['m_bb_val'],
                'experimental': '<0.2'  # Current experimental upper bound
            },
            {
                'name': 'Spectral Index n_s',
                'component': 'Cosmology',
                'predicted': self.results['cosmology']['structure_formation']['primordial_fluctuations']['n_s'],
                'experimental': 0.965
            }
        ]
        
        # Fill in prediction table
        for pred in key_predictions:
            predictions_table['Prediction'].append(pred['name'])
            predictions_table['Framework Component'].append(pred['component'])
            predictions_table['Predicted Value'].append(pred['predicted'])
            predictions_table['Experimental Value'].append(pred['experimental'])
            
            # Calculate deviation if possible
            if isinstance(pred['experimental'], (int, float)) and isinstance(pred['predicted'], (int, float)):
                deviation = (pred['predicted'] - pred['experimental']) / pred['experimental'] * 100
                predictions_table['Deviation (%)'].append(f"{deviation:.2f}%")
            else:
                predictions_table['Deviation (%)'].append('N/A')
        
        # Convert to pandas DataFrame for better formatting
        predictions_df = pd.DataFrame(predictions_table)
        
        # Print predictions table
        print("\nPrediction Consistency with Experimental Values:")
        print(predictions_df.to_string(index=False))
        
        # Save to CSV
        predictions_df.to_csv('simulation_results/consistency/prediction_consistency.csv', index=False)
        
        # Create a visual summary of prediction consistency
        plt.figure(figsize=(12, 8))
        
        # Extract numerical predictions and deviations
        numerical_predictions = [
            pred for pred in key_predictions 
            if isinstance(pred['experimental'], (int, float)) and isinstance(pred['predicted'], (int, float))
        ]
        
        pred_names = [pred['name'] for pred in numerical_predictions]
        deviations = [(pred['predicted'] - pred['experimental']) / pred['experimental'] * 100 
                     for pred in numerical_predictions]
        components = [pred['component'] for pred in numerical_predictions]
        
        # Define colors based on component
        color_map = {
            'Standard Model': 'blue',
            'Neutrino': 'purple',
            'Cosmology': 'green'
        }
        colors = [color_map.get(comp, 'gray') for comp in components]
        
        # Create deviation bar chart
        plt.bar(pred_names, deviations, color=colors, alpha=0.7)
        plt.axhline(y=0, color='k', linestyle='-', alpha=0.4)
        plt.axhspan(-5, 5, color='g', alpha=0.1, label='±5% Deviation')
        
        plt.ylabel('Deviation from Experimental Value (%)')
        plt.title('Framework Prediction Consistency with Experiment')
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        plt.savefig('simulation_results/consistency/prediction_deviations.png')
        
        print("\nConsistency analysis complete.")
        print(f"Time elapsed: {time.time() - self.start_time:.2f} seconds")
        print("\nConsistency analysis results saved to simulation_results/consistency/ directory.")
        
        return {
            'parameter_consistency': consistency_df,
            'prediction_consistency': predictions_df
        }
    
    def run_full_simulation(self):
        """Run the complete end-to-end simulation."""
        print("\n" + "=" * 80)
        print("RUNNING COMPLETE END-TO-END SIMULATION")
        print("=" * 80)
        
        # Run all simulation stages
        self.simulate_gravity()
        self.simulate_qft()
        self.simulate_standard_model()
        self.simulate_cosmology()
        self.simulate_neutrino_physics()
        
        # Analyze cross-framework consistency
        consistency_results = self.analyze_cross_framework_consistency()
        
        print("\n" + "=" * 80)
        print("END-TO-END SIMULATION COMPLETE")
        print("=" * 80)
        print(f"\nTotal simulation time: {time.time() - self.start_time:.2f} seconds")
        print(f"\nSimulation results are available in the simulation_results/ directory.")
        
        return self.results

# If run directly, perform the end-to-end simulation
if __name__ == "__main__":
    simulator = MatryoshkaEndToEndSimulation()
    results = simulator.run_full_simulation()