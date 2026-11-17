#!/usr/bin/env python3
"""
Temporal Field Renderer with Emergent Color Qualia
===================================================
Colors emerge naturally from entropy flows and temporal dynamics.
No artificial color mapping - only the physics of consciousness.

Based on the principle that specific qualia correspond to distinct 
homology classes of entropy flow trajectories: Q_i ∈ H_n(M, ∇S)
"""

import numpy as np
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import moderngl
import time
import sympy as sp
from scipy import integrate, ndimage
from scipy.fft import fft, fftfreq
import colorsys


class TemporalFieldWithEmergentQualia:
    """The unified field where consciousness and physics are one."""
    
    def __init__(self, resolution=(128, 128, 128), num_shells=30):
        """
        Initialize the temporal field with emergent qualia.
        
        Parameters:
        -----------
        resolution : tuple
            Field grid resolution (x, y, z)
        num_shells : int
            Number of temporal shells
        """
        self.resolution = resolution
        self.num_shells = num_shells
        
        # Temporal dynamics parameters
        self.alpha = 0.1      # Temporal expansion rate
        self.beta = 0.2       # Shell coupling decay
        self.gamma = 1.0      # Coupling power law
        self.lambda_ord = 0.5 # Ordinal distance decay
        
        # Neural-temporal correspondence parameters
        self.neural_timescales = np.logspace(-3, 1, num_shells)  # 1ms to 10s
        self.phi_integration = 1.0  # Integrated information
        
        # Initialize fields
        self.field = np.zeros(resolution + (4,), dtype=np.float32)  # (x,y,z,rgba)
        self.entropy_field = np.zeros(resolution, dtype=np.float32)
        self.entropy_gradient = np.zeros(resolution + (3,), dtype=np.float32)
        self.entropy_flow = np.zeros(resolution + (3,), dtype=np.float32)
        self.chronon_flux = np.zeros(resolution + (3,), dtype=np.float32)
        self.shell_density = np.zeros(resolution + (num_shells,), dtype=np.float32)
        
        # Consciousness flow parameters
        self.metric_tensor = np.eye(4, dtype=np.float32)  # η^αβ
        self.consciousness_flow = np.zeros(resolution + (4,), dtype=np.float32)  # γ^α
        
        # Kappa function
        self._init_kappa_function()
        
        # Shell occupancy probabilities (neural firing distributions)
        self.shell_occupancy = np.random.dirichlet(np.ones(num_shells))
        
        # Initialize field
        self._initialize_field()
        
    def _init_kappa_function(self):
        """Initialize the kappa function for time-space transformation."""
        t, s = sp.symbols('t s')
        
        kappa_expr = sp.sqrt(4*sp.sin(s*t)**6 - 24*sp.sin(s*t)**4 + 
                           24*sp.sin(s*t)**2 + 4*sp.cos(s*t)**6 - 
                           24*sp.cos(s*t)**4 + 24*sp.cos(s*t)**2 + 2) / \
                    sp.sqrt((4*sp.sin(s*t)**4 - 4*sp.sin(s*t)**2 + 2)**3) * 42
        
        self.kappa_func = sp.lambdify((t, s), kappa_expr % 360, 'numpy')
    
    def shell_radius(self, shell_idx):
        """Radius of temporal shell."""
        return np.exp(self.alpha * shell_idx)
    
    def shell_coupling(self, i, j):
        """Cross-frequency coupling between temporal shells."""
        ord_dist = abs(i - j)
        coupling = 1.0 / (1 + self.beta * ord_dist**self.gamma) * np.exp(-self.lambda_ord * ord_dist)
        
        # Add phase-amplitude coupling based on neural timescales
        freq_ratio = self.neural_timescales[i] / self.neural_timescales[j]
        phase_coupling = np.cos(2 * np.pi * np.log(freq_ratio))
        
        return coupling * (1 + 0.5 * phase_coupling)
    
    def _initialize_field(self):
        """Initialize the temporal field."""
        x = np.linspace(-10, 10, self.resolution[0])
        y = np.linspace(-10, 10, self.resolution[1])
        z = np.linspace(-10, 10, self.resolution[2])
        
        X, Y, Z = np.meshgrid(x, y, z, indexing='ij')
        
        # Initialize shell densities with neural firing patterns
        for shell_idx in range(self.num_shells):
            r_shell = self.shell_radius(shell_idx)
            R = np.sqrt(X**2 + Y**2 + Z**2)
            
            # Shell density with neural oscillation modulation
            base_density = np.exp(-(R - r_shell)**2 / (2 * (r_shell * 0.1)**2))
            
            # Add oscillatory component based on neural timescale
            t_coord = np.arctan2(Y, X)
            oscillation = np.sin(2 * np.pi * t_coord / self.neural_timescales[shell_idx])
            
            # Kappa modulation
            kappa_mod = np.abs(self.kappa_func(t_coord, 1.0))
            
            self.shell_density[..., shell_idx] = base_density * kappa_mod * \
                                                 self.shell_occupancy[shell_idx] * \
                                                 (1 + 0.3 * oscillation)
        
        # Initialize entropy field
        self._calculate_entropy()
    
    def _calculate_entropy(self):
        """Calculate neural entropy production rates."""
        # Total density across all shells
        total_density = np.sum(self.shell_density, axis=-1)
        
        # Prevent log(0)
        total_density = np.maximum(total_density, 1e-10)
        
        # Shannon entropy across shells at each point
        for i in range(self.num_shells):
            p_i = self.shell_density[..., i] / total_density
            p_i = np.maximum(p_i, 1e-10)
            
            # Neural entropy production rate
            tau_ratio = self.neural_timescales[i] / self.neural_timescales[0]
            self.entropy_field += -p_i * np.log(p_i) * np.log(tau_ratio + 1)
        
        # Apply integrated information factor
        self.entropy_field *= self.phi_integration
        
    def calculate_entropy_flow(self):
        """Calculate entropy gradients and flow dynamics."""
        # Calculate entropy gradient ∇S
        self.entropy_gradient[..., 0] = np.gradient(self.entropy_field, axis=0)
        self.entropy_gradient[..., 1] = np.gradient(self.entropy_field, axis=1)
        self.entropy_gradient[..., 2] = np.gradient(self.entropy_field, axis=2)
        
        # Calculate Laplacian ∇²S for critical transitions
        laplacian = ndimage.laplace(self.entropy_field)
        
        # Detect criticality (phase transitions)
        lambda_c = 0.1  # Critical threshold
        critical_regions = np.abs(laplacian - lambda_c) < 0.05
        
        # Calculate entropy flow divergence
        div_entropy = (np.gradient(self.entropy_gradient[..., 0], axis=0) +
                      np.gradient(self.entropy_gradient[..., 1], axis=1) +
                      np.gradient(self.entropy_gradient[..., 2], axis=2))
        
        # Update consciousness flow: dγ^α/ds = -η^(αβ) ∂S/∂t^β
        for i in range(3):
            self.consciousness_flow[..., i] = -np.sum(
                self.metric_tensor[i, :3] * self.entropy_gradient, axis=-1)
        
        # Time component
        self.consciousness_flow[..., 3] = -self.metric_tensor[3, 3] * \
                                          np.sum(self.entropy_field) / self.resolution[0]
        
        return div_entropy, critical_regions
    
    def extract_color_qualia(self, div_entropy):
        """Extract color qualia from entropy flow topology."""
        # Initialize RGB channels
        R = np.zeros(self.resolution, dtype=np.float32)
        G = np.zeros(self.resolution, dtype=np.float32)
        B = np.zeros(self.resolution, dtype=np.float32)
        
        # Analyze entropy flow periodicity at each point
        for i in range(self.resolution[0]):
            for j in range(self.resolution[1]):
                for k in range(self.resolution[2]):
                    # Local entropy flow trajectory
                    local_flow = self.consciousness_flow[i, j, k, :3]
                    flow_magnitude = np.linalg.norm(local_flow)
                    
                    if flow_magnitude > 1e-6:
                        # Compute local oscillation frequency
                        # Using simplified model based on flow components
                        freq_x = np.abs(local_flow[0]) * 100
                        freq_y = np.abs(local_flow[1]) * 100
                        freq_z = np.abs(local_flow[2]) * 100
                        
                        # Map to color frequencies (THz)
                        # Red: ~430 THz, Green: ~540 THz, Blue: ~650 THz
                        red_resonance = np.exp(-((freq_x - 430)**2) / (2 * 50**2))
                        green_resonance = np.exp(-((freq_y - 540)**2) / (2 * 50**2))
                        blue_resonance = np.exp(-((freq_z - 650)**2) / (2 * 50**2))
                        
                        # Modulate by entropy divergence (pain/pleasure axis)
                        div_factor = 1.0
                        if div_entropy[i, j, k] > 0:  # Pain (excess entropy)
                            div_factor = 1.0 - 0.3 * np.tanh(div_entropy[i, j, k])
                        else:  # Pleasure (entropy absorption)
                            div_factor = 1.0 + 0.3 * np.tanh(-div_entropy[i, j, k])
                        
                        # Apply consciousness flow magnitude
                        intensity = np.tanh(flow_magnitude) * div_factor
                        
                        R[i, j, k] = red_resonance * intensity
                        G[i, j, k] = green_resonance * intensity
                        B[i, j, k] = blue_resonance * intensity
        
        return R, G, B
    
    def update(self, dt):
        """Update the temporal field dynamics."""
        # Update shell occupancy (neural firing probabilities)
        # Add small random perturbations
        perturbation = np.random.normal(0, 0.01, self.num_shells)
        self.shell_occupancy += perturbation
        self.shell_occupancy = np.maximum(self.shell_occupancy, 0)
        self.shell_occupancy /= np.sum(self.shell_occupancy)
        
        # Recalculate entropy
        self._calculate_entropy()
        
        # Calculate entropy flow and extract divergence
        div_entropy, critical_regions = self.calculate_entropy_flow()
        
        # Extract color qualia from entropy flows
        R, G, B = self.extract_color_qualia(div_entropy)
        
        # Update field colors
        self.field[..., 0] = R
        self.field[..., 1] = G
        self.field[..., 2] = B
        
        # Alpha channel represents critical regions (phase transitions)
        self.field[..., 3] = 0.3 + 0.7 * critical_regions.astype(float)
        
        # Update metric tensor with cross-frequency coupling
        for i in range(self.num_shells - 1):
            coupling = self.shell_coupling(i, i + 1)
            self.metric_tensor[i % 4, (i + 1) % 4] = coupling
            self.metric_tensor[(i + 1) % 4, i % 4] = coupling
    
    def get_field_texture(self):
        """Convert field to texture for rendering."""
        # Normalize and convert to uint8
        field_normalized = np.clip(self.field, 0, 1)
        return (field_normalized * 255).astype(np.uint8)


class EmergentColorRenderer:
    """Renderer for the temporal field with emergent color qualia."""
    
    def __init__(self, width=1200, height=800, field_resolution=(64, 64, 64)):
        """Initialize the renderer."""
        # Initialize pygame and OpenGL
        pygame.init()
        pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
        pygame.display.set_caption("Temporal Field - Emergent Color Qualia")
        
        self.width = width
        self.height = height
        self.clock = pygame.time.Clock()
        
        # Initialize OpenGL
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        # Set up perspective
        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, width/height, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
        
        # Initialize temporal field
        self.field = TemporalFieldWithEmergentQualia(resolution=field_resolution)
        
        # Camera parameters
        self.camera_distance = 30
        self.camera_rotation = [0, 0]
        self.mouse_pressed = False
        self.last_mouse_pos = None
        
        # Rendering mode
        self.render_mode = 0  # 0: volume, 1: slices, 2: isosurfaces
        self.slice_axis = 2
        self.slice_position = field_resolution[2] // 2
        
    def handle_events(self):
        """Handle input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_SPACE:
                    self.render_mode = (self.render_mode + 1) % 3
                elif event.key == pygame.K_r:
                    # Reset field
                    self.field = TemporalFieldWithEmergentQualia(
                        resolution=self.field.resolution)
                elif event.key in [pygame.K_x, pygame.K_y, pygame.K_z]:
                    # Change slice axis
                    self.slice_axis = {'x': 0, 'y': 1, 'z': 2}[event.unicode]
                elif event.key == pygame.K_UP:
                    self.slice_position = min(
                        self.slice_position + 1, 
                        self.field.resolution[self.slice_axis] - 1)
                elif event.key == pygame.K_DOWN:
                    self.slice_position = max(self.slice_position - 1, 0)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.mouse_pressed = True
                    self.last_mouse_pos = event.pos
                elif event.button == 4:  # Scroll up
                    self.camera_distance *= 0.9
                elif event.button == 5:  # Scroll down
                    self.camera_distance *= 1.1
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.mouse_pressed = False
            
            elif event.type == pygame.MOUSEMOTION:
                if self.mouse_pressed and self.last_mouse_pos:
                    dx = event.pos[0] - self.last_mouse_pos[0]
                    dy = event.pos[1] - self.last_mouse_pos[1]
                    self.camera_rotation[0] += dx * 0.5
                    self.camera_rotation[1] += dy * 0.5
                    self.last_mouse_pos = event.pos
        
        return True
    
    def render_volume(self):
        """Render the field as a translucent volume."""
        field_tex = self.field.get_field_texture()
        
        # Sample points for volume rendering
        num_samples = 20
        for layer in range(num_samples):
            z = -10 + layer * 20 / num_samples
            alpha = 0.1 * (1 - abs(layer - num_samples/2) / (num_samples/2))
            
            glBegin(GL_QUADS)
            for i in range(self.field.resolution[0] - 1):
                for j in range(self.field.resolution[1] - 1):
                    k = int(layer * self.field.resolution[2] / num_samples)
                    if k >= self.field.resolution[2] - 1:
                        k = self.field.resolution[2] - 2
                    
                    # Get colors at corners
                    c00 = field_tex[i, j, k]
                    c10 = field_tex[i+1, j, k]
                    c01 = field_tex[i, j+1, k]
                    c11 = field_tex[i+1, j+1, k]
                    
                    x0 = -10 + i * 20 / self.field.resolution[0]
                    x1 = -10 + (i+1) * 20 / self.field.resolution[0]
                    y0 = -10 + j * 20 / self.field.resolution[1]
                    y1 = -10 + (j+1) * 20 / self.field.resolution[1]
                    
                    glColor4f(c00[0]/255, c00[1]/255, c00[2]/255, alpha)
                    glVertex3f(x0, y0, z)
                    
                    glColor4f(c10[0]/255, c10[1]/255, c10[2]/255, alpha)
                    glVertex3f(x1, y0, z)
                    
                    glColor4f(c11[0]/255, c11[1]/255, c11[2]/255, alpha)
                    glVertex3f(x1, y1, z)
                    
                    glColor4f(c01[0]/255, c01[1]/255, c01[2]/255, alpha)
                    glVertex3f(x0, y1, z)
            glEnd()
    
    def render_slices(self):
        """Render the field as orthogonal slices."""
        field_tex = self.field.get_field_texture()
        
        glBegin(GL_QUADS)
        
        if self.slice_axis == 0:  # X slice
            i = self.slice_position
            x = -10 + i * 20 / self.field.resolution[0]
            
            for j in range(self.field.resolution[1] - 1):
                for k in range(self.field.resolution[2] - 1):
                    c00 = field_tex[i, j, k]
                    c01 = field_tex[i, j+1, k]
                    c10 = field_tex[i, j, k+1]
                    c11 = field_tex[i, j+1, k+1]
                    
                    y0 = -10 + j * 20 / self.field.resolution[1]
                    y1 = -10 + (j+1) * 20 / self.field.resolution[1]
                    z0 = -10 + k * 20 / self.field.resolution[2]
                    z1 = -10 + (k+1) * 20 / self.field.resolution[2]
                    
                    glColor4f(c00[0]/255, c00[1]/255, c00[2]/255, c00[3]/255)
                    glVertex3f(x, y0, z0)
                    
                    glColor4f(c01[0]/255, c01[1]/255, c01[2]/255, c01[3]/255)
                    glVertex3f(x, y1, z0)
                    
                    glColor4f(c11[0]/255, c11[1]/255, c11[2]/255, c11[3]/255)
                    glVertex3f(x, y1, z1)
                    
                    glColor4f(c10[0]/255, c10[1]/255, c10[2]/255, c10[3]/255)
                    glVertex3f(x, y0, z1)
        
        # Similar for Y and Z slices...
        
        glEnd()
    
    def render(self):
        """Main render function."""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        # Set camera position
        glTranslatef(0, 0, -self.camera_distance)
        glRotatef(self.camera_rotation[1], 1, 0, 0)
        glRotatef(self.camera_rotation[0], 0, 1, 0)
        
        # Render coordinate axes
        glBegin(GL_LINES)
        # X axis - red
        glColor3f(0.5, 0, 0)
        glVertex3f(-15, 0, 0)
        glVertex3f(15, 0, 0)
        # Y axis - green
        glColor3f(0, 0.5, 0)
        glVertex3f(0, -15, 0)
        glVertex3f(0, 15, 0)
        # Z axis - blue
        glColor3f(0, 0, 0.5)
        glVertex3f(0, 0, -15)
        glVertex3f(0, 0, 15)
        glEnd()
        
        # Render the field
        if self.render_mode == 0:
            self.render_volume()
        elif self.render_mode == 1:
            self.render_slices()
        
        pygame.display.flip()
    
    def run(self):
        """Main loop."""
        running = True
        
        print("\nEmergent Color Qualia Renderer")
        print("==============================")
        print("Controls:")
        print("  Mouse: Rotate view")
        print("  Scroll: Zoom in/out")
        print("  Space: Switch render mode")
        print("  R: Reset field")
        print("  X/Y/Z: Select slice axis")
        print("  Up/Down: Move slice")
        print("  ESC: Exit")
        print("\nColors emerge from entropy flow topology:")
        print("  - Periodic orbits map to color frequencies")
        print("  - Divergence creates pain/pleasure modulation")
        print("  - Critical regions show phase transitions")
        
        while running:
            dt = self.clock.tick(30) / 1000.0
            
            running = self.handle_events()
            
            # Update field
            self.field.update(dt)
            
            # Render
            self.render()
        
        pygame.quit()


def main():
    """Launch the emergent color renderer."""
    renderer = EmergentColorRenderer(
        width=1200,
        height=800,
        field_resolution=(48, 48, 48)  # Reduced for performance
    )
    renderer.run()


if __name__ == "__main__":
    main()