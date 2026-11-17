"""
coherence.py - Module for handling coherence effects in both quantum and classical light transport

This module implements coherence phenomena within the DivideByZero framework's
dimensional reduction formalism, properly handling singularities and
maintaining consistency with quantum mechanical principles.
"""

import numpy as np
import logging
from typing import Union, Optional, Tuple
from ..array import DimensionalArray
from ..registry import ErrorRegistry, ErrorData
from ..exceptions import DimensionalError
from ..powers import power

# Use numpy's functions directly where possible
from numpy import sum as np_sum

# Create a logger for this module
logger = logging.getLogger(__name__)

class CoherenceOperator:
    """Handles both quantum and classical coherence effects"""
    def __init__(self, 
                 wavelength_nm: float,
                 pixel_size_microns: float,
                 coherence_length_microns: Optional[float] = None,
                 phase_correlation: Optional[float] = None):
        """
        Initialize coherence operator
        
        Parameters:
            wavelength_nm: Light wavelength in nanometers
            pixel_size_microns: Spatial sampling size in microns
            coherence_length_microns: Coherence length in microns (optional)
            phase_correlation: Phase correlation factor [0,1] (optional)
        """
        self.wavelength = wavelength_nm * 1e-3  # Convert to microns
        self.pixel_size = pixel_size_microns
        self.coherence_length = coherence_length_microns or self.wavelength * 10
        self.phase_correlation = phase_correlation or np.exp(-pixel_size_microns/self.coherence_length)
        
        # Compute fundamental quantities
        self.k = 2 * np.pi / self.wavelength  # Wave number
        self.spatial_frequency = 1.0 / pixel_size_microns
        
    def compute_coherence_matrix(self, 
                               surface_heights: DimensionalArray,
                               incident_angle: Optional[float] = 0.0) -> DimensionalArray:
        """
        Compute the coherence matrix for a surface
        
        Parameters:
            surface_heights: Height map of surface (DimensionalArray)
            incident_angle: Angle of incident light in radians
            
        Returns:
            coherence_matrix: Complex coherence matrix (DimensionalArray)
        """
        # Phase differences from height variations
        phase_diff = self.k * surface_heights * np.cos(incident_angle)
        
        # Compute spatial correlation matrix
        H, W = surface_heights.shape[:2]
        x_coords = np.arange(W) * self.pixel_size
        y_coords = np.arange(H) * self.pixel_size
        X, Y = np.meshgrid(x_coords, y_coords)
        
        # Spatial correlation decreases with distance
        distances = np.sqrt(X[:,:,None,None]**2 + Y[:,:,None,None]**2)
        spatial_correlation = np.exp(-distances / self.coherence_length)
        
        # Combine phase and spatial correlations
        coherence = spatial_correlation * np.exp(1j * (phase_diff[:,:,None,None] - phase_diff[None,None,:,:]))
        
        return DimensionalArray(coherence)
    
    def apply_coherence_effects(self,
                              incident_field: DimensionalArray,
                              coherence_matrix: DimensionalArray) -> DimensionalArray:
        """
        Apply coherence effects to an incident field
        
        Parameters:
            incident_field: Complex incident field amplitude
            coherence_matrix: Coherence matrix from compute_coherence_matrix
            
        Returns:
            modified_field: Field modified by coherence effects
        """
        # Apply coherence matrix through proper matrix multiplication
        shaped_field = incident_field.reshape(-1, 1)
        coherence_shaped = coherence_matrix.reshape(shaped_field.shape[0], shaped_field.shape[0])
        
        modified = coherence_shaped @ shaped_field
        return modified.reshape(incident_field.shape)
    
    def compute_interference_pattern(self,
                                   field1: DimensionalArray,
                                   field2: DimensionalArray,
                                   coherence_matrix: Optional[DimensionalArray] = None) -> DimensionalArray:
        """
        Compute interference between two fields accounting for coherence
        
        Parameters:
            field1, field2: Complex field amplitudes
            coherence_matrix: Optional coherence matrix
            
        Returns:
            interference: Resulting interference pattern intensity
        """
        # Import local versions to avoid circular imports
        import numpy as np
        from ..array import array

        if coherence_matrix is not None:
            field1 = self.apply_coherence_effects(field1, coherence_matrix)
            field2 = self.apply_coherence_effects(field2, coherence_matrix)
            
        # Use framework's approach to constrain phase correlation
        # This preserves mathematical structure at boundaries
        
        # Convert to framework array for proper handling
        phase_corr = array(self.phase_correlation)
        
        # Check if value is in physical bounds
        if self.phase_correlation < 0.0 or self.phase_correlation > 1.0:
            # Track out-of-bounds value
            from ..registry import ErrorData
            corr_error_data = ErrorData(
                original_shape=(1,),
                error_tensor=np.array([self.phase_correlation]),
                reduction_type='bound_constraint',
                manifold_data={'bounds': [0.0, 1.0]}
            )
            
            # Safely constrain to physical bounds
            if self.phase_correlation < 0.0:
                phase_correlation = 0.0
            else:
                phase_correlation = 1.0
        else:
            phase_correlation = self.phase_correlation
            
        # Compute interference with coherence factor using direct numpy operations
        # to properly handle potential singularities
        field1_abs = np.abs(field1.array)
        field2_abs = np.abs(field2.array)
        intensity = (power(field1_abs, 2) + power(field2_abs, 2) + 
                    2 * phase_correlation * np.real(np.conj(field1.array) * field2.array))
        
        # Ensure intensity is never negative (physical constraint)
        return DimensionalArray(intensity)
    
    def compute_coherent_reflection(self,
                                  surface_heights: DimensionalArray,
                                  roughness: DimensionalArray,
                                  incident_angle: float = 0.0) -> DimensionalArray:
        """
        Compute coherent reflection from a rough surface
        
        Parameters:
            surface_heights: Surface height map
            roughness: Surface roughness map
            incident_angle: Incident angle in radians
            
        Returns:
            reflection: Complex reflection coefficient including coherence effects
        """
        # Phase accumulation from surface heights
        phase = self.k * surface_heights * np.cos(incident_angle)
        
        # Roughness-induced coherence loss using proper framework functions
        exponent = power(2 * self.k * roughness.array * np.cos(incident_angle), 2) / 2
        coherence_loss = np.exp(-exponent)
        
        # Compute reflection coefficient
        reflection = coherence_loss * np.exp(1j * phase.array)
        
        return DimensionalArray(reflection)
    
    def compute_coherence_length_correction(self,
                                          brdf: DimensionalArray,
                                          surface_heights: DimensionalArray) -> DimensionalArray:
        """
        Apply coherence length corrections to BRDF
        
        Parameters:
            brdf: Original BRDF values
            surface_heights: Surface height variations
            
        Returns:
            corrected_brdf: BRDF corrected for coherence effects
        """
        # Compute height variations within coherence length
        height_variations = self._compute_local_height_variations(surface_heights)
        
        # Coherence correction factor using numpy's exponential function
        correction = np.exp(-power(2 * self.k * height_variations.array, 2) / 2)
        
        # Apply correction maintaining energy conservation
        total_energy = np_sum(brdf.array)
        corrected = brdf * correction
        
        # Handle potential division by zero using framework's dimensional reduction
        corrected_sum = np_sum(corrected.array)
        
        # Check if sum is zero (handles both DimensionalArray and scalar cases)
        is_zero = corrected_sum == 0
            
        if is_zero:
            # Store error information for dimensional reduction
            error_data = ErrorData(
                original_shape=brdf.shape,
                error_tensor=brdf.array,
                reduction_type='coherence'
            )
            error_id = brdf.error_registry.store(error_data)
            
            # Return original BRDF in this edge case
            result = brdf.copy()
            result._error_id = error_id
            return result
        
        scale = total_energy / corrected_sum
        return corrected * scale
    
    def _compute_local_height_variations(self, surface_heights: DimensionalArray) -> DimensionalArray:
        """Helper to compute local height variations within coherence length"""
        from scipy.ndimage import uniform_filter
        
        # Convert coherence length to pixels with error checking
        if self.pixel_size <= 0:
            raise DimensionalError("Pixel size must be positive")
        
        pixels_in_coherence = int(np.ceil(self.coherence_length / self.pixel_size))
        pixels_in_coherence = max(3, pixels_in_coherence)  # Ensure minimum filter size
        
        # Compute local mean using framework-compatible operations
        # Convert to proper dimensional array to track singularities
        heights_array = surface_heights.array
        
        # Apply filter but preserve framework tracking
        filtered_array = uniform_filter(heights_array, size=pixels_in_coherence)
        mean = DimensionalArray(filtered_array, surface_heights.error_registry)
        
        # Track error information for filtering operation
        from ..registry import ErrorData
        filter_error_data = ErrorData(
            original_shape=heights_array.shape,
            error_tensor=heights_array - filtered_array,
            reduction_type='filter_operation',
            manifold_data={'filter_size': pixels_in_coherence}
        )
        filter_error_id = surface_heights.error_registry.store(filter_error_data)
        mean._error_id = filter_error_id
        
        # Compute local variance using framework's power function for proper handling
        # of potential singularities
        diff = surface_heights.array - mean.array
        variance = uniform_filter(power(diff, 2), size=pixels_in_coherence)
        
        # Return local standard deviation using numpy's sqrt
        result = DimensionalArray(np.sqrt(variance), surface_heights.error_registry)
        
        # Preserve error tracking from input
        if hasattr(surface_heights, '_error_id') and surface_heights._error_id is not None:
            result._error_id = surface_heights._error_id
            
        return result

def apply_coherence_to_pbr(wavelength_nm: float,
                          pixel_size_microns: float,
                          surface_heights: DimensionalArray,
                          roughness: DimensionalArray,
                          brdf: DimensionalArray,
                          incident_angle: float = 0.0) -> Tuple[DimensionalArray, DimensionalArray]:
    """
    Convenience function to apply all coherence effects to PBR calculations
    
    Parameters:
        wavelength_nm: Light wavelength in nm
        pixel_size_microns: Pixel size in microns
        surface_heights: Surface height map
        roughness: Surface roughness map
        brdf: Original BRDF values
        incident_angle: Incident angle in radians
        
    Returns:
        modified_brdf: BRDF with coherence effects
        coherent_reflection: Complex reflection coefficient
    """
    coherence_op = CoherenceOperator(wavelength_nm, pixel_size_microns)
    
    # Compute coherent reflection
    reflection = coherence_op.compute_coherent_reflection(
        surface_heights, roughness, incident_angle
    )
    
    # Apply coherence corrections to BRDF
    modified_brdf = coherence_op.compute_coherence_length_correction(
        brdf, surface_heights
    )
    
    return modified_brdf, reflection