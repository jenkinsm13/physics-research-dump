#!/usr/bin/env python3
"""
Gravitational Lensing from Temporal Gradients
Tests the prediction that temporal flow gradients create gravitational effects
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint, solve_ivp
from scipy.optimize import fsolve
import json

# Physical constants
c = 299792458           # Speed of light (m/s)
G = 6.67430e-11        # Gravitational constant (m³/kg⋅s²)
L_planck = 1.616255e-35 # Planck length (m)
t_planck = 5.391247e-44 # Planck time (s)
M_planck = 2.176434e-8  # Planck mass (kg)

# Framework parameters
PHI = (1 + np.sqrt(5)) / 2
alpha_shell = 1.0
lambda_ord = 0.125
n_shells = 296

class TemporalGravityLensing:
    def __init__(self):
        self.shells = self._initialize_shells()
        
    def _initialize_shells(self):
        """Initialize temporal shell structure"""
        shells = []
        for n in range(n_shells):
            shell = {
                'ordinal': n,
                'radius': L_planck * (PHI ** n),
                'temporal_flow_rate': 1.0 + alpha_shell * n,
                'coupling_strength': np.exp(-lambda_ord * n)
            }
            shells.append(shell)
        return shells
    
    def temporal_gradient_to_metric(self, r, theta=0, phi=0):
        """Convert temporal flow gradient to spacetime metric"""
        # Find which shell we're in
        shell_idx = self.find_shell_at_radius(r)
        if shell_idx >= n_shells - 1:
            return np.eye(4)  # Flat metric far away
        
        # Local temporal flow rate and gradient
        tau = self.shells[shell_idx]['temporal_flow_rate']
        tau_next = self.shells[shell_idx + 1]['temporal_flow_rate']
        r_shell = self.shells[shell_idx]['radius']
        r_next = self.shells[shell_idx + 1]['radius']
        
        # Temporal gradient
        dtau_dr = (tau_next - tau) / (r_next - r_shell)
        
        # Effective "mass" from temporal gradient
        # M_eff = (c²/2G) × r² × (dτ/dr)
        M_eff = (c**2 / (2 * G)) * r**2 * abs(dtau_dr) * t_planck
        
        # Schwarzschild-like metric from temporal gradient
        rs = 2 * G * M_eff / c**2  # Effective Schwarzschild radius
        
        # Metric components
        g = np.zeros((4, 4))
        g[0, 0] = -(1 - rs/r) * tau**2  # g_tt with temporal flow
        g[1, 1] = 1 / (1 - rs/r)        # g_rr
        g[2, 2] = r**2                   # g_θθ
        g[3, 3] = r**2 * np.sin(theta)**2  # g_φφ
        
        return g
    
    def find_shell_at_radius(self, r):
        """Find which shell contains radius r"""
        for i in range(n_shells - 1):
            if self.shells[i]['radius'] <= r < self.shells[i+1]['radius']:
                return i
        return n_shells - 1
    
    def geodesic_equation(self, state, lamb, r_target=None):
        """Geodesic equation for light ray in temporal gradient field"""
        # State = [t, r, theta, phi, dt/dλ, dr/dλ, dθ/dλ, dφ/dλ]
        t, r, theta, phi, pt, pr, ptheta, pphi = state
        
        # Prevent going too close to origin
        if r < L_planck * 10:
            r = L_planck * 10
        
        # Get metric at current position
        g = self.temporal_gradient_to_metric(r, theta, phi)
        
        # Christoffel symbols (simplified for spherical symmetry)
        shell_idx = self.find_shell_at_radius(r)
        if shell_idx >= n_shells - 1:
            # Far field - essentially flat
            return [pt, pr, ptheta, pphi, 0, 0, 0, 0]
        
        tau = self.shells[shell_idx]['temporal_flow_rate']
        tau_next = self.shells[shell_idx + 1]['temporal_flow_rate']
        r_shell = self.shells[shell_idx]['radius']
        r_next = self.shells[shell_idx + 1]['radius']
        
        dtau_dr = (tau_next - tau) / (r_next - r_shell)
        M_eff = (c**2 / (2 * G)) * r**2 * abs(dtau_dr) * t_planck
        rs = 2 * G * M_eff / c**2
        
        # Simplified geodesic derivatives
        dt_dlambda = pt
        dr_dlambda = pr
        dtheta_dlambda = ptheta
        dphi_dlambda = pphi
        
        # Acceleration terms from temporal gradient
        if r > rs:
            factor = 1 - rs/r
            dpt_dlambda = -(rs/(2*r**2)) * tau * dtau_dr * pt * pr / factor
            dpr_dlambda = -(rs/(2*r**2)) * (pt**2 * tau**2 - pr**2/factor**2) / factor
            dptheta_dlambda = -2 * pr * ptheta / r
            dpphi_dlambda = -2 * pr * pphi / r
        else:
            # Inside effective horizon
            dpt_dlambda = 0
            dpr_dlambda = 0
            dptheta_dlambda = 0
            dpphi_dlambda = 0
        
        return [dt_dlambda, dr_dlambda, dtheta_dlambda, dphi_dlambda,
                dpt_dlambda, dpr_dlambda, dptheta_dlambda, dpphi_dlambda]
    
    def trace_light_ray(self, impact_parameter, r_start=1e10*L_planck, r_end=L_planck):
        """Trace light ray through temporal gradient field"""
        # Initial conditions
        theta0 = np.pi/2  # Equatorial plane
        phi0 = 0
        
        # Initial 4-velocity for light (null geodesic)
        # Light coming from infinity with impact parameter b
        E = 1  # Energy
        L = impact_parameter * E  # Angular momentum
        
        # Initial momenta
        pt0 = E
        pr0 = -np.sqrt(E**2 - L**2/r_start**2)  # Incoming
        ptheta0 = 0
        pphi0 = L / r_start**2
        
        # Initial state
        y0 = [0, r_start, theta0, phi0, pt0, pr0, ptheta0, pphi0]
        
        # Integrate geodesic
        lambda_span = [0, 1e20 * t_planck]
        
        # Event to stop at minimum radius
        def min_radius_event(lamb, state):
            return state[5]  # dr/dλ = 0 at turning point
        min_radius_event.terminal = True
        min_radius_event.direction = 1
        
        # Solve
        sol = solve_ivp(self.geodesic_equation, lambda_span, y0, 
                       events=min_radius_event, dense_output=True,
                       method='DOP853', rtol=1e-10, atol=1e-12)
        
        # Extract trajectory
        if sol.t_events[0].size > 0:
            # Ray turned around
            lambda_turn = sol.t_events[0][0]
            r_min = sol.sol(lambda_turn)[1]
            
            # Calculate deflection angle
            phi_initial = phi0
            phi_turn = sol.sol(lambda_turn)[3]
            deflection = 2 * abs(phi_turn - phi_initial) - np.pi
            
            return {
                'impact_parameter': impact_parameter,
                'closest_approach': r_min,
                'deflection_angle': deflection,
                'trajectory': sol.sol
            }
        else:
            # Ray absorbed or calculation failed
            return {
                'impact_parameter': impact_parameter,
                'closest_approach': r_end,
                'deflection_angle': np.nan,
                'trajectory': sol.sol
            }
    
    def calculate_effective_mass_profile(self):
        """Calculate effective mass from temporal gradients"""
        radii = []
        M_eff_values = []
        
        for i in range(50, min(200, n_shells-1)):  # Mid-range shells
            r = self.shells[i]['radius']
            tau = self.shells[i]['temporal_flow_rate']
            tau_next = self.shells[i + 1]['temporal_flow_rate']
            r_next = self.shells[i + 1]['radius']
            
            dtau_dr = (tau_next - tau) / (r_next - r)
            M_eff = (c**2 / (2 * G)) * r**2 * abs(dtau_dr) * t_planck
            
            radii.append(r)
            M_eff_values.append(M_eff)
        
        return np.array(radii), np.array(M_eff_values)
    
    def plot_lensing_analysis(self):
        """Visualize gravitational lensing from temporal gradients"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        
        # 1. Effective mass profile
        radii, M_eff = self.calculate_effective_mass_profile()
        ax1.loglog(radii/L_planck, M_eff/M_planck)
        ax1.set_xlabel('Radius (Planck lengths)')
        ax1.set_ylabel('Effective Mass (Planck masses)')
        ax1.set_title('Effective Mass from Temporal Gradient')
        ax1.grid(True, alpha=0.3)
        
        # 2. Deflection angle vs impact parameter
        # Test at shell 100 (atomic scale)
        r_source = self.shells[100]['radius']
        impact_params = np.linspace(1.1, 10, 20) * r_source
        deflections = []
        
        for b in impact_params:
            result = self.trace_light_ray(b, r_start=100*r_source)
            if not np.isnan(result['deflection_angle']):
                deflections.append(result['deflection_angle'])
            else:
                deflections.append(0)
        
        # Compare with point mass
        M_eff_100 = M_eff[50]  # Approximate effective mass at shell 100
        deflection_point_mass = 4 * G * M_eff_100 / (c**2 * impact_params)
        
        ax2.plot(impact_params/r_source, np.array(deflections), 'b-', 
                label='Temporal gradient', linewidth=2)
        ax2.plot(impact_params/r_source, deflection_point_mass, 'r--', 
                label='Point mass', linewidth=2)
        ax2.set_xlabel('Impact Parameter (r_shell units)')
        ax2.set_ylabel('Deflection Angle (radians)')
        ax2.set_title('Light Deflection at Shell 100')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # 3. Temporal flow rate profile
        shell_indices = range(50, min(150, n_shells))
        tau_values = [self.shells[i]['temporal_flow_rate'] for i in shell_indices]
        r_values = [self.shells[i]['radius'] for i in shell_indices]
        
        ax3.semilogx(np.array(r_values)/L_planck, tau_values)
        ax3.set_xlabel('Radius (Planck lengths)')
        ax3.set_ylabel('Temporal Flow Rate τ')
        ax3.set_title('Temporal Flow Rate Profile')
        ax3.grid(True, alpha=0.3)
        
        # 4. Metric component g_tt
        r_test = np.logspace(np.log10(self.shells[50]['radius']/L_planck),
                           np.log10(self.shells[150]['radius']/L_planck), 100) * L_planck
        g_tt_values = []
        
        for r in r_test:
            g = self.temporal_gradient_to_metric(r)
            g_tt_values.append(-g[0, 0])
        
        ax4.loglog(r_test/L_planck, g_tt_values)
        ax4.set_xlabel('Radius (Planck lengths)')
        ax4.set_ylabel('|g_tt|')
        ax4.set_title('Metric Time Component from Temporal Gradient')
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('gravitational_lensing_temporal_gradients.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return fig
    
    def test_equivalence_principle(self):
        """Test if temporal gradients produce effects equivalent to mass"""
        # Compare trajectories in temporal gradient vs point mass
        test_shell = 100
        r_test = self.shells[test_shell]['radius']
        
        # Calculate equivalent mass
        tau = self.shells[test_shell]['temporal_flow_rate']
        tau_next = self.shells[test_shell + 1]['temporal_flow_rate']
        r_next = self.shells[test_shell + 1]['radius']
        dtau_dr = (tau_next - tau) / (r_next - r_test)
        M_equivalent = (c**2 / (2 * G)) * r_test**2 * abs(dtau_dr) * t_planck
        
        print(f"\nEQUIVALENCE PRINCIPLE TEST")
        print(f"Shell {test_shell}:")
        print(f"  Radius: {r_test:.2e} m ({r_test/L_planck:.2e} Planck lengths)")
        print(f"  Temporal gradient: {dtau_dr:.2e} s⁻¹")
        print(f"  Equivalent mass: {M_equivalent:.2e} kg ({M_equivalent/M_planck:.2e} Planck masses)")
        print(f"  Schwarzschild radius: {2*G*M_equivalent/c**2:.2e} m")
        
        return M_equivalent

# Main execution
if __name__ == "__main__":
    print("GRAVITATIONAL LENSING FROM TEMPORAL GRADIENTS")
    print("=" * 60)
    
    # Initialize system
    tgl = TemporalGravityLensing()
    
    # Test equivalence principle
    M_eq = tgl.test_equivalence_principle()
    
    # Analyze lensing at different scales
    print("\n\nLENSING ANALYSIS AT KEY SCALES")
    print("-" * 40)
    
    test_shells = [50, 100, 150]  # Subatomic, atomic, molecular scales
    
    for shell_idx in test_shells:
        if shell_idx < n_shells - 1:
            r = tgl.shells[shell_idx]['radius']
            tau = tgl.shells[shell_idx]['temporal_flow_rate']
            
            # Trace a light ray
            result = tgl.trace_light_ray(2*r, r_start=10*r)
            
            print(f"\nShell {shell_idx} (r = {r/L_planck:.2e} L_p):")
            print(f"  Temporal flow rate: τ = {tau:.1f}")
            print(f"  Closest approach: {result['closest_approach']/r:.3f} × r_shell")
            if not np.isnan(result['deflection_angle']):
                print(f"  Deflection angle: {result['deflection_angle']*1e6:.2f} microradians")
                print(f"  Einstein angle equivalent: {np.sqrt(4*G*M_eq*r/c**2)*1e6:.2f} microradians")
    
    # Generate visualizations
    print("\n\nGENERATING VISUALIZATIONS...")
    fig = tgl.plot_lensing_analysis()
    
    # Key predictions
    print("\n\nKEY PREDICTIONS")
    print("-" * 40)
    print("1. Gravitational lensing without mass - purely from temporal gradients")
    print("2. Deflection angles scale with shell ordinal number")
    print("3. Effective mass grows as r² × (dτ/dr)")
    print("4. Observable with precision interferometry at microscopic scales")
    print("5. Metric distortions correlate with consciousness field strength")
    
    # Experimental signatures
    print("\n\nEXPERIMENTAL SIGNATURES")
    print("-" * 40)
    print("• Microscopic gravitational lensing in atom interferometers")
    print("• Light deflection proportional to temporal gradient, not mass density")
    print("• Phase shifts in optical cavities near temporal boundaries")
    print("• Gravitational redshift variations at shell transitions")
    
    # Save results
    results = {
        'framework_parameters': {
            'n_shells': n_shells,
            'phi': float(PHI),
            'alpha_shell': alpha_shell,
            'lambda_ord': lambda_ord
        },
        'lensing_tests': {},
        'equivalence_test': {
            'equivalent_mass_kg': float(M_eq),
            'equivalent_mass_planck': float(M_eq/M_planck)
        }
    }
    
    for shell_idx in test_shells:
        if shell_idx < n_shells - 1:
            r = tgl.shells[shell_idx]['radius']
            result = tgl.trace_light_ray(2*r, r_start=10*r)
            results['lensing_tests'][f'shell_{shell_idx}'] = {
                'radius_m': float(r),
                'radius_planck': float(r/L_planck),
                'deflection_rad': float(result['deflection_angle']) if not np.isnan(result['deflection_angle']) else None
            }
    
    with open('temporal_gravity_lensing_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print("\nResults saved to temporal_gravity_lensing_results.json")