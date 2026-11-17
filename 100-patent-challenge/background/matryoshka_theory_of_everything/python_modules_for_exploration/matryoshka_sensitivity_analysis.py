# matryoshka_sensitivity_analysis.py
#!/usr/bin/env python3
# Sensitivity Analysis for Matryoshka Theory of Everything

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
import pandas as pd
import time

# Import Matryoshka modules
from matryoshka_unified_parameters import MatryoshkaParameters
import matryoshka_core
import matryoshka_part3
import matryoshka_part4
import matryoshka_part5

class MatryoshkaSensitivityAnalysis:
    """Performs sensitivity analysis on key Matryoshka framework predictions."""
    
    def __init__(self):
        """Initialize the sensitivity analysis environment."""
        self.params = MatryoshkaParameters()
        self.framework = matryoshka_core.initialize_core()
        
        # Parameter ranges for sensitivity analysis (percentage variations)
        self.variation_range = np.linspace(-10, 10, 21)  # -10% to +10%
        
        # Initialize sensitivity results storage
        self.results = {}
        
        # Track computation time
        self.start_time = time.time()
        print("\n" + "=" * 80)
        print("MATRYOSHKA FRAMEWORK SENSITIVITY ANALYSIS")
        print("=" * 80)
        print(f"\nInitializing with base parameter values:")
        print(f"  ω = {self.params.omega:.4f}")
        print(f"  λₘ = {self.params.lambda_m:.6f}")
        print(f"  α_shell = {self.params.alpha_shell:.6f}")
        print(f"  c₀ = {self.params.c0:.10f}")
        print(f"  ϕ (golden ratio) = {self.params.phi:.10f}")
    
    def analyze_neutrino_sensitivity(self):
        """Analyze sensitivity of neutrino predictions to parameter variations."""
        print("\n" + "=" * 80)
        print("NEUTRINO PHYSICS SENSITIVITY ANALYSIS")
        print("=" * 80)
        
        # Initialize golden ratio structure (Part 5)
        golden_dict = matryoshka_part5.define_golden_ratio_structure(self.framework)
        
        # Initialize neutrino mass hierarchy
        neutrino_mass_dict = matryoshka_part5.derive_neutrino_mass_hierarchy(
            self.framework, golden_dict)
        
        # Initialize mixing angles
        mixing_dict = matryoshka_part5.derive_mixing_angles(
            self.framework, golden_dict)
        
        # Initialize PMNS matrix
        pmns_dict = matryoshka_part5.derive_pmns_matrix(
            self.framework, golden_dict, mixing_dict)
        
        # Initialize Majorana phases
        majorana_dict = matryoshka_part5.derive_majorana_phases(
            self.framework, golden_dict)
        
        # Initialize neutrinoless double beta decay prediction
        dbd_dict = matryoshka_part5.calculate_neutrinoless_double_beta_decay(
            self.framework, golden_dict, neutrino_mass_dict, pmns_dict, majorana_dict)
        
        print("\nAnalyzing sensitivity of neutrino predictions to parameter variations...")
        
        # Store base predictions
        base_predictions = {
            'm1': neutrino_mass_dict['m1_val'],
            'm2': neutrino_mass_dict['m2_val'],
            'm3': neutrino_mass_dict['m3_val'],
            'sum_m': neutrino_mass_dict['m1_val'] + neutrino_mass_dict['m2_val'] + neutrino_mass_dict['m3_val'],
            'sin2_theta12': mixing_dict['sin2_theta12_val'],
            'sin2_theta23': mixing_dict['sin2_theta23_val'],
            'sin2_theta13': mixing_dict['sin2_theta13_val'],
            'm_bb': dbd_dict['m_bb_val']
        }
        
        print("\nBase predictions:")
        for key, value in base_predictions.items():
            print(f"  {key} = {value:.6f}")
        
        # Create storage for sensitivity results
        sensitivity = {
            'omega': {pred: [] for pred in base_predictions},
            'lambda_nu': {pred: [] for pred in base_predictions},
            'phi': {pred: [] for pred in base_predictions}
        }
        
        # Analyze omega sensitivity
        for var in self.variation_range:
            # Create modified framework with varied omega
            modified_framework = self.framework.copy()
            modified_framework['parameters']['omega'] = self.params.omega * (1 + var/100)
            
            # Recalculate predictions
            golden_dict_mod = matryoshka_part5.define_golden_ratio_structure(modified_framework)
            neutrino_mass_dict_mod = matryoshka_part5.derive_neutrino_mass_hierarchy(
                modified_framework, golden_dict_mod)
            mixing_dict_mod = matryoshka_part5.derive_mixing_angles(
                modified_framework, golden_dict_mod)
            pmns_dict_mod = matryoshka_part5.derive_pmns_matrix(
                modified_framework, golden_dict_mod, mixing_dict_mod)
            majorana_dict_mod = matryoshka_part5.derive_majorana_phases(
                modified_framework, golden_dict_mod)
            dbd_dict_mod = matryoshka_part5.calculate_neutrinoless_double_beta_decay(
                modified_framework, golden_dict_mod, neutrino_mass_dict_mod, 
                pmns_dict_mod, majorana_dict_mod)
            
            # Store results
            sensitivity['omega']['m1'].append(neutrino_mass_dict_mod['m1_val'])
            sensitivity['omega']['m2'].append(neutrino_mass_dict_mod['m2_val'])
            sensitivity['omega']['m3'].append(neutrino_mass_dict_mod['m3_val'])
            sensitivity['omega']['sum_m'].append(
                neutrino_mass_dict_mod['m1_val'] + 
                neutrino_mass_dict_mod['m2_val'] + 
                neutrino_mass_dict_mod['m3_val'])
            sensitivity['omega']['sin2_theta12'].append(mixing_dict_mod['sin2_theta12_val'])
            sensitivity['omega']['sin2_theta23'].append(mixing_dict_mod['sin2_theta23_val'])
            sensitivity['omega']['sin2_theta13'].append(mixing_dict_mod['sin2_theta13_val'])
            sensitivity['omega']['m_bb'].append(dbd_dict_mod['m_bb_val'])
        
        # Analyze lambda_nu sensitivity
        for var in self.variation_range:
            # Create modified framework with varied lambda_nu
            modified_framework = self.framework.copy()
            modified_framework['parameters']['lambda_nu'] = self.params.lambda_nu * (1 + var/100)
            
            # Recalculate predictions
            golden_dict_mod = matryoshka_part5.define_golden_ratio_structure(modified_framework)
            neutrino_mass_dict_mod = matryoshka_part5.derive_neutrino_mass_hierarchy(
                modified_framework, golden_dict_mod)
            mixing_dict_mod = matryoshka_part5.derive_mixing_angles(
                modified_framework, golden_dict_mod)
            pmns_dict_mod = matryoshka_part5.derive_pmns_matrix(
                modified_framework, golden_dict_mod, mixing_dict_mod)
            majorana_dict_mod = matryoshka_part5.derive_majorana_phases(
                modified_framework, golden_dict_mod)
            dbd_dict_mod = matryoshka_part5.calculate_neutrinoless_double_beta_decay(
                modified_framework, golden_dict_mod, neutrino_mass_dict_mod, 
                pmns_dict_mod, majorana_dict_mod)
            
            # Store results
            sensitivity['lambda_nu']['m1'].append(neutrino_mass_dict_mod['m1_val'])
            sensitivity['lambda_nu']['m2'].append(neutrino_mass_dict_mod['m2_val'])
            sensitivity['lambda_nu']['m3'].append(neutrino_mass_dict_mod['m3_val'])
            sensitivity['lambda_nu']['sum_m'].append(
                neutrino_mass_dict_mod['m1_val'] + 
                neutrino_mass_dict_mod['m2_val'] + 
                neutrino_mass_dict_mod['m3_val'])
            sensitivity['lambda_nu']['sin2_theta12'].append(mixing_dict_mod['sin2_theta12_val'])
            sensitivity['lambda_nu']['sin2_theta23'].append(mixing_dict_mod['sin2_theta23_val'])
            sensitivity['lambda_nu']['sin2_theta13'].append(mixing_dict_mod['sin2_theta13_val'])
            sensitivity['lambda_nu']['m_bb'].append(dbd_dict_mod['m_bb_val'])
        
        # Analyze phi sensitivity
        for var in self.variation_range:
            # Create modified framework with varied phi
            modified_framework = self.framework.copy()
            golden_dict_mod = golden_dict.copy()
            golden_dict_mod['phi'] = self.params.phi * (1 + var/100)
            
            # Recalculate predictions
            neutrino_mass_dict_mod = matryoshka_part5.derive_neutrino_mass_hierarchy(
                modified_framework, golden_dict_mod)
            mixing_dict_mod = matryoshka_part5.derive_mixing_angles(
                modified_framework, golden_dict_mod)
            pmns_dict_mod = matryoshka_part5.derive_pmns_matrix(
                modified_framework, golden_dict_mod, mixing_dict_mod)
            majorana_dict_mod = matryoshka_part5.derive_majorana_phases(
                modified_framework, golden_dict_mod)
            dbd_dict_mod = matryoshka_part5.calculate_neutrinoless_double_beta_decay(
                modified_framework, golden_dict_mod, neutrino_mass_dict_mod, 
                pmns_dict_mod, majorana_dict_mod)
            
            # Store results
            sensitivity['phi']['m1'].append(neutrino_mass_dict_mod['m1_val'])
            sensitivity['phi']['m2'].append(neutrino_mass_dict_mod['m2_val'])
            sensitivity['phi']['m3'].append(neutrino_mass_dict_mod['m3_val'])
            sensitivity['phi']['sum_m'].append(
                neutrino_mass_dict_mod['m1_val'] + 
                neutrino_mass_dict_mod['m2_val'] + 
                neutrino_mass_dict_mod['m3_val'])
            sensitivity['phi']['sin2_theta12'].append(mixing_dict_mod['sin2_theta12_val'])
            sensitivity['phi']['sin2_theta23'].append(mixing_dict_mod['sin2_theta23_val'])
            sensitivity['phi']['sin2_theta13'].append(mixing_dict_mod['sin2_theta13_val'])
            sensitivity['phi']['m_bb'].append(dbd_dict_mod['m_bb_val'])
        
        # Calculate sensitivities (percentage change)
        relative_sensitivity = {}
        for param in sensitivity:
            relative_sensitivity[param] = {}
            for pred in base_predictions:
                relative_values = np.array(sensitivity[param][pred]) / base_predictions[pred]
                relative_sensitivity[param][pred] = relative_values
        
        # Store results
        self.results['neutrino'] = {
            'base_predictions': base_predictions,
            'sensitivity': sensitivity,
            'relative_sensitivity': relative_sensitivity
        }
        
        print("\nNeutrino sensitivity analysis complete.")
        print(f"Time elapsed: {time.time() - self.start_time:.2f} seconds")
        
        return self.results['neutrino']
    
    def analyze_cosmology_sensitivity(self):
        """Analyze sensitivity of cosmological predictions to parameter variations."""
        print("\n" + "=" * 80)
        print("COSMOLOGICAL SENSITIVITY ANALYSIS")
        print("=" * 80)
        
        # Initialize cosmological model (Part 4)
        cosmo_model = matryoshka_part4.derive_cosmological_model(self.framework)
        
        # Initialize cosmological puzzle resolutions
        puzzle_resolutions = matryoshka_part4.resolve_cosmological_puzzles(
            self.framework, cosmo_model)
        
        # Initialize dark sector model
        dark_sector = matryoshka_part4.model_dark_sector(
            self.framework, cosmo_model)
        
        # Initialize structure formation model
        structure_formation = matryoshka_part4.derive_structure_formation(
            self.framework, cosmo_model)
        
        print("\nAnalyzing sensitivity of cosmological predictions to parameter variations...")
        
        # Store base predictions
        base_predictions = {
            'Omega_k': puzzle_resolutions['flatness_problem']['Omega_k'],
            'Lambda': puzzle_resolutions['cc_problem']['Lambda_val'],
            'w_0': dark_sector['dark_energy']['w0'],
            'w_a': dark_sector['dark_energy']['wa'],
            'n_s': structure_formation['primordial_fluctuations']['n_s'],
            'r': structure_formation['primordial_fluctuations']['r'],
            'alpha_s': structure_formation['primordial_fluctuations']['alpha_s']
        }
        
        print("\nBase predictions:")
        for key, value in base_predictions.items():
            if key == 'Lambda':
                print(f"  {key} = {value:.6e}")
            else:
                print(f"  {key} = {value:.6f}")
        
        # Create storage for sensitivity results
        sensitivity = {
            'omega': {pred: [] for pred in base_predictions},
            'lambda_ord': {pred: [] for pred in base_predictions},
            'alpha_shell': {pred: [] for pred in base_predictions}
        }
        
        # Analyze omega sensitivity
        for var in self.variation_range:
            # Create modified framework with varied omega
            modified_framework = self.framework.copy()
            modified_framework['parameters']['omega'] = self.params.omega * (1 + var/100)
            
            # Recalculate predictions
            cosmo_model_mod = matryoshka_part4.derive_cosmological_model(modified_framework)
            puzzle_resolutions_mod = matryoshka_part4.resolve_cosmological_puzzles(
                modified_framework, cosmo_model_mod)
            dark_sector_mod = matryoshka_part4.model_dark_sector(
                modified_framework, cosmo_model_mod)
            structure_formation_mod = matryoshka_part4.derive_structure_formation(
                modified_framework, cosmo_model_mod)
            
            # Store results
            sensitivity['omega']['Omega_k'].append(puzzle_resolutions_mod['flatness_problem']['Omega_k'])
            sensitivity['omega']['Lambda'].append(puzzle_resolutions_mod['cc_problem']['Lambda_val'])
            sensitivity['omega']['w_0'].append(dark_sector_mod['dark_energy']['w0'])
            sensitivity['omega']['w_a'].append(dark_sector_mod['dark_energy']['wa'])
            sensitivity['omega']['n_s'].append(structure_formation_mod['primordial_fluctuations']['n_s'])
            sensitivity['omega']['r'].append(structure_formation_mod['primordial_fluctuations']['r'])
            sensitivity['omega']['alpha_s'].append(structure_formation_mod['primordial_fluctuations']['alpha_s'])
        
        # Analyze lambda_ord sensitivity
        for var in self.variation_range:
            # Create modified framework with varied lambda_ord
            modified_framework = self.framework.copy()
            modified_framework['parameters']['lambda_ord'] = self.params.lambda_ord * (1 + var/100)
            
            # Recalculate predictions
            cosmo_model_mod = matryoshka_part4.derive_cosmological_model(modified_framework)
            puzzle_resolutions_mod = matryoshka_part4.resolve_cosmological_puzzles(
                modified_framework, cosmo_model_mod)
            dark_sector_mod = matryoshka_part4.model_dark_sector(
                modified_framework, cosmo_model_mod)
            structure_formation_mod = matryoshka_part4.derive_structure_formation(
                modified_framework, cosmo_model_mod)
            
            # Store results
            sensitivity['lambda_ord']['Omega_k'].append(puzzle_resolutions_mod['flatness_problem']['Omega_k'])
            sensitivity['lambda_ord']['Lambda'].append(puzzle_resolutions_mod['cc_problem']['Lambda_val'])
            sensitivity['lambda_ord']['w_0'].append(dark_sector_mod['dark_energy']['w0'])
            sensitivity['lambda_ord']['w_a'].append(dark_sector_mod['dark_energy']['wa'])
            sensitivity['lambda_ord']['n_s'].append(structure_formation_mod['primordial_fluctuations']['n_s'])
            sensitivity['lambda_ord']['r'].append(structure_formation_mod['primordial_fluctuations']['r'])
            sensitivity['lambda_ord']['alpha_s'].append(structure_formation_mod['primordial_fluctuations']['alpha_s'])
        
        # Analyze alpha_shell sensitivity
        for var in self.variation_range:
            # Create modified framework with varied alpha_shell
            modified_framework = self.framework.copy()
            modified_framework['parameters']['alpha_shell'] = self.params.alpha_shell * (1 + var/100)
            
            # Recalculate predictions
            cosmo_model_mod = matryoshka_part4.derive_cosmological_model(modified_framework)
            puzzle_resolutions_mod = matryoshka_part4.resolve_cosmological_puzzles(
                modified_framework, cosmo_model_mod)
            dark_sector_mod = matryoshka_part4.model_dark_sector(
                modified_framework, cosmo_model_mod)
            structure_formation_mod = matryoshka_part4.derive_structure_formation(
                modified_framework, cosmo_model_mod)
            
            # Store results
            sensitivity['alpha_shell']['Omega_k'].append(puzzle_resolutions_mod['flatness_problem']['Omega_k'])
            sensitivity['alpha_shell']['Lambda'].append(puzzle_resolutions_mod['cc_problem']['Lambda_val'])
            sensitivity['alpha_shell']['w_0'].append(dark_sector_mod['dark_energy']['w0'])
            sensitivity['alpha_shell']['w_a'].append(dark_sector_mod['dark_energy']['wa'])
            sensitivity['alpha_shell']['n_s'].append(structure_formation_mod['primordial_fluctuations']['n_s'])
            sensitivity['alpha_shell']['r'].append(structure_formation_mod['primordial_fluctuations']['r'])
            sensitivity['alpha_shell']['alpha_s'].append(structure_formation_mod['primordial_fluctuations']['alpha_s'])
        
        # Calculate sensitivities (percentage change)
        relative_sensitivity = {}
        for param in sensitivity:
            relative_sensitivity[param] = {}
            for pred in base_predictions:
                # Special handling for w_0 since it's close to -1
                if pred == 'w_0':
                    absolute_change = np.array(sensitivity[param][pred]) - base_predictions[pred]
                    relative_sensitivity[param][pred] = absolute_change
                else:
                    relative_values = np.array(sensitivity[param][pred]) / base_predictions[pred]
                    relative_sensitivity[param][pred] = relative_values
        
        # Store results
        self.results['cosmology'] = {
            'base_predictions': base_predictions,
            'sensitivity': sensitivity,
            'relative_sensitivity': relative_sensitivity
        }
        
        print("\nCosmology sensitivity analysis complete.")
        print(f"Time elapsed: {time.time() - self.start_time:.2f} seconds")
        
        return self.results['cosmology']
    
    def analyze_particle_mass_sensitivity(self):
        """Analyze sensitivity of particle mass predictions to parameter variations."""
        print("\n" + "=" * 80)
        print("PARTICLE MASS SENSITIVITY ANALYSIS")
        print("=" * 80)
        
        # Initialize excitation patterns from Part 3
        excitation_dict = matryoshka_part3.define_excitation_patterns(self.framework)
        
        # Initialize particle families
        family_dict = matryoshka_part3.define_particle_families(
            self.framework, excitation_dict)
        
        # Initialize generational structure
        generation_dict = matryoshka_part3.define_generational_structure(
            self.framework, family_dict)
        
        # Derive mass formula
        mass_dict = matryoshka_part3.derive_mass_formula(
            self.framework, generation_dict)
        
        # Calculate all particle masses
        mass_hierarchy_data = matryoshka_part3.calculate_all_particle_masses(
            self.framework, mass_dict, neutrino_mass_dict = {})
        
        print("\nAnalyzing sensitivity of particle mass predictions to parameter variations...")
        
        # Store base predictions (focus on key particles)
        base_predictions = {
            'e_mass': mass_hierarchy_data['leptons']['e']['mass_physical'],
            'mu_mass': mass_hierarchy_data['leptons']['mu']['mass_physical'],
            'tau_mass': mass_hierarchy_data['leptons']['tau']['mass_physical'],
            'u_mass': mass_hierarchy_data['quarks']['u']['mass_physical'],
            'd_mass': mass_hierarchy_data['quarks']['d']['mass_physical'],
            't_mass': mass_hierarchy_data['quarks']['t']['mass_physical'],
            'W_mass': mass_hierarchy_data['bosons']['W']['mass_physical'],
            'Z_mass': mass_hierarchy_data['bosons']['Z']['mass_physical'],
            'H_mass': mass_hierarchy_data['bosons']['H']['mass_physical']
        }
        
        print("\nBase predictions:")
        for key, value in base_predictions.items():
            print(f"  {key} = {value:.6f} MeV")
        
        # Create storage for sensitivity results
        sensitivity = {
            'omega': {pred: [] for pred in base_predictions},
            'lambda_m': {pred: [] for pred in base_predictions},
            'alpha_cal': {pred: [] for pred in base_predictions}
        }
        
        # Analyze omega sensitivity
        for var in self.variation_range:
            # Create modified framework with varied omega
            modified_framework = self.framework.copy()
            modified_framework['parameters']['omega'] = self.params.omega * (1 + var/100)
            
            # Recalculate predictions
            excitation_dict_mod = matryoshka_part3.define_excitation_patterns(modified_framework)
            family_dict_mod = matryoshka_part3.define_particle_families(
                modified_framework, excitation_dict_mod)
            generation_dict_mod = matryoshka_part3.define_generational_structure(
                modified_framework, family_dict_mod)
            mass_dict_mod = matryoshka_part3.derive_mass_formula(
                modified_framework, generation_dict_mod)
            mass_hierarchy_data_mod = matryoshka_part3.calculate_all_particle_masses(
                modified_framework, mass_dict_mod, neutrino_mass_dict = {})
            
            # Store results
            sensitivity['omega']['e_mass'].append(mass_hierarchy_data_mod['leptons']['e']['mass_physical'])
            sensitivity['omega']['mu_mass'].append(mass_hierarchy_data_mod['leptons']['mu']['mass_physical'])
            sensitivity['omega']['tau_mass'].append(mass_hierarchy_data_mod['leptons']['tau']['mass_physical'])
            sensitivity['omega']['u_mass'].append(mass_hierarchy_data_mod['quarks']['u']['mass_physical'])
            sensitivity['omega']['d_mass'].append(mass_hierarchy_data_mod['quarks']['d']['mass_physical'])
            sensitivity['omega']['t_mass'].append(mass_hierarchy_data_mod['quarks']['t']['mass_physical'])
            sensitivity['omega']['W_mass'].append(mass_hierarchy_data_mod['bosons']['W']['mass_physical'])
            sensitivity['omega']['Z_mass'].append(mass_hierarchy_data_mod['bosons']['Z']['mass_physical'])
            sensitivity['omega']['H_mass'].append(mass_hierarchy_data_mod['bosons']['H']['mass_physical'])
        
        # Analyze lambda_m sensitivity
        for var in self.variation_range:
            # Create modified framework with varied lambda_m
            modified_framework = self.framework.copy()
            modified_framework['parameters']['lambda_m'] = self.params.lambda_m * (1 + var/100)
            
            # Recalculate predictions
            excitation_dict_mod = matryoshka_part3.define_excitation_patterns(modified_framework)
            family_dict_mod = matryoshka_part3.define_particle_families(
                modified_framework, excitation_dict_mod)
            generation_dict_mod = matryoshka_part3.define_generational_structure(
                modified_framework, family_dict_mod)
            mass_dict_mod = matryoshka_part3.derive_mass_formula(
                modified_framework, generation_dict_mod)
            mass_hierarchy_data_mod = matryoshka_part3.calculate_all_particle_masses(
                modified_framework, mass_dict_mod, neutrino_mass_dict = {})
            
            # Store results
            sensitivity['lambda_m']['e_mass'].append(mass_hierarchy_data_mod['leptons']['e']['mass_physical'])
            sensitivity['lambda_m']['mu_mass'].append(mass_hierarchy_data_mod['leptons']['mu']['mass_physical'])
            sensitivity['lambda_m']['tau_mass'].append(mass_hierarchy_data_mod['leptons']['tau']['mass_physical'])
            sensitivity['lambda_m']['u_mass'].append(mass_hierarchy_data_mod['quarks']['u']['mass_physical'])
            sensitivity['lambda_m']['d_mass'].append(mass_hierarchy_data_mod['quarks']['d']['mass_physical'])
            sensitivity['lambda_m']['t_mass'].append(mass_hierarchy_data_mod['quarks']['t']['mass_physical'])
            sensitivity['lambda_m']['W_mass'].append(mass_hierarchy_data_mod['bosons']['W']['mass_physical'])
            sensitivity['lambda_m']['Z_mass'].append(mass_hierarchy_data_mod['bosons']['Z']['mass_physical'])
            sensitivity['lambda_m']['H_mass'].append(mass_hierarchy_data_mod['bosons']['H']['mass_physical'])
        
        # Analyze alpha_cal sensitivity
        for var in self.variation_range:
            # Create modified framework with varied alpha_cal
            modified_framework = self.framework.copy()
            modified_framework['parameters']['alpha_cal'] = self.params.alpha_cal * (1 + var/100)
            
            # Recalculate predictions
            excitation_dict_mod = matryoshka_part3.define_excitation_patterns(modified_framework)
            family_dict_mod = matryoshka_part3.define_particle_families(
                modified_framework, excitation_dict_mod)
            generation_dict_mod = matryoshka_part3.define_generational_structure(
                modified_framework, family_dict_mod)
            mass_dict_mod = matryoshka_part3.derive_mass_formula(
                modified_framework, generation_dict_mod)
            mass_hierarchy_data_mod = matryoshka_part3.calculate_all_particle_masses(
                modified_framework, mass_dict_mod, neutrino_mass_dict = {})
            
            # Store results
            sensitivity['alpha_cal']['e_mass'].append(mass_hierarchy_data_mod['leptons']['e']['mass_physical'])
            sensitivity['alpha_cal']['mu_mass'].append(mass_hierarchy_data_mod['leptons']['mu']['mass_physical'])
            sensitivity['alpha_cal']['tau_mass'].append(mass_hierarchy_data_mod['leptons']['tau']['mass_physical'])
            sensitivity['alpha_cal']['u_mass'].append(mass_hierarchy_data_mod['quarks']['u']['mass_physical'])
            sensitivity['alpha_cal']['d_mass'].append(mass_hierarchy_data_mod['quarks']['d']['mass_physical'])
            sensitivity['alpha_cal']['t_mass'].append(mass_hierarchy_data_mod['quarks']['t']['mass_physical'])
            sensitivity['alpha_cal']['W_mass'].append(mass_hierarchy_data_mod['bosons']['W']['mass_physical'])
            sensitivity['alpha_cal']['Z_mass'].append(mass_hierarchy_data_mod['bosons']['Z']['mass_physical'])
            sensitivity['alpha_cal']['H_mass'].append(mass_hierarchy_data_mod['bosons']['H']['mass_physical'])
        
        # Calculate sensitivities (percentage change)
        relative_sensitivity = {}
        for param in sensitivity:
            relative_sensitivity[param] = {}
            for pred in base_predictions:
                relative_values = np.array(sensitivity[param][pred]) / base_predictions[pred]
                relative_sensitivity[param][pred] = relative_values
        
        # Store results
        self.results['particle_masses'] = {
            'base_predictions': base_predictions,
            'sensitivity': sensitivity,
            'relative_sensitivity': relative_sensitivity
        }
        
        print("\nParticle mass sensitivity analysis complete.")
        print(f"Time elapsed: {time.time() - self.start_time:.2f} seconds")
        
        return self.results['particle_masses']
    
    def analyze_oscillation_sensitivity(self):
        """Analyze sensitivity of neutrino oscillation predictions to parameter variations."""
        print("\n" + "=" * 80)
        print("NEUTRINO OSCILLATION SENSITIVITY ANALYSIS")
        print("=" * 80)
        
        # Initialize golden ratio structure (Part 5)
        golden_dict = matryoshka_part5.define_golden_ratio_structure(self.framework)
        
        # Initialize neutrino mass hierarchy
        neutrino_mass_dict = matryoshka_part5.derive_neutrino_mass_hierarchy(
            self.framework, golden_dict)
        
        # Initialize mixing angles
        mixing_dict = matryoshka_part5.derive_mixing_angles(
            self.framework, golden_dict)
        
        # Initialize PMNS matrix
        pmns_dict = matryoshka_part5.derive_pmns_matrix(
            self.framework, golden_dict, mixing_dict)
        
        # Calculate oscillation probabilities (standard parameters)
        L = 1000  # km (representative baseline)
        E_values = np.linspace(0.1, 10, 100)  # GeV
        
        # Calculate standard oscillation probabilities
        base_probabilities = {
            'P_e_mu': [],
            'P_e_tau': [],
            'P_mu_e': [],
            'P_mu_mu': [],
            'P_mu_tau': []
        }
        
        for E in E_values:
            # Convert units for calculation
            L_m = L * 1000  # km to m
            E_eV = E * 1e9  # GeV to eV
            
            # Calculate probabilities
            prob_e_mu = matryoshka_part5.calculate_oscillation_probability_shell(
                1, 2, L_m, E_eV, pmns_dict['U_PMNS'], neutrino_mass_dict['m_sq'],
                self.params.lambda_nu, self.params.omega)
            
            prob_e_tau = matryoshka_part5.calculate_oscillation_probability_shell(
                1, 3, L_m, E_eV, pmns_dict['U_PMNS'], neutrino_mass_dict['m_sq'],
                self.params.lambda_nu, self.params.omega)
            
            prob_mu_e = matryoshka_part5.calculate_oscillation_probability_shell(
                2, 1, L_m, E_eV, pmns_dict['U_PMNS'], neutrino_mass_dict['m_sq'],
                self.params.lambda_nu, self.params.omega)
            
            prob_mu_mu = matryoshka_part5.calculate_oscillation_probability_shell(
                2, 2, L_m, E_eV, pmns_dict['U_PMNS'], neutrino_mass_dict['m_sq'],
                self.params.lambda_nu, self.params.omega)
            
            prob_mu_tau = matryoshka_part5.calculate_oscillation_probability_shell(
                2, 3, L_m, E_eV, pmns_dict['U_PMNS'], neutrino_mass_dict['m_sq'],
                self.params.lambda_nu, self.params.omega)
            
            base_probabilities['P_e_mu'].append(prob_e_mu)
            base_probabilities['P_e_tau'].append(prob_e_tau)
            base_probabilities['P_mu_e'].append(prob_mu_e)
            base_probabilities['P_mu_mu'].append(prob_mu_mu)
            base_probabilities['P_mu_tau'].append(prob_mu_tau)
        
        print("\nAnalyzing sensitivity of neutrino oscillation predictions to parameter variations...")
        
        # Create storage for sensitivity results
        sensitivity = {
            'lambda_nu': {
                'variation': self.variation_range,
                'P_e_mu': [],
                'P_e_tau': [],
                'P_mu_e': [],
                'P_mu_mu': [],
                'P_mu_tau': []
            },
            'omega': {
                'variation': self.variation_range,
                'P_e_mu': [],
                'P_e_tau': [],
                'P_mu_e': [],
                'P_mu_mu': [],
                'P_mu_tau': []
            }
        }
        
        # Analyze lambda_nu sensitivity (at representative energy)
        representative_E = 1.0  # GeV
        representative_E_eV = representative_E * 1e9  # GeV to eV
        
        for var in self.variation_range:
            lambda_nu_mod = self.params.lambda_nu * (1 + var/100)
            
            # Calculate modified probabilities
            prob_e_mu = matryoshka_part5.calculate_oscillation_probability_shell(
                1, 2, L_m, representative_E_eV, pmns_dict['U_PMNS'], neutrino_mass_dict['m_sq'],
                lambda_nu_mod, self.params.omega)
            
            prob_e_tau = matryoshka_part5.calculate_oscillation_probability_shell(
                1, 3, L_m, representative_E_eV, pmns_dict['U_PMNS'], neutrino_mass_dict['m_sq'],
                lambda_nu_mod, self.params.omega)
            
            prob_mu_e = matryoshka_part5.calculate_oscillation_probability_shell(
                2, 1, L_m, representative_E_eV, pmns_dict['U_PMNS'], neutrino_mass_dict['m_sq'],
                lambda_nu_mod, self.params.omega)
            
            prob_mu_mu = matryoshka_part5.calculate_oscillation_probability_shell(
                2, 2, L_m, representative_E_eV, pmns_dict['U_PMNS'], neutrino_mass_dict['m_sq'],
                lambda_nu_mod, self.params.omega)
            
            prob_mu_tau = matryoshka_part5.calculate_oscillation_probability_shell(
                2, 3, L_m, representative_E_eV, pmns_dict['U_PMNS'], neutrino_mass_dict['m_sq'],
                lambda_nu_mod, self.params.omega)
            
            sensitivity['lambda_nu']['P_e_mu'].append(prob_e_mu)
            sensitivity['lambda_nu']['P_e_tau'].append(prob_e_tau)
            sensitivity['lambda_nu']['P_mu_e'].append(prob_mu_e)
            sensitivity['lambda_nu']['P_mu_mu'].append(prob_mu_mu)
            sensitivity['lambda_nu']['P_mu_tau'].append(prob_mu_tau)
        
        # Analyze omega sensitivity (at representative energy)
        for var in self.variation_range:
            omega_mod = self.params.omega * (1 + var/100)
            
            # Calculate modified probabilities
            prob_e_mu = matryoshka_part5.calculate_oscillation_probability_shell(
                1, 2, L_m, representative_E_eV, pmns_dict['U_PMNS'], neutrino_mass_dict['m_sq'],
                self.params.lambda_nu, omega_mod)
            
            prob_e_tau = matryoshka_part5.calculate_oscillation_probability_shell(
                1, 3, L_m, representative_E_eV, pmns_dict['U_PMNS'], neutrino_mass_dict['m_sq'],
                self.params.lambda_nu, omega_mod)
            
            prob_mu_e = matryoshka_part5.calculate_oscillation_probability_shell(
                2, 1, L_m, representative_E_eV, pmns_dict['U_PMNS'], neutrino_mass_dict['m_sq'],
                self.params.lambda_nu, omega_mod)
            
            prob_mu_mu = matryoshka_part5.calculate_oscillation_probability_shell(
                2, 2, L_m, representative_E_eV, pmns_dict['U_PMNS'], neutrino_mass_dict['m_sq'],
                self.params.lambda_nu, omega_mod)
            
            prob_mu_tau = matryoshka_part5.calculate_oscillation_probability_shell(
                2, 3, L_m, representative_E_eV, pmns_dict['U_PMNS'], neutrino_mass_dict['m_sq'],
                self.params.lambda_nu, omega_mod)
            
            sensitivity['omega']['P_e_mu'].append(prob_e_mu)
            sensitivity['omega']['P_e_tau'].append(prob_e_tau)
            sensitivity['omega']['P_mu_e'].append(prob_mu_e)
            sensitivity['omega']['P_mu_mu'].append(prob_mu_mu)
            sensitivity['omega']['P_mu_tau'].append(prob_mu_tau)
        
        # Store results
        self.results['oscillations'] = {
            'E_values': E_values,
            'L': L,
            'base_probabilities': base_probabilities,
            'sensitivity': sensitivity
        }
        
        print("\nNeutrino oscillation sensitivity analysis complete.")
        print(f"Time elapsed: {time.time() - self.start_time:.2f} seconds")
        
        return self.results['oscillations']
    
    def visualize_results(self):
        """Visualize the sensitivity analysis results."""
        print("\n" + "=" * 80)
        print("VISUALIZING SENSITIVITY ANALYSIS RESULTS")
        print("=" * 80)
        
        # Check which analyses have been run
        analyses_run = list(self.results.keys())
        
        if not analyses_run:
            print("\nNo sensitivity analyses have been run yet.")
            return
        
        print(f"\nCreating visualizations for: {', '.join(analyses_run)}")
        
        # Create directory for visualizations
        import os
        if not os.path.exists('sensitivity_plots'):
            os.makedirs('sensitivity_plots')
        
        # Visualize neutrino sensitivity if available
        if 'neutrino' in analyses_run:
            self.visualize_neutrino_sensitivity()
        
        # Visualize cosmology sensitivity if available
        if 'cosmology' in analyses_run:
            self.visualize_cosmology_sensitivity()
        
        # Visualize particle mass sensitivity if available
        if 'particle_masses' in analyses_run:
            self.visualize_particle_mass_sensitivity()
        
        # Visualize oscillation sensitivity if available
        if 'oscillations' in analyses_run:
            self.visualize_oscillation_sensitivity()
        
        print("\nAll visualization complete.")
        print(f"Time elapsed: {time.time() - self.start_time:.2f} seconds")
    
    def visualize_neutrino_sensitivity(self):
        """Visualize neutrino parameter sensitivity results."""
        results = self.results['neutrino']
        
        # Create heatmap of sensitivities
        parameters = ['omega', 'lambda_nu', 'phi']
        predictions = ['m1', 'm2', 'm3', 'sum_m', 'm_bb', 'sin2_theta12', 'sin2_theta23', 'sin2_theta13']
        
        # Convert to heatmap data
        # Use slope of sensitivity curve at 0 as sensitivity metric
        sensitivity_matrix = np.zeros((len(parameters), len(predictions)))
        
        for i, param in enumerate(parameters):
            for j, pred in enumerate(predictions):
                rel_sens = results['relative_sensitivity'][param][pred]
                # Calculate slope near central value (ignoring endpoints)
                mid_idx = len(self.variation_range) // 2
                x_vals = self.variation_range[mid_idx-2:mid_idx+3]
                y_vals = rel_sens[mid_idx-2:mid_idx+3]
                slope, _, _, _, _ = stats.linregress(x_vals, y_vals)
                sensitivity_matrix[i, j] = slope
        
        # Plot heatmap
        plt.figure(figsize=(12, 8))
        plt.imshow(sensitivity_matrix, cmap='RdBu_r', aspect='auto', vmin=-2, vmax=2)
        plt.colorbar(label='Sensitivity (rel. change / % param change)')
        plt.xticks(np.arange(len(predictions)), predictions, rotation=45)
        plt.yticks(np.arange(len(parameters)), parameters)
        plt.title('Neutrino Prediction Sensitivity to Parameter Variations')
        plt.tight_layout()
        plt.savefig('sensitivity_plots/neutrino_sensitivity_heatmap.png')
        
        # Plot individual sensitivity curves for key predictions
        key_predictions = ['m_bb', 'sum_m']
        
        for pred in key_predictions:
            plt.figure(figsize=(10, 6))
            
            for param in parameters:
                rel_sens = results['relative_sensitivity'][param][pred]
                plt.plot(self.variation_range, rel_sens, '.-', linewidth=2, label=f'{param}')
            
            plt.axhline(y=1.0, color='k', linestyle='--', alpha=0.3)
            plt.xlabel('Parameter Variation (%)')
            plt.ylabel(f'Relative {pred} Value')
            plt.title(f'Sensitivity of {pred} to Parameter Variations')
            plt.grid(alpha=0.3)
            plt.legend()
            plt.tight_layout()
            plt.savefig(f'sensitivity_plots/neutrino_{pred}_sensitivity.png')
        
        print("\nNeutrino sensitivity visualizations saved to sensitivity_plots/ directory.")
    
    def visualize_cosmology_sensitivity(self):
        """Visualize cosmology parameter sensitivity results."""
        results = self.results['cosmology']
        
        # Create heatmap of sensitivities
        parameters = ['omega', 'lambda_ord', 'alpha_shell']
        predictions = ['Omega_k', 'Lambda', 'w_0', 'w_a', 'n_s', 'r', 'alpha_s']
        
        # Convert to heatmap data
        # Use slope of sensitivity curve at 0 as sensitivity metric
        sensitivity_matrix = np.zeros((len(parameters), len(predictions)))
        
        for i, param in enumerate(parameters):
            for j, pred in enumerate(predictions):
                # Special handling for w_0 (absolute change)
                if pred == 'w_0':
                    rel_sens = np.array(results['sensitivity'][param][pred]) / results['base_predictions'][pred]
                else:
                    rel_sens = results['relative_sensitivity'][param][pred]
                
                # Calculate slope near central value (ignoring endpoints)
                mid_idx = len(self.variation_range) // 2
                x_vals = self.variation_range[mid_idx-2:mid_idx+3]
                y_vals = rel_sens[mid_idx-2:mid_idx+3]
                slope, _, _, _, _ = stats.linregress(x_vals, y_vals)
                sensitivity_matrix[i, j] = slope
        
        # Plot heatmap
        plt.figure(figsize=(12, 8))
        plt.imshow(sensitivity_matrix, cmap='RdBu_r', aspect='auto', vmin=-5, vmax=5)
        plt.colorbar(label='Sensitivity (rel. change / % param change)')
        plt.xticks(np.arange(len(predictions)), predictions, rotation=45)
        plt.yticks(np.arange(len(parameters)), parameters)
        plt.title('Cosmological Prediction Sensitivity to Parameter Variations')
        plt.tight_layout()
        plt.savefig('sensitivity_plots/cosmology_sensitivity_heatmap.png')
        
        # Plot individual sensitivity curves for key predictions
        key_predictions = ['Lambda', 'n_s', 'r']
        
        for pred in key_predictions:
            plt.figure(figsize=(10, 6))
            
            for param in parameters:
                rel_sens = results['relative_sensitivity'][param][pred]
                plt.plot(self.variation_range, rel_sens, '.-', linewidth=2, label=f'{param}')
            
            plt.axhline(y=1.0, color='k', linestyle='--', alpha=0.3)
            plt.xlabel('Parameter Variation (%)')
            plt.ylabel(f'Relative {pred} Value')
            plt.title(f'Sensitivity of {pred} to Parameter Variations')
            plt.grid(alpha=0.3)
            plt.legend()
            plt.tight_layout()
            plt.savefig(f'sensitivity_plots/cosmology_{pred}_sensitivity.png')
        
        print("\nCosmology sensitivity visualizations saved to sensitivity_plots/ directory.")
    
    def visualize_particle_mass_sensitivity(self):
        """Visualize particle mass sensitivity results."""
        results = self.results['particle_masses']
        
        # Create heatmap of sensitivities
        parameters = ['omega', 'lambda_m', 'alpha_cal']
        predictions = ['mu_mass', 'tau_mass', 't_mass', 'W_mass', 'H_mass']
        
        # Convert to heatmap data
        # Use slope of sensitivity curve at 0 as sensitivity metric
        sensitivity_matrix = np.zeros((len(parameters), len(predictions)))
        
        for i, param in enumerate(parameters):
            for j, pred in enumerate(predictions):
                rel_sens = results['relative_sensitivity'][param][pred]
                # Calculate slope near central value (ignoring endpoints)
                mid_idx = len(self.variation_range) // 2
                x_vals = self.variation_range[mid_idx-2:mid_idx+3]
                y_vals = rel_sens[mid_idx-2:mid_idx+3]
                slope, _, _, _, _ = stats.linregress(x_vals, y_vals)
                sensitivity_matrix[i, j] = slope
        
        # Plot heatmap
        plt.figure(figsize=(12, 8))
        plt.imshow(sensitivity_matrix, cmap='RdBu_r', aspect='auto', vmin=-10, vmax=10)
        plt.colorbar(label='Sensitivity (rel. change / % param change)')
        plt.xticks(np.arange(len(predictions)), predictions, rotation=45)
        plt.yticks(np.arange(len(parameters)), parameters)
        plt.title('Particle Mass Sensitivity to Parameter Variations')
        plt.tight_layout()
        plt.savefig('sensitivity_plots/particle_mass_sensitivity_heatmap.png')
        
        # Plot individual sensitivity curves for key particles
        key_particles = ['mu_mass', 'tau_mass', 'H_mass']
        
        for pred in key_particles:
            plt.figure(figsize=(10, 6))
            
            for param in parameters:
                rel_sens = results['relative_sensitivity'][param][pred]
                plt.plot(self.variation_range, rel_sens, '.-', linewidth=2, label=f'{param}')
            
            plt.axhline(y=1.0, color='k', linestyle='--', alpha=0.3)
            plt.xlabel('Parameter Variation (%)')
            plt.ylabel(f'Relative {pred}')
            plt.title(f'Sensitivity of {pred} to Parameter Variations')
            plt.grid(alpha=0.3)
            plt.legend()
            plt.tight_layout()
            plt.savefig(f'sensitivity_plots/particle_{pred}_sensitivity.png')
        
        print("\nParticle mass sensitivity visualizations saved to sensitivity_plots/ directory.")
    
    def visualize_oscillation_sensitivity(self):
        """Visualize oscillation sensitivity results."""
        results = self.results['oscillations']
        
        # Plot base oscillation probabilities as a function of energy
        plt.figure(figsize=(12, 8))
        
        plt.plot(results['E_values'], results['base_probabilities']['P_e_mu'], '.-', label='P(νₑ → νᵤ)')
        plt.plot(results['E_values'], results['base_probabilities']['P_mu_e'], '.-', label='P(νᵤ → νₑ)')
        plt.plot(results['E_values'], results['base_probabilities']['P_mu_mu'], '.-', label='P(νᵤ → νᵤ)')
        plt.plot(results['E_values'], results['base_probabilities']['P_mu_tau'], '.-', label='P(νᵤ → νᵧ)')
        
        plt.xlabel('Neutrino Energy (GeV)')
        plt.ylabel('Oscillation Probability')
        plt.title(f'Shell-Modified Neutrino Oscillation Probabilities (L = {results["L"]} km)')
        plt.grid(alpha=0.3)
        plt.legend()
        plt.tight_layout()
        plt.savefig('sensitivity_plots/oscillation_probabilities.png')
        
        # Plot sensitivity of oscillation probabilities to lambda_nu and omega
        for param in ['lambda_nu', 'omega']:
            plt.figure(figsize=(12, 8))
            
            plt.plot(results['sensitivity'][param]['variation'], 
                     results['sensitivity'][param]['P_e_mu'], '.-', label='P(νₑ → νᵤ)')
            plt.plot(results['sensitivity'][param]['variation'], 
                     results['sensitivity'][param]['P_mu_e'], '.-', label='P(νᵤ → νₑ)')
            plt.plot(results['sensitivity'][param]['variation'], 
                     results['sensitivity'][param]['P_mu_mu'], '.-', label='P(νᵤ → νᵤ)')
            plt.plot(results['sensitivity'][param]['variation'], 
                     results['sensitivity'][param]['P_mu_tau'], '.-', label='P(νᵤ → νᵧ)')
            
            plt.axvline(x=0, color='k', linestyle='--', alpha=0.3)
            plt.xlabel(f'{param} Variation (%)')
            plt.ylabel('Oscillation Probability')
            plt.title(f'Sensitivity of Oscillation Probabilities to {param}\n(E = 1 GeV, L = {results["L"]} km)')
            plt.grid(alpha=0.3)
            plt.legend()
            plt.tight_layout()
            plt.savefig(f'sensitivity_plots/oscillation_{param}_sensitivity.png')
        
        print("\nOscillation sensitivity visualizations saved to sensitivity_plots/ directory.")
    
    def run_all_analyses(self):
        """Run all sensitivity analyses."""
        # Run neutrino sensitivity analysis
        self.analyze_neutrino_sensitivity()
        
        # Run cosmology sensitivity analysis
        self.analyze_cosmology_sensitivity()
        
        # Run particle mass sensitivity analysis
        self.analyze_particle_mass_sensitivity()
        
        # Run oscillation sensitivity analysis
        self.analyze_oscillation_sensitivity()
        
        # Visualize all results
        self.visualize_results()
        
        print("\n" + "=" * 80)
        print("ALL SENSITIVITY ANALYSES COMPLETE")
        print("=" * 80)
        print(f"\nTotal time elapsed: {time.time() - self.start_time:.2f} seconds")
        print("\nResults and visualizations are available in the sensitivity_plots/ directory.")
        
        return self.results

# If run directly, perform all analyses
if __name__ == "__main__":
    analyzer = MatryoshkaSensitivityAnalysis()
    results = analyzer.run_all_analyses()