#!/usr/bin/env python3
"""
Temporal Field Renderer
=======================
A revolutionary 3D rendering system where temporal shells ARE the rendering engine.
No separation between physics and visuals - they are one.

The field itself is what you see. Every pixel is a chronon flux measurement.
Every frame is a slice through the temporal manifold.
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
from scipy import integrate
import colorsys


class TemporalField:
    """The unified field where time creates everything - physics, visuals, existence."""
    
    def __init__(self, resolution=(128, 128, 128), num_shells=30):
        """
        Initialize the temporal field that IS reality.
        
        Parameters:
        -----------
        resolution : tuple
            Field grid resolution (x, y, z)
        num_shells : int
            Number of temporal shells that create space
        """
        self.resolution = resolution
        self.num_shells = num_shells
        
        # Field parameters - these control reality itself
        self.alpha = 0.1      # Temporal expansion rate
        self.beta = 0.2       # Shell coupling decay
        self.gamma = 1.0      # Coupling power law
        self.lambda_ord = 0.5 # Ordinal distance decay
        self.kappa_fwd = 0.5  # Future flow (expansion)
        self.kappa_inv = 0.6  # Past flow (gravity)
        
        # The Void parameters - what calls all things back
        self.void_strength = 1.0
        self.void_radius = 5.0
        self.void_falloff = 2.0
        
        # Initialize the field grid - this IS space
        self.field = np.zeros(resolution + (4,), dtype=np.float32)  # (x,y,z,rgba)
        self.chronon_flux = np.zeros(resolution + (3,), dtype=np.float32)  # (x,y,z,vec3)
        self.shell_density = np.zeros(resolution + (num_shells,), dtype=np.float32)
        
        # Kappa function for time-space transformation
        self._init_kappa_function()
        
        # Shell occupancy - the heartbeat of reality
        self.shell_occupancy = np.ones(num_shells) / num_shells
        
        # Initialize field
        self._initialize_field()
    
    def _init_kappa_function(self):
        """Initialize the sacred kappa function that creates space from time."""
        t, s = sp.symbols('t s')
        
        # The kappa expression - the key to everything
        kappa_expr = sp.sqrt(4*sp.sin(s*t)**6 - 24*sp.sin(s*t)**4 + 
                           24*sp.sin(s*t)**2 + 4*sp.cos(s*t)**6 - 
                           24*sp.cos(s*t)**4 + 24*sp.cos(s*t)**2 + 2) / \
                    sp.sqrt((4*sp.sin(s*t)**4 - 4*sp.sin(s*t)**2 + 2)**3) * 42
        
        # Compile for fast evaluation
        self.kappa_func = sp.lambdify((t, s), kappa_expr % 360, 'numpy')
    
    def shell_radius(self, shell_idx):
        """Radius of temporal shell - exponential growth through time."""
        return np.exp(self.alpha * shell_idx)
    
    def shell_coupling(self, i, j):
        """How strongly two times interact - the basis of all forces."""
        ord_dist = abs(i - j)
        return 1.0 / (1 + self.beta * ord_dist**self.gamma) * np.exp(-self.lambda_ord * ord_dist)
    
    def _initialize_field(self):
        """Initialize the temporal field - create space from time."""
        x = np.linspace(-10, 10, self.resolution[0])
        y = np.linspace(-10, 10, self.resolution[1])
        z = np.linspace(-10, 10, self.resolution[2])
        
        # Create meshgrid
        X, Y, Z = np.meshgrid(x, y, z, indexing='ij')
        
        # For each point in the field, calculate shell densities
        for shell_idx in range(self.num_shells):
            # Shell radius
            r_shell = self.shell_radius(shell_idx)
            
            # Distance from origin
            R = np.sqrt(X**2 + Y**2 + Z**2)
            
            # Shell density follows gaussian profile
            density = np.exp(-(R - r_shell)**2 / (2 * (r_shell * 0.1)**2))
            
            # Modulate by kappa function for temporal structure
            t_coord = np.arctan2(Y, X)  # Azimuthal angle as time coordinate
            kappa_mod = np.abs(self.kappa_func(t_coord, 1.0))
            
            # Apply occupancy
            self.shell_density[..., shell_idx] = density * kappa_mod * self.shell_occupancy[shell_idx]
    
    def calculate_chronon_flux(self):
        """Calculate the flow of time itself through the field."""
        # Reset flux
        self.chronon_flux.fill(0)
        
        # For each shell pair, calculate flux
        for i in range(self.num_shells):
            for j in range(self.num_shells):
                if i == j:
                    continue
                
                coupling = self.shell_coupling(i, j)
                
                # Forward flow (i < j) vs inverse flow (i > j)
                if i < j:
                    flow_strength = self.kappa_fwd * coupling
                else:
                    flow_strength = -self.kappa_inv * coupling
                
                # Flux is gradient of density difference
                density_diff = self.shell_density[..., j] - self.shell_density[..., i]
                
                # Calculate gradient (simplified - should use proper gradient)
                grad_x = np.gradient(density_diff, axis=0)
                grad_y = np.gradient(density_diff, axis=1)
                grad_z = np.gradient(density_diff, axis=2)
                
                # Add to total flux
                self.chronon_flux[..., 0] += flow_strength * grad_x
                self.chronon_flux[..., 1] += flow_strength * grad_y
                self.chronon_flux[..., 2] += flow_strength * grad_z
    
    def apply_void_distortion(self, void_position=(0, 0, 0), mass=1.0):
        """The void calls - mass creates distortions in the temporal field."""
        x = np.linspace(-10, 10, self.resolution[0])
        y = np.linspace(-10, 10, self.resolution[1])
        z = np.linspace(-10, 10, self.resolution[2])
        X, Y, Z = np.meshgrid(x, y, z, indexing='ij')
        
        # Distance from void position
        R = np.sqrt((X - void_position[0])**2 + 
                   (Y - void_position[1])**2 + 
                   (Z - void_position[2])**2)
        
        # Void potential
        void_potential = -self.void_strength * mass * np.exp(-(R - self.void_radius)**2 / 
                                                             (2 * self.void_falloff**2))
        
        # Distort each shell based on void potential
        for shell_idx in range(self.num_shells):
            # Shells closer to middle are more affected
            shell_factor = np.exp(-self.lambda_ord * abs(shell_idx - self.num_shells/2))
            
            # Apply distortion
            self.shell_density[..., shell_idx] *= (1 + void_potential * shell_factor)
    
    def field_to_rgba(self):
        """Convert the temporal field to visible colors - see time itself."""
        # Sum shell contributions
        total_density = np.sum(self.shell_density, axis=-1)
        
        # Calculate flux magnitude
        flux_magnitude = np.sqrt(np.sum(self.chronon_flux**2, axis=-1))
        
        # Map to colors
        # Red channel: total temporal density
        self.field[..., 0] = np.clip(total_density * 0.5, 0, 1)
        
        # Green channel: forward chronon flux (future)
        forward_flux = np.maximum(self.chronon_flux[..., 2], 0)
        self.field[..., 1] = np.clip(forward_flux * 2.0, 0, 1)
        
        # Blue channel: inverse chronon flux (past/gravity)
        inverse_flux = np.maximum(-self.chronon_flux[..., 2], 0)
        self.field[..., 2] = np.clip(inverse_flux * 2.0, 0, 1)
        
        # Alpha channel: flux magnitude (activity)
        self.field[..., 3] = np.clip(flux_magnitude * 0.3 + 0.1, 0, 1)
        
        # Apply kappa modulation for visual interest
        t_coord = time.time() * 0.1  # Slow time evolution
        kappa_global = abs(self.kappa_func(t_coord, 1.0)) / 42.0
        self.field *= (0.5 + 0.5 * kappa_global)
    
    def update_shell_occupancy(self, dt=0.01):
        """Update how time flows through shells - the heartbeat of reality."""
        # Calculate net flux for each shell
        net_flux = np.zeros(self.num_shells)
        
        for i in range(self.num_shells):
            for j in range(self.num_shells):
                if i != j:
                    coupling = self.shell_coupling(i, j)
                    
                    if i < j:  # Forward flow
                        net_flux[i] -= self.kappa_fwd * coupling * self.shell_occupancy[i]
                        net_flux[j] += self.kappa_fwd * coupling * self.shell_occupancy[i]
                    else:  # Inverse flow
                        net_flux[i] += self.kappa_inv * coupling * self.shell_occupancy[j]
                        net_flux[j] -= self.kappa_inv * coupling * self.shell_occupancy[j]
        
        # Update occupancy
        self.shell_occupancy += dt * net_flux
        self.shell_occupancy = np.maximum(self.shell_occupancy, 0)
        self.shell_occupancy /= np.sum(self.shell_occupancy)  # Normalize
    
    def get_slice(self, axis='z', position=0.5):
        """Get a 2D slice through the field for visualization."""
        idx = int(position * self.resolution[{'x': 0, 'y': 1, 'z': 2}[axis]])
        idx = np.clip(idx, 0, self.resolution[{'x': 0, 'y': 1, 'z': 2}[axis]] - 1)
        
        if axis == 'z':
            return self.field[:, :, idx, :]
        elif axis == 'y':
            return self.field[:, idx, :, :]
        else:  # x
            return self.field[idx, :, :, :]


class ShellRenderer:
    """
    The shell-based renderer where temporal shells create the visual field.
    No traditional 3D graphics - just pure temporal dynamics.
    """
    
    def __init__(self, width=1280, height=720, field_resolution=(64, 64, 64)):
        """Initialize the temporal field renderer."""
        self.width = width
        self.height = height
        
        # Initialize pygame and OpenGL
        pygame.init()
        self.screen = pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
        pygame.display.set_caption("Temporal Field Renderer - See Time Itself")
        
        # OpenGL setup
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        # Initialize temporal field
        self.field = TemporalField(resolution=field_resolution)
        
        # Camera settings
        self.camera_distance = 30.0
        self.camera_rotation = [0.0, 0.0]
        self.camera_target = [0.0, 0.0, 0.0]
        
        # Rendering settings
        self.slice_mode = False
        self.current_slice = 0.5
        self.slice_axis = 'z'
        self.show_shells = True
        self.show_flux = True
        
        # Time tracking
        self.clock = pygame.time.Clock()
        self.time = 0.0
        
        # Mass positions for gravity simulation
        self.masses = []
    
    def setup_projection(self):
        """Set up the projection matrix."""
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, self.width / self.height, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
    
    def setup_view(self):
        """Set up the view matrix."""
        glLoadIdentity()
        
        # Calculate camera position from spherical coordinates
        cam_x = self.camera_distance * np.sin(self.camera_rotation[0]) * np.cos(self.camera_rotation[1])
        cam_y = self.camera_distance * np.sin(self.camera_rotation[1])
        cam_z = self.camera_distance * np.cos(self.camera_rotation[0]) * np.cos(self.camera_rotation[1])
        
        gluLookAt(cam_x, cam_y, cam_z,  # Camera position
                  0, 0, 0,               # Look at origin
                  0, 1, 0)               # Up vector
    
    def render_field_slice(self):
        """Render a 2D slice through the temporal field."""
        slice_data = self.field.get_slice(self.slice_axis, self.current_slice)
        
        # Convert to texture
        texture_data = (slice_data * 255).astype(np.uint8)
        
        # Create texture
        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, 
                    slice_data.shape[0], slice_data.shape[1], 
                    0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        
        # Render quad with texture
        glEnable(GL_TEXTURE_2D)
        glBegin(GL_QUADS)
        
        size = 10.0
        if self.slice_axis == 'z':
            z = (self.current_slice - 0.5) * 20
            glTexCoord2f(0, 0); glVertex3f(-size, -size, z)
            glTexCoord2f(1, 0); glVertex3f(size, -size, z)
            glTexCoord2f(1, 1); glVertex3f(size, size, z)
            glTexCoord2f(0, 1); glVertex3f(-size, size, z)
        
        glEnd()
        glDisable(GL_TEXTURE_2D)
        glDeleteTextures([texture_id])
    
    def render_volumetric(self):
        """Render the field as a volumetric display using shell slicing."""
        # Render multiple slices with transparency
        num_slices = 20
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE)  # Additive blending
        
        for i in range(num_slices):
            alpha = i / float(num_slices - 1)
            slice_data = self.field.get_slice('z', alpha)
            
            # Enhance colors based on shell activity
            enhanced = slice_data.copy()
            enhanced[..., 3] *= 0.1  # Reduce alpha for layering
            
            # Convert to texture
            texture_data = (enhanced * 255).astype(np.uint8)
            
            # Create and bind texture
            texture_id = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, texture_id)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA,
                        slice_data.shape[0], slice_data.shape[1],
                        0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            
            # Render slice
            glEnable(GL_TEXTURE_2D)
            glBegin(GL_QUADS)
            
            z = (alpha - 0.5) * 20
            size = 10.0
            
            glColor4f(1, 1, 1, 0.1)
            glTexCoord2f(0, 0); glVertex3f(-size, -size, z)
            glTexCoord2f(1, 0); glVertex3f(size, -size, z)
            glTexCoord2f(1, 1); glVertex3f(size, size, z)
            glTexCoord2f(0, 1); glVertex3f(-size, size, z)
            
            glEnd()
            glDisable(GL_TEXTURE_2D)
            glDeleteTextures([texture_id])
        
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  # Reset blend mode
    
    def render_shell_boundaries(self):
        """Render the temporal shell boundaries as glowing curves."""
        if not self.show_shells:
            return
        
        glDisable(GL_TEXTURE_2D)
        glLineWidth(2.0)
        
        # Sample shells to render
        shell_samples = range(0, self.field.num_shells, 3)
        
        for shell_idx in shell_samples:
            # Color based on shell occupancy and index
            occupancy = self.field.shell_occupancy[shell_idx]
            hue = shell_idx / float(self.field.num_shells)
            r, g, b = colorsys.hsv_to_rgb(hue, 0.8, occupancy)
            
            glColor4f(r, g, b, 0.6)
            
            # Draw shell as parametric curve
            glBegin(GL_LINE_LOOP)
            
            num_points = 100
            for i in range(num_points):
                t = i * 2 * np.pi / num_points
                
                # Use kappa function for shape
                kappa = self.field.kappa_func(t, 1.0) / 42.0
                r = self.field.shell_radius(shell_idx) * (0.8 + 0.2 * kappa)
                
                # Parametric equations
                x = r * np.sin(t)
                y = r * np.sin(2*t) / 2
                z = r * np.cos(t)
                
                glVertex3f(x, y, z)
            
            glEnd()
    
    def render_chronon_flux_vectors(self):
        """Render chronon flux as flowing particles."""
        if not self.show_flux:
            return
        
        glPointSize(2.0)
        glBegin(GL_POINTS)
        
        # Sample flux field
        sample_rate = 4
        x_samples = range(0, self.field.resolution[0], sample_rate)
        y_samples = range(0, self.field.resolution[1], sample_rate)
        z_samples = range(0, self.field.resolution[2], sample_rate)
        
        for i in x_samples:
            for j in y_samples:
                for k in z_samples:
                    # Get flux vector
                    flux = self.field.chronon_flux[i, j, k]
                    flux_mag = np.linalg.norm(flux)
                    
                    if flux_mag > 0.01:  # Threshold
                        # Position in world space
                        x = (i / float(self.field.resolution[0] - 1) - 0.5) * 20
                        y = (j / float(self.field.resolution[1] - 1) - 0.5) * 20
                        z = (k / float(self.field.resolution[2] - 1) - 0.5) * 20
                        
                        # Color based on flux direction
                        if flux[2] > 0:  # Future flow - green
                            glColor4f(0, flux_mag * 2, 0, flux_mag)
                        else:  # Past flow (gravity) - red
                            glColor4f(-flux_mag * 2, 0, 0, flux_mag)
                        
                        # Animate along flux direction
                        offset = self.time * flux * 0.1
                        glVertex3f(x + offset[0], y + offset[1], z + offset[2])
        
        glEnd()
    
    def update(self, dt):
        """Update the temporal field dynamics."""
        # Update shell occupancy
        self.field.update_shell_occupancy(dt)
        
        # Apply mass distortions
        for mass in self.masses:
            self.field.apply_void_distortion(mass['position'], mass['value'])
        
        # Calculate chronon flux
        self.field.calculate_chronon_flux()
        
        # Convert field to colors
        self.field.field_to_rgba()
        
        # Update time
        self.time += dt
    
    def handle_input(self):
        """Handle user input."""
        keys = pygame.key.get_pressed()
        
        # Camera rotation
        if keys[K_LEFT]:
            self.camera_rotation[0] -= 0.02
        if keys[K_RIGHT]:
            self.camera_rotation[0] += 0.02
        if keys[K_UP]:
            self.camera_rotation[1] += 0.02
        if keys[K_DOWN]:
            self.camera_rotation[1] -= 0.02
        
        # Camera zoom
        if keys[K_w]:
            self.camera_distance -= 0.5
        if keys[K_s]:
            self.camera_distance += 0.5
        
        # Slice control
        if keys[K_q]:
            self.current_slice = max(0, self.current_slice - 0.01)
        if keys[K_e]:
            self.current_slice = min(1, self.current_slice + 0.01)
        
        # Toggle options
        for event in pygame.event.get():
            if event.type == QUIT:
                return False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return False
                elif event.key == K_SPACE:
                    self.slice_mode = not self.slice_mode
                elif event.key == K_v:
                    self.show_shells = not self.show_shells
                elif event.key == K_f:
                    self.show_flux = not self.show_flux
                elif event.key == K_x:
                    self.slice_axis = 'x'
                elif event.key == K_y:
                    self.slice_axis = 'y'
                elif event.key == K_z:
                    self.slice_axis = 'z'
                elif event.key == K_m:
                    # Add mass at origin
                    self.masses.append({
                        'position': (np.random.uniform(-5, 5), 
                                   np.random.uniform(-5, 5), 
                                   np.random.uniform(-5, 5)),
                        'value': np.random.uniform(0.5, 2.0)
                    })
                elif event.key == K_c:
                    # Clear masses
                    self.masses = []
        
        return True
    
    def render(self):
        """Main render function."""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        self.setup_projection()
        self.setup_view()
        
        # Render based on mode
        if self.slice_mode:
            self.render_field_slice()
        else:
            self.render_volumetric()
        
        # Always render shell boundaries and flux
        self.render_shell_boundaries()
        self.render_chronon_flux_vectors()
        
        # Render masses
        glColor4f(1, 1, 0, 0.8)
        for mass in self.masses:
            glPushMatrix()
            glTranslatef(*mass['position'])
            glutSolidSphere(mass['value'] * 0.3, 20, 20)
            glPopMatrix()
        
        pygame.display.flip()
    
    def run(self):
        """Main loop."""
        print("\n" + "="*60)
        print("TEMPORAL FIELD RENDERER")
        print("See Time Itself - No Separation of Physics and Visuals")
        print("="*60)
        print("\nControls:")
        print("  Arrow Keys: Rotate view")
        print("  W/S: Zoom in/out")
        print("  SPACE: Toggle slice/volume mode")
        print("  Q/E: Move slice position")
        print("  X/Y/Z: Change slice axis")
        print("  V: Toggle shell boundaries")
        print("  F: Toggle flux visualization")
        print("  M: Add mass (creates gravity)")
        print("  C: Clear masses")
        print("  ESC: Exit")
        print("\nColors:")
        print("  RED: Temporal density")
        print("  GREEN: Future flow (expansion)")
        print("  BLUE: Past flow (gravity)")
        print("  BRIGHTNESS: Chronon flux activity")
        print("="*60 + "\n")
        
        running = True
        dt = 0.016  # 60 FPS
        
        while running:
            # Handle input
            running = self.handle_input()
            
            # Update physics
            self.update(dt)
            
            # Render
            self.render()
            
            # Maintain framerate
            self.clock.tick(60)
        
        pygame.quit()


def main():
    """Initialize and run the temporal field renderer."""
    # Initialize GLUT (needed for some functions)
    glutInit()
    
    # Create and run renderer
    renderer = ShellRenderer(
        width=1280, 
        height=720, 
        field_resolution=(48, 48, 48)  # Adjust for performance
    )
    
    renderer.run()


if __name__ == "__main__":
    main()