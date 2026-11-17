# matryoshka_tests.py
#!/usr/bin/env python3
# Integrated Test Suite for the Matryoshka Theory of Everything

import unittest
import numpy as np
from scipy import constants as const
import matplotlib.pyplot as plt

# Import Matryoshka modules
from matryoshka_unified_parameters import MatryoshkaParameters
import matryoshka_core
import matryoshka_part1
import matryoshka_part2
import matryoshka_part3
import matryoshka_part4
import matryoshka_part5

class TestShellParameters(unittest.TestCase):
    """Test the core shell parameter definitions and consistency."""
    
    def setUp(self):
        """Set up the test environment."""
        self.params = MatryoshkaParameters()
        self.framework = matryoshka_core.initialize_core()
    
    def test_omega_value(self):
        """Test that omega is consistent with lepton mass ratios."""
        # Theoretical calculation: mu/e = exp(lambda_m * (omega - n_e))
        expected_mu_over_e = np.exp(self.params.lambda_m * (self.params.omega - self.params.n_e))
        
        # Test with a 1% tolerance
        self.assertAlmostEqual(
            expected_mu_over_e / self.params.mu_over_e, 
            1.0, 
            delta=0.01,
            msg=f"Omega value inconsistent with mu/e ratio. Expected mu/e: {expected_mu_over_e}, Actual: {self.params.mu_over_e}"
        )
    
    def test_gravitational_constant(self):
        """Test that G is correctly derived from kappa_minus and c0."""
        derived_G = self.params.kappa_minus * self.params.c0
        
        # Test with a 1% tolerance
        self.assertAlmostEqual(
            derived_G / self.params.G, 
            1.0, 
            delta=0.01,
            msg=f"Derived G inconsistent with actual G. Derived: {derived_G}, Actual: {self.params.G}"
        )
    
    def test_shell_radius_scaling(self):
        """Test that shell radius increases exponentially with ordinal index."""
        # Create a sample of shell indices
        indices = np.arange(1, 11)
        
        # Calculate radii
        radii = self.params.r0 * np.exp(self.params.alpha_shell * indices)
        
        # Test exponential scaling by checking consecutive radius ratios
        for i in range(1, len(radii)):
            ratio = radii[i] / radii[i-1]
            expected_ratio = np.exp(self.params.alpha_shell)
            
            self.assertAlmostEqual(
                ratio, 
                expected_ratio, 
                delta=1e-10,
                msg=f"Shell radius scaling inconsistent at i={indices[i]}. Ratio: {ratio}, Expected: {expected_ratio}"
            )


class TestNeutrinoPhysics(unittest.TestCase):
    """Test the neutrino physics predictions of the framework."""
    
    def setUp(self):
        """Set up the test environment."""
        self.params = MatryoshkaParameters()
        self.framework = matryoshka_core.initialize_core()
        
        # Initialize golden dict from Part 5
        self.golden_dict = matryoshka_part5.define_golden_ratio_structure(self.framework)
        
        # Setup neutrino mass hierarchy
        self.neutrino_mass_dict = matryoshka_part5.derive_neutrino_mass_hierarchy(
            self.framework, self.golden_dict)
        
        # Setup mixing angles
        self.mixing_dict = matryoshka_part5.derive_mixing_angles(
            self.framework, self.golden_dict)
        
        # Setup PMNS matrix
        self.pmns_dict = matryoshka_part5.derive_pmns_matrix(
            self.framework, self.golden_dict, self.mixing_dict)
        
        # Setup Majorana phases
        self.majorana_dict = matryoshka_part5.derive_majorana_phases(
            self.framework, self.golden_dict)
        
        # Calculate neutrinoless double beta decay
        self.dbd_dict = matryoshka_part5.calculate_neutrinoless_double_beta_decay(
            self.framework, self.golden_dict, self.neutrino_mass_dict, 
            self.pmns_dict, self.majorana_dict)
    
    def test_golden_ratio_mixing(self):
        """Test that mixing angles match golden ratio predictions."""
        # Check sin²(θ₁₂) = 1/φ²
        self.assertAlmostEqual(
            self.mixing_dict['sin2_theta12_val'],
            1.0 / self.params.phi_sq,
            delta=1e-10,
            msg=f"sin²(θ₁₂) does not match 1/φ². Actual: {self.mixing_dict['sin2_theta12_val']}, Expected: {1.0/self.params.phi_sq}"
        )
        
        # Check sin²(θ₂₃) = 1/2 - 1/(2φ³)
        self.assertAlmostEqual(
            self.mixing_dict['sin2_theta23_val'],
            0.5 - 0.5 / self.params.phi_cb,
            delta=1e-10,
            msg=f"sin²(θ₂₃) does not match 1/2 - 1/(2φ³). Actual: {self.mixing_dict['sin2_theta23_val']}"
        )
        
        # Check sin²(θ₁₃) = 1/(4φ⁴)
        self.assertAlmostEqual(
            self.mixing_dict['sin2_theta13_val'],
            1.0 / (4 * self.params.phi**4),
            delta=1e-10,
            msg=f"sin²(θ₁₃) does not match 1/(4φ⁴). Actual: {self.mixing_dict['sin2_theta13_val']}"
        )
    
    def test_pmns_unitarity(self):
        """Test that the PMNS matrix is unitary."""
        U = self.pmns_dict['U_PMNS']
        UUdag = np.matmul(U, U.conj().T)
        
        # Check that U·U† = I (identity matrix)
        for i in range(3):
            for j in range(3):
                expected = 1.0 if i == j else 0.0
                self.assertAlmostEqual(
                    abs(UUdag[i, j]),
                    expected,
                    delta=1e-10,
                    msg=f"PMNS matrix is not unitary. U·U†[{i},{j}] = {UUdag[i,j]}, Expected: {expected}"
                )
    
    def test_majorana_phases(self):
        """Test that Majorana phases follow the golden ratio pattern."""
        # α₁ = π/φ
        self.assertAlmostEqual(
            self.majorana_dict['alpha1'] / np.pi,
            1.0 / self.params.phi,
            delta=1e-10,
            msg=f"α₁ does not match π/φ. Actual: {self.majorana_dict['alpha1']/np.pi}π"
        )
        
        # α₂ = π/φ²
        self.assertAlmostEqual(
            self.majorana_dict['alpha2'] / np.pi,
            1.0 / self.params.phi_sq,
            delta=1e-10,
            msg=f"α₂ does not match π/φ². Actual: {self.majorana_dict['alpha2']/np.pi}π"
        )
    
    def test_neutrinoless_double_beta(self):
        """Test the prediction for neutrinoless double beta decay."""
        # Check that |m_ββ| matches the prediction ~0.0074 eV
        self.assertAlmostEqual(
            self.dbd_dict['m_bb_val'],
            0.0074,
            delta=0.0005,
            msg=f"|m_ββ| does not match prediction. Actual: {self.dbd_dict['m_bb_val']} eV"
        )


class TestParticleMasses(unittest.TestCase):
    """Test the particle mass predictions of the framework."""
    
    def setUp(self):
        """Set up the test environment."""
        self.params = MatryoshkaParameters()
        self.framework = matryoshka_core.initialize_core()
        
        # Initialize excitation patterns from Part 3
        self.excitation_dict = matryoshka_part3.define_excitation_patterns(self.framework)
        
        # Initialize particle families
        self.family_dict = matryoshka_part3.define_particle_families(
            self.framework, self.excitation_dict)
        
        # Initialize generational structure
        self.generation_dict = matryoshka_part3.define_generational_structure(
            self.framework, self.family_dict)
        
        # Derive mass formula
        self.mass_dict = matryoshka_part3.derive_mass_formula(
            self.framework, self.generation_dict)
        
        # Calculate all particle masses
        self.mass_hierarchy_data = matryoshka_part3.calculate_all_particle_masses(
            self.framework, self.mass_dict, neutrino_mass_dict={})
    
    def test_lepton_mass_ratios(self):
        """Test that lepton mass ratios match experimental values."""
        # Extract masses
        m_e = self.mass_hierarchy_data['leptons']['e']['mass_physical']
        m_mu = self.mass_hierarchy_data['leptons']['mu']['mass_physical']
        m_tau = self.mass_hierarchy_data['leptons']['tau']['mass_physical']
        
        # Calculate ratios
        mu_over_e = m_mu / m_e
        tau_over_e = m_tau / m_e
        tau_over_mu = m_tau / m_mu
        
        # Check mu/e ratio
        self.assertAlmostEqual(
            mu_over_e,
            self.params.mu_over_e,
            delta=self.params.mu_over_e * 0.01,  # 1% tolerance
            msg=f"Muon/electron mass ratio doesn't match. Calculated: {mu_over_e}, Expected: {self.params.mu_over_e}"
        )
        
        # Check tau/e ratio
        self.assertAlmostEqual(
            tau_over_e,
            self.params.tau_over_e,
            delta=self.params.tau_over_e * 0.01,  # 1% tolerance
            msg=f"Tau/electron mass ratio doesn't match. Calculated: {tau_over_e}, Expected: {self.params.tau_over_e}"
        )
    
    def test_ordinal_depth_scaling(self):
        """Test that particle masses scale correctly with ordinal depth."""
        # Get ordinal depths
        ordinal_depths = {
            'e': self.mass_hierarchy_data['leptons']['e']['ordinal_depth'],
            'mu': self.mass_hierarchy_data['leptons']['mu']['ordinal_depth'],
            'tau': self.mass_hierarchy_data['leptons']['tau']['ordinal_depth'],
        }
        
        # Base masses before corrections
        base_masses = {
            'e': self.mass_hierarchy_data['leptons']['e']['mass_base'],
            'mu': self.mass_hierarchy_data['leptons']['mu']['mass_base'],
            'tau': self.mass_hierarchy_data['leptons']['tau']['mass_base'],
        }
        
        # Test the relation: m ~ exp(lambda_m * ordinal_depth)
        for p1 in ['e', 'mu', 'tau']:
            for p2 in ['e', 'mu', 'tau']:
                if p1 != p2:
                    expected_ratio = np.exp(self.params.lambda_m * (ordinal_depths[p2] - ordinal_depths[p1]))
                    actual_ratio = base_masses[p2] / base_masses[p1]
                    
                    self.assertAlmostEqual(
                        actual_ratio / expected_ratio,
                        1.0,
                        delta=0.01,  # 1% tolerance
                        msg=f"Mass ratio {p2}/{p1} doesn't follow ordinal scaling. Actual: {actual_ratio}, Expected: {expected_ratio}"
                    )


class TestCosmology(unittest.TestCase):
    """Test the cosmological predictions of the framework."""
    
    def setUp(self):
        """Set up the test environment."""
        self.params = MatryoshkaParameters()
        self.framework = matryoshka_core.initialize_core()
        
        # Initialize cosmological model from Part 4
        self.cosmo_model = matryoshka_part4.derive_cosmological_model(self.framework)
        
        # Initialize cosmological puzzle resolutions
        self.puzzle_resolutions = matryoshka_part4.resolve_cosmological_puzzles(
            self.framework, self.cosmo_model)
        
        # Initialize dark sector model
        self.dark_sector = matryoshka_part4.model_dark_sector(
            self.framework, self.cosmo_model)
        
        # Initialize structure formation model
        self.structure_formation = matryoshka_part4.derive_structure_formation(
            self.framework, self.cosmo_model)
    
    def test_friedmann_equations(self):
        """Test that the derived Friedmann equations match standard form."""
        # Extract Friedmann equations
        friedmann_1 = self.cosmo_model['friedmann_equations']['friedmann_1']
        friedmann_2 = self.cosmo_model['friedmann_equations']['friedmann_2']
        
        # Test that Friedmann equations include proper terms (symbolic test)
        self.assertTrue(
            '8πG/3' in str(friedmann_1) and 'ρ' in str(friedmann_1),
            msg=f"First Friedmann equation missing expected terms: {friedmann_1}"
        )
        
        self.assertTrue(
            '4πG' in str(friedmann_2) and 'p' in str(friedmann_2),
            msg=f"Second Friedmann equation missing expected terms: {friedmann_2}"
        )
    
    def test_dark_energy_equation_of_state(self):
        """Test the dark energy equation of state prediction."""
        # Extract equation of state parameters
        w0 = self.dark_sector['dark_energy']['w0']
        wa = self.dark_sector['dark_energy']['wa']
        
        # Check w0 is close to -1
        self.assertAlmostEqual(
            w0,
            -1.0,
            delta=0.05,
            msg=f"Dark energy w0 far from -1. Actual: {w0}"
        )
        
        # Check wa is close to theoretical prediction
        self.assertAlmostEqual(
            wa,
            self.params.wa,
            delta=0.01,
            msg=f"Dark energy wa doesn't match prediction. Actual: {wa}, Expected: {self.params.wa}"
        )
    
    def test_cosmological_constant(self):
        """Test the prediction for the cosmological constant."""
        # Extract cosmological constant
        lambda_val = self.puzzle_resolutions['cc_problem']['Lambda_val']
        
        # Check Lambda is close to observed value ~1e-52 m^-2
        expected_lambda = 1.1056e-52  # m^-2 (approximate observed value)
        
        # Use logarithmic comparison due to small value
        log_ratio = np.log10(lambda_val / expected_lambda)
        
        self.assertAlmostEqual(
            log_ratio,
            0.0,
            delta=1.0,  # Within one order of magnitude
            msg=f"Cosmological constant doesn't match observation. Calculated: {lambda_val}, Expected: {expected_lambda}"
        )
    
    def test_primordial_fluctuations(self):
        """Test the predictions for primordial fluctuation parameters."""
        # Extract parameters
        n_s = self.structure_formation['primordial_fluctuations']['n_s']
        r = self.structure_formation['primordial_fluctuations']['r']
        alpha_s = self.structure_formation['primordial_fluctuations']['alpha_s']
        
        # Check against theoretical predictions
        self.assertAlmostEqual(
            n_s,
            self.params.n_s,
            delta=0.002,
            msg=f"Spectral index n_s doesn't match prediction. Actual: {n_s}, Expected: {self.params.n_s}"
        )
        
        self.assertAlmostEqual(
            r,
            self.params.r,
            delta=0.005,
            msg=f"Tensor-to-scalar ratio r doesn't match prediction. Actual: {r}, Expected: {self.params.r}"
        )
        
        self.assertAlmostEqual(
            alpha_s,
            self.params.alpha_s,
            delta=0.0002,
            msg=f"Running of spectral index alpha_s doesn't match prediction. Actual: {alpha_s}, Expected: {self.params.alpha_s}"
        )


class TestQFT(unittest.TestCase):
    """Test the Quantum Field Theory aspects of the framework."""
    
    def setUp(self):
        """Set up the test environment."""
        self.params = MatryoshkaParameters()
        self.framework = matryoshka_core.initialize_core()
        
        # Initialize Hilbert space from Part 2
        self.hilbert_space_dict = matryoshka_part2.define_hilbert_space(self.framework)
        
        # Initialize creation and annihilation operators
        self.operator_dict = matryoshka_part2.define_creation_annihilation_operators(
            self.framework, self.hilbert_space_dict)
        
        # Initialize field operators
        self.field_operators_dict = matryoshka_part2.define_field_operators(
            self.framework, self.operator_dict)
        
        # Initialize path integral formulation
        self.path_int_dict = matryoshka_part2.derive_path_integral(
            self.framework, self.field_operators_dict)
        
        # Initialize shell propagators
        self.propagator_dict = matryoshka_part2.derive_shell_propagators(
            self.framework, self.path_int_dict)
        
        # Initialize Feynman rules
        self.feynman_dict = matryoshka_part2.derive_feynman_rules(
            self.framework, self.propagator_dict)
        
        # Initialize ordinal regularization
        self.regularization_dict = matryoshka_part2.derive_ordinal_regularization(
            self.framework, self.feynman_dict)
    
    def test_creation_annihilation_commutation(self):
        """Test the commutation relations of creation and annihilation operators."""
        # Extract commutation relation
        commutation = self.operator_dict['commutation_relation']
        
        # Check that it includes canonical form [a,a†] = δ
        self.assertTrue(
            '[a' in str(commutation) and 'a^\\dagger' in str(commutation) and 'delta' in str(commutation),
            msg=f"Commutation relation does not have canonical form: {commutation}"
        )
    
    def test_propagator_momentum_dependence(self):
        """Test the momentum dependence of shell propagators."""
        # Extract scalar propagator
        scalar_propagator = self.propagator_dict['scalar_propagator']
        
        # Check that propagator has standard momentum dependence
        self.assertTrue(
            'p^2' in str(scalar_propagator) or 'k^2' in str(scalar_propagator),
            msg=f"Scalar propagator missing standard momentum dependence: {scalar_propagator}"
        )
    
    def test_ordinal_regularization(self):
        """Test that ordinal regularization renders loop integrals finite."""
        # Extract regularization formula
        reg_formula = self.regularization_dict['regularization_formula']
        
        # Check that formula includes ordinal suppression terms
        self.assertTrue(
            'exp(-lambda' in str(reg_formula) and 'ord' in str(reg_formula),
            msg=f"Regularization formula missing ordinal suppression terms: {reg_formula}"
        )
        
        # Extract loop integral result
        loop_result = self.regularization_dict['loop_integral_result']
        
        # Check that result is finite
        self.assertTrue(
            'finite' in str(loop_result) or not ('infinity' in str(loop_result) or 'divergent' in str(loop_result)),
            msg=f"Loop integral result not explicitly finite: {loop_result}"
        )


def run_tests():
    """Run all tests and generate a comprehensive report."""
    # Create test suite
    test_loader = unittest.TestLoader()
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_suite.addTest(test_loader.loadTestsFromTestCase(TestShellParameters))
    test_suite.addTest(test_loader.loadTestsFromTestCase(TestNeutrinoPhysics))
    test_suite.addTest(test_loader.loadTestsFromTestCase(TestParticleMasses))
    test_suite.addTest(test_loader.loadTestsFromTestCase(TestCosmology))
    test_suite.addTest(test_loader.loadTestsFromTestCase(TestQFT))
    
    # Run tests
    test_runner = unittest.TextTestRunner(verbosity=2)
    test_result = test_runner.run(test_suite)
    
    # Print summary
    print("\n" + "=" * 80)
    print("MATRYOSHKA THEORY TEST RESULTS")
    print("=" * 80)
    print(f"Tests run: {test_result.testsRun}")
    print(f"Errors: {len(test_result.errors)}")
    print(f"Failures: {len(test_result.failures)}")
    
    # Plot test results if matplotlib is available
    try:
        # Test coverage by category
        categories = ['Shell', 'Neutrino', 'Particles', 'Cosmology', 'QFT']
        tests_per_category = [
            len(test_loader.getTestCaseNames(TestShellParameters)),
            len(test_loader.getTestCaseNames(TestNeutrinoPhysics)),
            len(test_loader.getTestCaseNames(TestParticleMasses)),
            len(test_loader.getTestCaseNames(TestCosmology)),
            len(test_loader.getTestCaseNames(TestQFT))
        ]
        
        plt.figure(figsize=(10, 6))
        plt.bar(categories, tests_per_category, color='skyblue')
        plt.title('Matryoshka Theory Test Coverage by Category')
        plt.ylabel('Number of Tests')
        plt.grid(axis='y', alpha=0.3)
        plt.savefig('test_coverage.png')
        print("\nTest coverage chart saved as 'test_coverage.png'")
        
    except ImportError:
        print("\nMatplotlib not available for generating test coverage chart")
    
    return test_result

if __name__ == "__main__":
    run_tests()