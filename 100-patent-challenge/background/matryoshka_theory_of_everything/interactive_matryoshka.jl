"""
Interactive Matryoshka-Chronon Renderer with GUI

A real-time interactive version of the Matryoshka-Chronon renderer
that allows tweaking parameters and seeing results immediately.
"""

using LinearAlgebra
using Random
using Printf
using Plots
using Interact
using Blink
using Statistics
using Images
using Logging
using Dates
# Use GR backend for speed
gr()

"""
    MatryoshkaRenderer

A light transport renderer based on the Matryoshka-Chronon framework with interactive controls.
"""
mutable struct MatryoshkaRenderer
    # Core shell system parameters
    shell_count::Int
    alpha::Float64
    kappa_ratio::Float64
    coupling_decay::Float64
    
    # Boundary parameters (critical for photon propagation)
    boundary_coupling::Float64
    boundary_width::Float64
    
    # "Call of the Void" potential parameters
    v_ratio::Float64
    sigma_ratio::Float64
    
    # Spectral parameters
    spectral_samples::Int
    min_wavelength::Float64
    max_wavelength::Float64
    
    # Rendering parameters
    step_size::Float64
    max_simulation_steps::Int
    
    # Scene parameters
    scene::Dict{Symbol, Any}
    state::Dict{Symbol, Any}
    
    # Random number generator
    rng::MersenneTwister
    
    # Internal state tracking
    initialized::Bool
    
    # Constructor with default values
    function MatryoshkaRenderer(config::Dict{Symbol, Any})
        # Set defaults for optional parameters
        shell_count = get(config, :shell_count, 32)
        alpha = get(config, :alpha, 0.1)
        kappa_ratio = get(config, :kappa_ratio, 0.95)
        coupling_decay = get(config, :coupling_decay, 0.3)
        boundary_coupling = get(config, :boundary_coupling, 0.9)
        boundary_width = get(config, :boundary_width, 0.02)
        v_ratio = get(config, :v_ratio, 1.2)
        sigma_ratio = get(config, :sigma_ratio, 0.7)
        spectral_samples = get(config, :spectral_samples, 8)
        min_wavelength = get(config, :min_wavelength, 380.0)
        max_wavelength = get(config, :max_wavelength, 780.0)
        step_size = get(config, :step_size, 0.1)
        max_simulation_steps = get(config, :max_steps, 50)
        
        # Initialize random number generator
        rng = MersenneTwister(get(config, :seed, 42))
        
        # Create empty scene and state
        scene = Dict{Symbol, Any}()
        state = Dict{Symbol, Any}()
        
        new(
            shell_count,
            alpha,
            kappa_ratio,
            coupling_decay,
            boundary_coupling,
            boundary_width,
            v_ratio,
            sigma_ratio,
            spectral_samples,
            min_wavelength,
            max_wavelength,
            step_size,
            max_simulation_steps,
            scene,
            state,
            rng,
            false  # initialized
        )
    end
end

"""
    update_parameters!(renderer::MatryoshkaRenderer, params::Dict{Symbol, Any})

Update renderer parameters and reinitialize if necessary.
"""
function update_parameters!(renderer::MatryoshkaRenderer, params::Dict{Symbol, Any})
    # Track if core parameters that require reinitialization changed
    core_params_changed = false
    
    # Update shell system parameters
    if haskey(params, :shell_count) && params[:shell_count] != renderer.shell_count
        renderer.shell_count = params[:shell_count]
        core_params_changed = true
    end
    
    if haskey(params, :alpha) && params[:alpha] != renderer.alpha
        renderer.alpha = params[:alpha]
        core_params_changed = true
    end
    
    if haskey(params, :kappa_ratio)
        renderer.kappa_ratio = params[:kappa_ratio]
    end
    
    if haskey(params, :coupling_decay)
        renderer.coupling_decay = params[:coupling_decay]
    end
    
    # Update boundary parameters
    if haskey(params, :boundary_coupling)
        renderer.boundary_coupling = params[:boundary_coupling]
    end
    
    if haskey(params, :boundary_width)
        renderer.boundary_width = params[:boundary_width]
    end
    
    # Update "Call of the Void" parameters
    if haskey(params, :v_ratio)
        renderer.v_ratio = params[:v_ratio]
    end
    
    if haskey(params, :sigma_ratio)
        renderer.sigma_ratio = params[:sigma_ratio]
    end
    
    # Update spectral parameters
    if haskey(params, :spectral_samples) && params[:spectral_samples] != renderer.spectral_samples
        renderer.spectral_samples = params[:spectral_samples]
        core_params_changed = true
    end
    
    if haskey(params, :min_wavelength)
        renderer.min_wavelength = params[:min_wavelength]
    end
    
    if haskey(params, :max_wavelength)
        renderer.max_wavelength = params[:max_wavelength]
    end
    
    # Update rendering parameters
    if haskey(params, :step_size)
        renderer.step_size = params[:step_size]
    end
    
    if haskey(params, :max_simulation_steps)
        renderer.max_simulation_steps = params[:max_simulation_steps]
    end
    
    # If core parameters changed, mark as uninitialized
    if core_params_changed
        renderer.initialized = false
    end
    
    return core_params_changed
end

"""
    initialize_shell_system(renderer::MatryoshkaRenderer)

Initialize the shell system with the current scene parameters.
"""
function initialize_shell_system(renderer::MatryoshkaRenderer)
    # Check if scene is defined
    if !haskey(renderer.scene, :geometry) || !haskey(renderer.scene, :materials) || !haskey(renderer.scene, :resolution)
        error("Scene geometry, materials, or resolution not defined")
    end
    
    # Extract scene components
    geometry = renderer.scene[:geometry]
    materials = renderer.scene[:materials]
    resolution = renderer.scene[:resolution]
    
    height, width = resolution
    
    # Initialize shell radii with exponential scaling
    shell_radii = exp.(renderer.alpha .* (0:renderer.shell_count-1))
    
    # Define shell boundaries (where photons propagate)
    boundary_count = renderer.shell_count - 1
    boundary_radii = zeros(boundary_count)
    for i in 1:boundary_count
        # Boundary lies between adjacent shells
        boundary_radii[i] = (shell_radii[i] + shell_radii[i+1]) / 2
    end
    
    # Initialize shell state variables
    # 1. Shell densities (for particles/matter)
    shell_densities = ones(renderer.shell_count, height, width)
    
    # 2. Boundary field (for photons) - complex valued for phase information
    # Each spectral component tracked separately
    boundary_field = 0.01 .* randn(renderer.rng, ComplexF64, boundary_count, height, width, renderer.spectral_samples)
    
    # 3. Phase information
    shell_phases = 2π .* rand(renderer.rng, Float64, renderer.shell_count, height, width)
    boundary_phases = 2π .* rand(renderer.rng, Float64, boundary_count, height, width)
    
    # Initialize coupling matrices
    # 1. Shell-to-shell coupling (for particles/matter)
    shell_coupling = zeros(renderer.shell_count, renderer.shell_count)
    for i in 1:renderer.shell_count
        for j in 1:renderer.shell_count
            if i != j
                dist = abs(i - j)
                shell_coupling[i, j] = exp(-renderer.coupling_decay * dist) / dist
            end
        end
    end
    
    # 2. Boundary-to-boundary coupling (for photons)
    boundary_coupling = zeros(boundary_count, boundary_count)
    for i in 1:boundary_count
        for j in 1:boundary_count
            if i != j
                dist = abs(i - j)
                boundary_coupling[i, j] = renderer.boundary_coupling * exp(-dist) / sqrt(dist)
            end
        end
    end
    
    # 3. Shell-to-boundary coupling (for emission/absorption)
    shell_boundary_coupling = zeros(renderer.shell_count, boundary_count)
    for i in 1:renderer.shell_count
        for j in 1:boundary_count
            # Strong coupling for adjacent shell-boundary pairs
            if i == j || i == j + 1
                shell_boundary_coupling[i, j] = 0.8
            else
                # Weak coupling for distant pairs
                shell_boundary_coupling[i, j] = 0.1 * exp(-abs(i - j - 0.5))
            end
        end
    end
    
    # Initialize spectral wavelengths
    wavelengths = range(renderer.min_wavelength, renderer.max_wavelength, length=renderer.spectral_samples)
    
    # Project geometry to shell system
    shell_geometry = project_geometry_to_shells(renderer, geometry, shell_radii)
    
    # Initialize light sources
    boundary_field = initialize_light_sources(renderer, boundary_field, geometry, materials, shell_radii, boundary_radii)
    
    # Create state dictionary
    state = Dict(
        :shell_radii => shell_radii,
        :boundary_radii => boundary_radii,
        :shell_densities => shell_densities,
        :boundary_field => boundary_field,
        :shell_phases => shell_phases,
        :boundary_phases => boundary_phases,
        :shell_coupling => shell_coupling,
        :boundary_coupling => boundary_coupling,
        :shell_boundary_coupling => shell_boundary_coupling,
        :shell_geometry => shell_geometry,
        :materials => materials,
        :wavelengths => wavelengths
    )
    
    # Store state
    renderer.state = state
    renderer.initialized = true
    
    return state
end

"""
    project_geometry_to_shells(renderer::MatryoshkaRenderer, geometry::Dict, shell_radii::Vector{Float64})

Project scene geometry onto the shell system.
"""
function project_geometry_to_shells(renderer::MatryoshkaRenderer, geometry::Dict, shell_radii::Vector{Float64})
    # Create occupancy field for each shell
    if haskey(geometry, :spheres)
        spheres = geometry[:spheres]
        n_spheres = length(spheres[:centers])
        
        # For each shell, compute occupancy based on spheres
        shell_occupancy = zeros(renderer.shell_count, n_spheres)
        
        # Compute occupancy for all shell-sphere pairs
        for s_idx in 1:renderer.shell_count
            for sp_idx in 1:n_spheres
                sphere_center = spheres[:centers][sp_idx]
                sphere_radius = spheres[:radii][sp_idx]
                shell_radius = shell_radii[s_idx]
                
                # Distance from shell to sphere center
                center_distance = norm(sphere_center)
                
                # Shell-sphere intersection occurs when shell radius is within
                # sphere's range
                intersection = max(0.0, 1.0 - abs(shell_radius - center_distance) / sphere_radius)
                
                shell_occupancy[s_idx, sp_idx] = intersection
            end
        end
        
        # Material indices for each sphere
        material_indices = spheres[:material_indices]
        
        return Dict(
            :occupancy => shell_occupancy,
            :material_indices => material_indices,
            :sphere_centers => spheres[:centers],
            :sphere_radii => spheres[:radii]
        )
    else
        # Default empty geometry
        return Dict(
            :occupancy => zeros(renderer.shell_count, 1),
            :material_indices => [0]
        )
    end
end

"""
    initialize_light_sources(renderer::MatryoshkaRenderer, boundary_field::Array{ComplexF64}, geometry::Dict, materials::Dict, shell_radii::Vector{Float64}, boundary_radii::Vector{Float64})

Initialize light sources at appropriate shell boundaries.
"""
function initialize_light_sources(renderer::MatryoshkaRenderer, boundary_field::Array{ComplexF64}, geometry::Dict, materials::Dict, shell_radii::Vector{Float64}, boundary_radii::Vector{Float64})
    if !haskey(geometry, :emitters)
        return boundary_field
    end
    
    emitters = geometry[:emitters]
    n_emitters = length(emitters[:positions])
    
    # Process each emitter
    for i in 1:n_emitters
        # Get emitter properties
        position = emitters[:positions][i]
        intensity = emitters[:intensities][i]
        spectrum = emitters[:spectra][i]
        
        # Find distance from origin
        distance = norm(position)
        
        # Find closest boundary
        _, boundary_idx = findmin(abs.(boundary_radii .- distance))
        
        # Normalize position to get direction
        direction = position / max(distance, 1e-10)
        
        # Create angular distribution on boundary
        h, w = size(boundary_field)[2:3]
        y_vals = range(-1, 1, length=h)
        x_vals = range(-1, 1, length=w)
        
        # Create grids
        y_grid = [y for y in y_vals, x in x_vals]
        x_grid = [x for y in y_vals, x in x_vals]
        
        # Convert to spherical coordinates
        grid_r = sqrt.(x_grid.^2 .+ y_grid.^2)
        grid_phi = atan.(y_grid, x_grid)
        
        # Map emitter direction to grid
        emitter_phi = atan(direction[2], direction[1])
        emitter_theta = length(direction) > 2 ? acos(direction[3]) : 0.0
        
        # Create angular mask (directional emission)
        # Stronger emission in emitter's forward direction
        angular_mask = exp.(-5.0 .* (1.0 .- cos.(grid_phi .- emitter_phi)))
        
        # Apply mask only where grid radius is valid
        valid_mask = (grid_r .<= 1.0)
        emission_mask = angular_mask .* valid_mask
        
        # Add emission to boundary field
        for s in 1:renderer.spectral_samples
            # Scale by spectrum and intensity
            intensity_at_wavelength = intensity * spectrum[s]
            
            # Add to boundary field
            boundary_field[boundary_idx, :, :, s] .+= intensity_at_wavelength .* emission_mask
        end
    end
    
    return boundary_field
end

"""
    compute_call_of_void_potential(renderer::MatryoshkaRenderer, shell_radii::Vector{Float64}, shell_densities::Array{Float64}, shell_geometry::Dict)

Compute the "Call of the Void" potential effect that creates gravity and other forces.
Based on the dual-component potential with attractive and repulsive elements.
"""
function compute_call_of_void_potential(renderer::MatryoshkaRenderer, shell_radii::Vector{Float64}, shell_densities::Array{Float64}, shell_geometry::Dict)
    n_shells = length(shell_radii)
    height, width = size(shell_densities)[2:3]
    
    # Initialize potential field
    void_potential = zeros(n_shells, height, width)
    density_changes = zeros(n_shells, height, width)
    
    # Get mass centers from geometry
    if haskey(shell_geometry, :sphere_centers) && haskey(shell_geometry, :sphere_radii)
        centers = shell_geometry[:sphere_centers]
        radii = shell_geometry[:sphere_radii]
        n_masses = length(radii)
        
        # For each mass, compute its "Call of the Void" potential
        for m in 1:n_masses
            center = centers[m]
            mass_radius = radii[m]
            mass_distance = norm(center)
            
            # Attractive and repulsive parameters based on mass
            V1 = mass_radius  # Attractive strength proportional to radius
            V2 = renderer.v_ratio * V1  # Repulsive strength (ratio from renderer)
            σ1 = mass_radius * 2.0  # Attractive width
            σ2 = σ1 * renderer.sigma_ratio  # Repulsive width
            r1 = mass_distance  # Attractive center at mass distance
            r2 = mass_distance * 0.8  # Repulsive center slightly inside mass
            
            # For each shell, compute potential
            for i in 1:n_shells
                r = shell_radii[i]
                
                # The "Call of the Void" potential formula:
                # W_void = -V₁e^(-(r-r₁)²/2σ₁²) + V₂e^(-(r-r₂)²/2σ₂²)
                attractive = -V1 * exp(-(r - r1)^2 / (2 * σ1^2))
                repulsive = V2 * exp(-(r - r2)^2 / (2 * σ2^2))
                potential = attractive + repulsive
                
                # Calculate shell distortion from potential
                # This creates the effect of space-time curvature in shell structure
                void_potential[i, :, :] .+= potential
            end
        end
    end
    
    # Apply the potential to create density changes
    # Density flows from high potential to low potential
    for i in 1:(n_shells-1)
        # Compute potential gradient between adjacent shells
        potential_gradient = void_potential[i+1, :, :] - void_potential[i, :, :]
        
        # Density flows proportional to potential gradient
        flow = renderer.step_size * 0.05 * potential_gradient
        
        # Apply flow (density conservation)
        density_changes[i, :, :] .+= flow
        density_changes[i+1, :, :] .-= flow
    end
    
    return density_changes
end

"""
    propagate_shell_system(renderer::MatryoshkaRenderer)

Propagate the shell system forward one time step.
"""
function propagate_shell_system(renderer::MatryoshkaRenderer)
    # Check if initialized
    if !renderer.initialized
        initialize_shell_system(renderer)
    end
    
    # Extract state components
    state = renderer.state
    shell_densities = state[:shell_densities]
    boundary_field = state[:boundary_field]
    shell_phases = state[:shell_phases]
    boundary_phases = state[:boundary_phases]
    shell_coupling = state[:shell_coupling]
    boundary_coupling = state[:boundary_coupling]
    shell_boundary_coupling = state[:shell_boundary_coupling]
    shell_geometry = state[:shell_geometry]
    materials = state[:materials]
    shell_radii = state[:shell_radii]
    
    # 1. PHOTON PROPAGATION (strictly along boundaries)
    new_boundary_field = propagate_photons(renderer, boundary_field, boundary_coupling, boundary_phases)
    
    # 2. MATTER TRANSPORT (between shells)
    new_shell_densities = propagate_matter(renderer, shell_densities, shell_coupling, shell_phases, shell_radii, shell_geometry)
    
    # 3. SHELL-BOUNDARY INTERACTION (emission & absorption)
    # 3a. Emission (shell → boundary)
    shell_to_boundary = compute_emission(renderer, shell_densities, shell_boundary_coupling, shell_phases, boundary_phases)
    
    # 3b. Absorption (boundary → shell)
    boundary_to_shell, absorption_mask = compute_absorption(renderer, boundary_field, shell_boundary_coupling, shell_phases, boundary_phases)
    
    # Apply emission and absorption
    new_boundary_field = new_boundary_field .+ shell_to_boundary
    
    # Add additional dimension to absorption_mask for broadcasting
    expanded_absorption_mask = reshape(absorption_mask, size(absorption_mask)..., 1)
    new_boundary_field = new_boundary_field .* (1.0 .- expanded_absorption_mask)
    new_shell_densities = new_shell_densities .+ boundary_to_shell
    
    # 4. MATERIAL INTERACTIONS
    new_boundary_field = apply_material_interactions(renderer, new_boundary_field, shell_geometry, materials)
    
    # 5. UPDATE PHASES
    new_boundary_phases = update_boundary_phases(renderer, boundary_phases, new_boundary_field)
    new_shell_phases = update_shell_phases(renderer, shell_phases, new_shell_densities)
    
    # Update state
    state[:shell_densities] = new_shell_densities
    state[:boundary_field] = new_boundary_field
    state[:shell_phases] = new_shell_phases
    state[:boundary_phases] = new_boundary_phases
    
    return state
end

"""
    propagate_photons(renderer::MatryoshkaRenderer, boundary_field::Array{ComplexF64}, boundary_coupling::Matrix{Float64}, boundary_phases::Array{Float64})

Propagate photons along shell boundaries.
"""
function propagate_photons(renderer::MatryoshkaRenderer, boundary_field::Array{ComplexF64}, boundary_coupling::Matrix{Float64}, boundary_phases::Array{Float64})
    # For each boundary point and spectral component
    n_boundaries = size(boundary_field, 1)
    height, width = size(boundary_field)[2:3]
    n_spectral = size(boundary_field, 4)
    
    # Create wave propagation kernel
    new_boundary_field = copy(boundary_field)
    
    # For each spectral component
    for s in 1:n_spectral
        # Scale propagation by wavelength
        wavelength_factor = sqrt((s) / n_spectral)
        
        # Compute field changes
        for i in 1:n_boundaries
            for j in 1:n_boundaries
                if i != j
                    # Phase-dependent coupling
                    phase_diff = boundary_phases[i, :, :] .- boundary_phases[j, :, :]
                    coupling_factor = boundary_coupling[i, j] .* exp.(1im .* phase_diff)
                    
                    # Field transfer from j to i
                    contribution = coupling_factor .* wavelength_factor .* 
                                 (boundary_field[j, :, :, s] .- boundary_field[i, :, :, s])
                    
                    new_boundary_field[i, :, :, s] .+= renderer.step_size .* contribution
                end
            end
        end
    end
    
    return new_boundary_field
end

"""
    propagate_matter(renderer::MatryoshkaRenderer, shell_densities::Array{Float64}, shell_coupling::Matrix{Float64}, shell_phases::Array{Float64}, shell_radii::Vector{Float64}, shell_geometry::Dict)

Propagate matter between shells.
"""
function propagate_matter(renderer::MatryoshkaRenderer, shell_densities::Array{Float64}, shell_coupling::Matrix{Float64}, shell_phases::Array{Float64}, shell_radii::Vector{Float64}, shell_geometry::Dict)
    # For each shell point
    n_shells = size(shell_densities, 1)
    
    # Create density transport kernel
    new_shell_densities = copy(shell_densities)
    
    # Compute density changes
    for i in 1:n_shells
        for j in 1:n_shells
            if i != j
                # Phase-dependent coupling
                phase_diff = shell_phases[i, :, :] .- shell_phases[j, :, :]
                coupling_factor = shell_coupling[i, j] .* sin.(phase_diff)
                
                # Density transfer from j to i
                contribution = coupling_factor .* (shell_densities[j, :, :] .- shell_densities[i, :, :])
                
                new_shell_densities[i, :, :] .+= renderer.step_size .* contribution
            end
        end
    end
    
    # Apply "Call of the Void" potential effect
    void_effect = compute_call_of_void_potential(renderer, shell_radii, shell_densities, shell_geometry)
    new_shell_densities .+= void_effect
    
    # Update shell densities (ensure non-negative)
    return max.(0.0, new_shell_densities)
end

"""
    compute_emission(renderer::MatryoshkaRenderer, shell_densities::Array{Float64}, shell_boundary_coupling::Matrix{Float64}, shell_phases::Array{Float64}, boundary_phases::Array{Float64})

Compute emission from shells to boundaries.
"""
function compute_emission(renderer::MatryoshkaRenderer, shell_densities::Array{Float64}, shell_boundary_coupling::Matrix{Float64}, shell_phases::Array{Float64}, boundary_phases::Array{Float64})
    # Initialize emission field
    n_shells = size(shell_densities, 1)
    n_boundaries = size(boundary_phases, 1)
    height, width = size(shell_densities)[2:3]
    emission = zeros(ComplexF64, n_boundaries, height, width, renderer.spectral_samples)
    
    # Simple emission model for demonstration
    # Each shell emits to adjacent boundaries based on density
    for i in 1:n_shells
        for j in 1:n_boundaries
            # Phase difference based emission
            phase_diff = shell_phases[i, :, :] .- boundary_phases[j, :, :]
            coupling = shell_boundary_coupling[i, j]
            
            # Emission strength proportional to density and coupling
            strength = coupling .* shell_densities[i, :, :]
            
            # Create emission pattern across spectrum
            # (Simple blackbody-like spectrum)
            for s in 1:renderer.spectral_samples
                # Temperature-like spectrum (higher shells = hotter)
                temp_factor = exp.(-(s - i/n_shells*renderer.spectral_samples)^2 / 
                               (2 * (n_shells/5)^2))
                
                # Create emission with phase information
                spec_emission = strength .* temp_factor .* exp.(1im .* phase_diff)
                
                # Add to emission field
                emission[j, :, :, s] .+= renderer.step_size * 0.1 .* spec_emission
            end
        end
    end
    
    return emission
end

"""
    compute_absorption(renderer::MatryoshkaRenderer, boundary_field::Array{ComplexF64}, shell_boundary_coupling::Matrix{Float64}, shell_phases::Array{Float64}, boundary_phases::Array{Float64})

Compute absorption from boundaries to shells.
"""
function compute_absorption(renderer::MatryoshkaRenderer, boundary_field::Array{ComplexF64}, shell_boundary_coupling::Matrix{Float64}, shell_phases::Array{Float64}, boundary_phases::Array{Float64})
    # Initialize absorption
    n_shells = size(shell_phases, 1)
    n_boundaries = size(boundary_field, 1)
    height, width = size(boundary_field)[2:3]
    absorption = zeros(n_shells, height, width)
    
    # Absorption mask (how much energy is removed from boundary field)
    absorption_mask = zeros(n_boundaries, height, width)
    
    # Simple absorption model
    # Boundaries transfer energy to adjacent shells
    for i in 1:n_boundaries
        # Compute total intensity at this boundary
        intensity = sum(abs2.(boundary_field[i, :, :, :]), dims=3)[:, :, 1]
        
        for j in 1:n_shells
            # Phase difference based absorption
            phase_diff = boundary_phases[i, :, :] .- shell_phases[j, :, :]
            coupling = shell_boundary_coupling[j, i]  # Note index swap
            
            # Absorption strength proportional to intensity and coupling
            strength = coupling .* intensity
            
            # Add to shell
            absorption[j, :, :] .+= renderer.step_size * 0.1 .* strength .* cos.(phase_diff).^2
            
            # Remove from boundary
            absorption_mask[i, :, :] .+= renderer.step_size * 0.1 .* coupling .* cos.(phase_diff).^2
        end
    end
    
    # Clamp absorption mask to avoid overabsorption
    absorption_mask = min.(absorption_mask, 0.5)
    
    return absorption, absorption_mask
end

"""
    apply_material_interactions(renderer::MatryoshkaRenderer, boundary_field::Array{ComplexF64}, shell_geometry::Dict, materials::Dict)

Apply material interactions to boundary field.
"""
function apply_material_interactions(renderer::MatryoshkaRenderer, boundary_field::Array{ComplexF64}, shell_geometry::Dict, materials::Dict)
    # Extract material properties
    reflectance = materials[:reflectance]
    transmittance = materials[:transmittance]
    absorption = materials[:absorption]
    
    # Extract geometry
    occupancy = shell_geometry[:occupancy]
    material_indices = shell_geometry[:material_indices]
    
    # Initialize new field
    new_field = copy(boundary_field)
    
    # Apply material response at shell-boundary interface
    n_boundaries = size(boundary_field, 1)
    n_materials = length(material_indices)
    
    # For each boundary
    for i in 1:n_boundaries
        # Adjacent shells
        shell_idx1 = i
        shell_idx2 = i + 1
        
        if shell_idx1 > size(occupancy, 1) || shell_idx2 > size(occupancy, 1)
            continue
        end
            
        # For each material
        for m in 1:n_materials
            mat_idx = material_indices[m] + 1  # Julia uses 1-based indexing
            
            # Occupancy of this material in adjacent shells
            occ1 = occupancy[shell_idx1, m]
            occ2 = shell_idx2 <= size(occupancy, 1) ? occupancy[shell_idx2, m] : 0.0
            
            # Material effect is proportional to occupancy
            effect = max(occ1, occ2)
            
            # Get material properties
            r = reflectance[mat_idx]
            t = transmittance[mat_idx]
            a = absorption[mat_idx]
            
            # Apply to boundary field
            # Reflection and transmission (simplified)
            new_field[i, :, :, :] .*= (1.0 - effect * a) .* (effect * (t + r) + (1 - effect))
        end
    end
    
    return new_field
end

"""
    update_boundary_phases(renderer::MatryoshkaRenderer, boundary_phases::Array{Float64}, boundary_field::Array{ComplexF64})

Update boundary phases based on field evolution.
"""
function update_boundary_phases(renderer::MatryoshkaRenderer, boundary_phases::Array{Float64}, boundary_field::Array{ComplexF64})
    # Phase evolves based on field intensity
    intensity = sum(abs2.(boundary_field), dims=4)[:, :, :, 1]
    phase_change = renderer.step_size * 0.5 .* intensity
    
    # Add phase rotation from field
    field_angle = angle.(mean(boundary_field, dims=4)[:, :, :, 1])
    
    # Update phases
    new_phases = boundary_phases .+ phase_change .+ renderer.step_size * 0.2 .* field_angle
    
    # Normalize to [0, 2π)
    return mod2pi.(new_phases)
end

"""
    update_shell_phases(renderer::MatryoshkaRenderer, shell_phases::Array{Float64}, shell_densities::Array{Float64})

Update shell phases based on density evolution.
"""
function update_shell_phases(renderer::MatryoshkaRenderer, shell_phases::Array{Float64}, shell_densities::Array{Float64})
    # Phase evolves based on density
    phase_change = renderer.step_size .* shell_densities
    
    # Update phases
    new_phases = shell_phases .+ phase_change
    
    # Normalize to [0, 2π)
    return mod2pi.(new_phases)
end

"""
    project_to_camera(renderer::MatryoshkaRenderer)

Project shell system state to camera to create rendered image.
"""
function project_to_camera(renderer::MatryoshkaRenderer)
    # Check if initialized
    if !renderer.initialized
        return zeros(64, 64, 3)  # Return empty image if not initialized
    end
    
    # Extract state
    state = renderer.state
    
    # Get camera properties from scene
    if !haskey(renderer.scene, :camera)
        camera = Dict(
            :position => [0.0, 0.0, -5.0],
            :direction => [0.0, 0.0, 1.0],
            :up => [0.0, 1.0, 0.0],
            :fov => 60.0
        )
    else
        camera = renderer.scene[:camera]
    end
    
    # Extract camera properties
    position = get(camera, :position, [0.0, 0.0, -5.0])
    direction = get(camera, :direction, [0.0, 0.0, 1.0])
    up = get(camera, :up, [0.0, 1.0, 0.0])
    fov = get(camera, :fov, 60.0)
    response = get(camera, :spectral_response, nothing)
    
    # Default spectral response if not provided
    if response === nothing
        # CIE 1931 standard observer (approximated)
        wavelengths = state[:wavelengths]
        response = zeros(length(wavelengths), 3)
        
        # Simple RGB response curves
        for (i, wl) in enumerate(wavelengths)
            # Red response
            response[i, 1] = exp(-((wl - 650)^2) / (2 * 60^2))
            # Green response
            response[i, 2] = exp(-((wl - 550)^2) / (2 * 60^2))
            # Blue response
            response[i, 3] = exp(-((wl - 450)^2) / (2 * 60^2))
        end
    end
    
    # Extract boundary field (photons propagate along boundaries)
    boundary_field = state[:boundary_field]
    boundary_radii = state[:boundary_radii]
    
    # Compute distance from camera to each boundary
    camera_distance = norm(position)
    
    # Find boundaries that contribute to image
    # Weigh by distance from camera plane
    weights = exp.(-((abs.(boundary_radii .- camera_distance)) ./ 
                   (0.2 * camera_distance)).^2)
    
    # Apply weights to boundary field
    weighted_field = reshape(weights, :, 1, 1, 1) .* boundary_field
    
    # Sum over boundaries to get image
    spectral_image = sum(abs2.(weighted_field), dims=1)[1, :, :, :]
    
    # Convert to RGB using spectral response
    height, width = size(spectral_image)[1:2]
    rgb_image = zeros(height, width, 3)
    
    for c in 1:3
        for s in 1:renderer.spectral_samples
            rgb_image[:, :, c] .+= spectral_image[:, :, s] .* response[s, c]
        end
    end
    
    # Apply tone mapping
    rgb_image = tone_mapping(rgb_image)
    
    return rgb_image
end

"""
    tone_mapping(hdr_image::Array{Float64})

Apply tone mapping to convert HDR to LDR.
"""
function tone_mapping(hdr_image::Array{Float64})
    # Simple Reinhard tone mapping
    return hdr_image ./ (1.0 .+ hdr_image)
end

"""
    create_test_scene(renderer::MatryoshkaRenderer, resolution::Tuple{Int, Int}=(128, 128))

Create a simple test scene for the renderer.
"""
function create_test_scene(renderer::MatryoshkaRenderer, resolution::Tuple{Int, Int}=(128, 128))
    # Create geometry
    geometry = Dict(
        :spheres => Dict(
            :centers => [
                [0.0, 0.0, 0.0],    # Center sphere
                [1.5, 0.5, 0.5],    # Right sphere
                [-1.5, -0.5, 0.5],  # Left sphere
            ],
            :radii => [1.0, 0.5, 0.7],
            :material_indices => [0, 1, 2]
        ),
        :emitters => Dict(
            :positions => [
                [3.0, 3.0, -3.0],   # Top-right light
                [-3.0, 3.0, -3.0],  # Top-left light
            ],
            :intensities => [2.0, 1.5],
        :spectra => [ones(renderer.spectral_samples) for _ in 1:2],
        )
    )
    
    # Create materials
    materials = Dict(
        :reflectance => [0.8, 0.1, 0.6],      # Reflectance for each material
        :transmittance => [0.1, 0.8, 0.2],    # Transmittance for each material
        :absorption => [0.1, 0.1, 0.2],       # Absorption for each material
        :emission_strength => [0.0, 0.0, 0.0] # No emission from materials
    )
    
    # Create camera
    camera = Dict(
        :position => [0.0, 0.0, -5.0],
        :direction => [0.0, 0.0, 1.0],
        :up => [0.0, 1.0, 0.0],
        :fov => 60.0
    )
    
    # Store scene in renderer
    renderer.scene = Dict(
        :geometry => geometry,
        :materials => materials,
        :camera => camera,
        :resolution => resolution
    )
    
    # Mark as uninitialized to force reinitialization
    renderer.initialized = false
    
    return renderer.scene
end

"""
    visualize_renderer_state(renderer::MatryoshkaRenderer)

Create visualization of the renderer's current state.
"""
function visualize_renderer_state(renderer::MatryoshkaRenderer)
    # Check if initialized
    if !renderer.initialized
        return plot(title="Renderer not initialized", axis=false)
    end
    
    # Extract state
    state = renderer.state
    shell_densities = state[:shell_densities]
    shell_radii = state[:shell_radii]
    boundary_field = state[:boundary_field]
    boundary_radii = state[:boundary_radii]
    
    # Create plot with multiple panels
    p = plot(layout=(2, 2), size=(800, 800), legend=false)
    
    # 1. Plot average shell densities
    avg_densities = mean(shell_densities, dims=(2, 3))[:, 1, 1]
    plot!(
        p[1, 1],
        shell_radii, 
        avg_densities, 
        marker=:circle,
        xlabel="Shell Radius",
        ylabel="Average Density",
        title="Shell Density Distribution",
        grid=true,
        linewidth=2
    )
    
    # 2. Plot boundary field intensity
    intensity = mean(abs2.(boundary_field), dims=(2, 3, 4))[:, 1, 1, 1]
    plot!(
        p[1, 2],
        boundary_radii, 
        intensity, 
        marker=:circle,
        color=:red,
        xlabel="Boundary Radius",
        ylabel="Field Intensity",
        title="Boundary Field Intensity",
        grid=true,
        linewidth=2
    )
    
    # 3. Calculate and plot the "Call of the Void" potential
    # Simplified version of the potential for visualization
    n_shells = length(shell_radii)
    potential = zeros(n_shells)
    
    # Use geometry data if available
    if haskey(state[:shell_geometry], :sphere_centers)
        centers = state[:shell_geometry][:sphere_centers]
        radii = state[:shell_geometry][:sphere_radii]
        
        for m in 1:length(radii)
            mass_radius = radii[m]
            mass_distance = norm(centers[m])
            
            # Parameters based on mass
            V1 = mass_radius
            V2 = renderer.v_ratio * V1
            σ1 = mass_radius * 2.0
            σ2 = σ1 * renderer.sigma_ratio
            r1 = mass_distance
            r2 = mass_distance * 0.8
            
            # Calculate potential
            for i in 1:n_shells
                r = shell_radii[i]
                potential[i] += -V1 * exp(-(r - r1)^2 / (2 * σ1^2)) + 
                                V2 * exp(-(r - r2)^2 / (2 * σ2^2))
            end
        end
    end
    
    # Plot the potential
    plot!(
        p[2, 1],
        shell_radii,
        potential,
        marker=:circle,
        color=:purple,
        xlabel="Shell Radius",
        ylabel="Potential",
        title="\"Call of the Void\" Potential",
        grid=true,
        linewidth=2
    )
    
    # 4. Plot shell density cross-section
    # Take middle slice of densities for visualization
    h, w = size(shell_densities, 2), size(shell_densities, 3)
    middle_slice = shell_densities[:, div(h, 2), :]
    
    heatmap!(
        p[2, 2],
        1:w,
        shell_radii,
        middle_slice,
        xlabel="Position",
        ylabel="Shell Radius",
        title="Shell Density Cross-section",
        c=:viridis
    )
    
    return p
end

"""
    create_interactive_gui()

Create an interactive GUI for the Matryoshka-Chronon renderer.
"""
function create_interactive_gui()
    # Set up logging
    logger = ConsoleLogger(stderr, Logging.Info)
    global_logger(logger)
    
    @info "Starting interactive Matryoshka-Chronon renderer"
    
    # Create renderer with default parameters
    config = Dict{Symbol, Any}(  # Explicitly specify Dict{Symbol, Any}
        :shell_count => 24,
        :spectral_samples => 8,
        :step_size => 0.1,
        :max_steps => 30,
        :seed => 42
    )
    
    @info "Creating renderer with config: $config"
    renderer = MatryoshkaRenderer(config)
    
    # Create default scene
    @info "Creating test scene"
    create_test_scene(renderer, (96, 96))
    
    # Initialize system
    @info "Initializing shell system"
    try
        initialize_shell_system(renderer)
        @info "Shell system initialized successfully"
    catch e
        @error "Failed to initialize shell system" exception=(e, catch_backtrace())
        rethrow(e)
    end
    # Create widgets for parameter control
    shell_count_slider = slider(8:4:40, label="Shell Count", value=24)
    alpha_slider = slider(0.05:0.01:0.2, label="Shell Scaling (α)", value=0.1)
    
    # "Call of the Void" potential parameters
    v_ratio_slider = slider(0.5:0.05:2.0, label="V₂/V₁ Ratio", value=1.2)
    sigma_ratio_slider = slider(0.3:0.05:1.0, label="σ₂/σ₁ Ratio", value=0.7)
    
    # Coupling parameters
    boundary_coupling_slider = slider(0.3:0.05:1.5, label="Boundary Coupling", value=0.9)
    coupling_decay_slider = slider(0.1:0.05:0.5, label="Coupling Decay", value=0.3)
    
    # Rendering parameters
    step_size_slider = slider(0.05:0.01:0.2, label="Step Size", value=0.1)
    
    # Scene controls
    center_sphere_size = slider(0.5:0.1:2.0, label="Center Sphere Size", value=1.0)
    light_intensity = slider(0.5:0.1:3.0, label="Light Intensity", value=2.0)
    
    # Create toggles and buttons
    auto_update = toggle(label="Auto Update", value=true)
    show_visualization = toggle(label="Show State Visualization", value=true)
    
    # Button to take a single simulation step
    step_button = button("Take Simulation Step")
    
    # Button to reset the simulation
    reset_button = button("Reset Simulation")
    
    # Create plots for displaying results
    render_plot = plot(title="Rendered Image", axis=false)
    viz_plot = plot(title="System State", axis=false)
    
    # Update function for parameter changes
    function update_parameters(shell_count, alpha, v_ratio, sigma_ratio, boundary_coupling, coupling_decay, step_size)
        params = Dict{Symbol, Any}(  # Also fix here
            :shell_count => shell_count,
            :alpha => alpha,
            :v_ratio => v_ratio,
            :sigma_ratio => sigma_ratio,
            :boundary_coupling => boundary_coupling,
            :coupling_decay => coupling_decay,
            :step_size => step_size
        )
        
        # Update renderer parameters
        core_changed = update_parameters!(renderer, params)
        
        # Reinitialize if core parameters changed
        if core_changed
            initialize_shell_system(renderer)
        end
    end
    
    # Update function for scene parameters
    function update_scene(center_size, light_int)
        # Update center sphere size
        renderer.scene[:geometry][:spheres][:radii][1] = center_size
        
        # Update light intensities
        renderer.scene[:geometry][:emitters][:intensities][1] = light_int
        renderer.scene[:geometry][:emitters][:intensities][2] = light_int * 0.75
        
        # Mark as uninitialized to force reinitialization
        renderer.initialized = false
        initialize_shell_system(renderer)
        return true  # Explicitly return a boolean value for the Observable
    end
    # Update visualization function
    function update_visualization()
        local render_plot, viz_plot
        local start_time = time()
        
        try
            @info "Starting visualization update" timestamp=Dates.now() thread=Threads.threadid()
            
            # Render image using the camera projection
            @info "Projecting to camera"
            img = project_to_camera(renderer)
            
            # Process image data for display
            @info "Processing image data"
            rgb_img = clamp.(img, 0.0, 1.0)
            
            # Convert to an RGB image for display
            @info "Converting to color image"
            @debug "Image size: $(size(rgb_img))"
            
            # Defensive check for NaN values
            if any(isnan, rgb_img)
                @warn "NaN values detected in rendered image, replacing with zeros"
                rgb_img = replace(rgb_img, NaN => 0.0)
            end
            
            # Check for invalid array dimensions
            if size(rgb_img, 3) != 3
                @warn "Invalid RGB dimensions: $(size(rgb_img)), reshaping"
                if ndims(rgb_img) == 2  # If image is 2D
                    rgb_img = reshape(rgb_img, size(rgb_img)..., 1)
                    # Repeat the grayscale for all channels
                    rgb_img = repeat(rgb_img, 1, 1, 3)
                elseif size(rgb_img, 3) < 3  # If not enough color channels
                    # Pad with zeros
                    dims = size(rgb_img)
                    new_img = zeros(dims[1], dims[2], 3)
                    new_img[:, :, 1:size(rgb_img, 3)] = rgb_img
                    rgb_img = new_img
                elseif size(rgb_img, 3) > 3  # If too many channels
                    rgb_img = rgb_img[:, :, 1:3]  # Take first three
                end
            end
            
            # Create colorview from RGB array
            color_img = colorview(RGB, permutedims(rgb_img, (3, 1, 2)))
            
            # Create an image plot with the full color image
            @info "Creating render plot"
            render_plot = plot(
                color_img,
                title="Rendered Image",
                axis=false,
                aspect_ratio=:equal,
                yflip=true
            )
            
            # Update state visualization if enabled
            if show_visualization[]
                @info "Creating visualization plot"
                viz_plot = visualize_renderer_state(renderer)
            else
                viz_plot = plot(title="Visualization disabled", axis=false)
            end
            
            # Calculate and log elapsed time
            elapsed = time() - start_time
            @info "Visualization update completed in $(elapsed) seconds"
            
        catch e
            @error "Error in visualization update" exception=(e, catch_backtrace())
            
            # Create fallback plots in case of error
            render_plot = plot(title="Rendering Error: $(typeof(e))", axis=false)
            viz_plot = plot(title="Visualization Error", axis=false)
            
            # Add some text to the error plot to show the error message
            plot!(render_plot, [0], [0], series_type=:scatter, markersize=0,
                  annotations=(0, 0, text("$(e)", :center, 9)))
            
            # Don't rethrow to keep UI responsive
        end
        
        return render_plot, viz_plot
    end
    
    # Function to take a simulation step
    function take_step()
        try
            @info "Taking simulation step"
            propagate_shell_system(renderer)
            @info "Simulation step completed, updating visualization"
            return update_visualization()
        catch e
            @error "Error in simulation step" exception=(e, catch_backtrace())
            # Return empty plots to avoid UI freeze
            return plot(title="Simulation Error", axis=false), plot(title="Visualization Error", axis=false)
        end
    end
    
    # Function to reset simulation
    function reset_simulation()
        try
            @info "Resetting simulation"
            # Update parameters
            update_parameters(
                shell_count_slider[], 
                alpha_slider[], 
                v_ratio_slider[], 
                sigma_ratio_slider[], 
                boundary_coupling_slider[], 
                coupling_decay_slider[], 
                step_size_slider[]
            )
            
            # Update scene
            update_scene(center_sphere_size[], light_intensity[])
            
            # Reinitialize
            @info "Reinitializing shell system"
            initialize_shell_system(renderer)
            
            @info "Reset completed, updating visualization"
            return update_visualization()
        catch e
            @error "Error in simulation reset" exception=(e, catch_backtrace())
            # Return empty plots to avoid UI freeze
            return plot(title="Reset Error", axis=false), plot(title="Visualization Error", axis=false)
        end
    end
    
    # Connect UI elements
    # Create a wrapper function to ensure all args are passed correctly
    function safe_update_parameters(a, b, c, d, e, f, g)
        update_parameters(a, b, c, d, e, f, g)
        return true  # Explicitly return a boolean value for the Observable
    end
    
    # Create a destination observable for the parameters update
    parameters_updated = Observable(false)
    
    # Connect parameters through a combined map
    map!(safe_update_parameters, 
        parameters_updated, # destination observable 
        observe(shell_count_slider), 
        observe(alpha_slider),
        observe(v_ratio_slider), 
        observe(sigma_ratio_slider),
        observe(boundary_coupling_slider), 
        observe(coupling_decay_slider),
        observe(step_size_slider))
    
    # Create a destination observable for scene updates
    scene_updated = Observable(false)
    
    # Connect scene parameters through a map
    map!(update_scene, 
        scene_updated, # destination observable
        observe(center_sphere_size), 
        observe(light_intensity))
    
    # Connect buttons
    on(x -> take_step(), observe(step_button))
    on(x -> reset_simulation(), observe(reset_button))
    on(x -> reset_simulation(), observe(reset_button))
    
    # Create locks for thread safety
    update_lock = ReentrantLock()
    visualization_lock = ReentrantLock()
    ui_update_lock = ReentrantLock() # New lock for UI updates
    
    # Variables to store state and references
    timer_ref = Ref{Union{Timer, Nothing}}(nothing)
    # Variables to store state and references - use atomic for thread safety
    timer_ref = Ref{Union{Timer, Nothing}}(nothing)
    is_running = Ref{Bool}(true)
    last_update_time = Ref{Float64}(time())
    consecutive_errors = Ref{Int}(0) # Track consecutive errors
    ui_plots = Ref{Tuple}((plot(), plot())) # Store latest plots
    ui_update_in_progress = Ref{Bool}(false) # Track if UI update is in progress
    last_ui_update_time = Ref{Float64}(time())
    update_cycle_running = Ref{Bool}(false) # Track if update cycle is running
    update_cycle_start_time = Ref{Float64}(0.0) # Track when update cycle started
    last_visualization_time = Ref{Float64}(0.0) # Track when visualization last completed
    
    # Function to update the UI without blocking the timer thread
    function update_ui_plots(p_render, p_viz)
        # Skip update if another one is in progress and it hasn't been too long
        elapsed_since_last_ui = time() - last_ui_update_time[]
        if ui_update_in_progress[] && elapsed_since_last_ui < 1.0
            @info "Skipping UI update - another update in progress ($elapsed_since_last_ui sec)"
            return
        end
        
        # Try to get the lock with a short timeout
        timeout = 0.5
        start_time = time()
        locked = false
        
        while !locked && (time() - start_time < timeout)
            locked = trylock(ui_update_lock)
            if !locked
                sleep(0.01)
            end
        end
        
        if !locked
            @warn "Could not acquire UI update lock after $timeout seconds"
            
            # Force unlock if it's been too long since the last update
            if elapsed_since_last_ui > 5.0 && islocked(ui_update_lock)
                @warn "Possible UI deadlock, force unlocking"
                try unlock(ui_update_lock) catch; end
                ui_update_in_progress[] = false
                return
            end
            return
        end
        
        try
            ui_update_in_progress[] = true
            @info "Updating UI plots" timestamp=Dates.now()
            
            # Use try-catch to ensure no errors break the UI update
            try
                # Store the latest plots
                ui_plots[] = (p_render, p_viz)
                last_ui_update_time[] = time()
            catch e
                @error "Error storing UI plots" exception=(e, catch_backtrace())
            end
        catch e
            @error "Error in UI update" exception=(e, catch_backtrace())
        finally
            ui_update_in_progress[] = false
            if islocked(ui_update_lock)
                unlock(ui_update_lock)
            end
        end
    end
    function auto_update_timer()
        # Use try-catch for the entire function to catch any unexpected errors
        try
            # Early exit if not running anymore
            if !is_running[]
                @info "Auto-update: system is shutting down, stopping timer"
                return
            end
            
            current_time = time()
            elapsed = current_time - last_update_time[]
            @info "Auto-update timer fired after $(elapsed) seconds" timestamp=Dates.now()
            
            # Check if another update cycle is already running
            if update_cycle_running[]
                cycle_duration = current_time - update_cycle_start_time[]
                @warn "Another update cycle is already running for $(cycle_duration) seconds"
                
                # If update cycle has been running too long, it might be stuck
                if cycle_duration > 10.0
                    @warn "Update cycle appears stuck, attempting recovery"
                    # Force reset all locks and state variables
                    for lock in [update_lock, visualization_lock, ui_update_lock, timer_lock]
                        if islocked(lock)
                            try unlock(lock) catch; end
                        end
                    end
                    
                    # Reset state variables
                    update_cycle_running[] = false
                    ui_update_in_progress[] = false
                    
                    # Force GC to clean up any pending resources
                    GC.gc()
                end
                
                # Schedule another attempt and return
                schedule_next_update(1.0)
                return
            end
            
            # Mark update cycle as running and track start time
            update_cycle_running[] = true
            update_cycle_start_time[] = current_time
            
            # Try to lock with timeout to avoid deadlocks (3 second timeout)
            timeout = 3.0
            lock_start = time()
            locked = false
            
            while !locked && (time() - lock_start < timeout)
                locked = trylock(update_lock)
                if !locked
                    # Small sleep to avoid CPU spinning
                    sleep(0.01)
                end
            end
            
            if !locked
                @warn "Could not acquire update lock after $(timeout) seconds, possible deadlock"
                # Force reset locks if we suspect a deadlock
                if elapsed > 5.0
                    @warn "Possible deadlock detected, force resetting locks"
                    if islocked(update_lock)
                        try unlock(update_lock) catch; end
                    end
                    if islocked(visualization_lock)
                        try unlock(visualization_lock) catch; end
                    end
                    if islocked(ui_update_lock)
                        try unlock(ui_update_lock) catch; end
                    end
                    last_update_time[] = current_time
                end
                
                # Mark update cycle as not running before returning
                update_cycle_running[] = false
                
                # Schedule another attempt and return
                schedule_next_update(1.0)
                return
            end
            
            # We got the lock, proceed with update
            update_successful = false
            try
                if auto_update[] && is_running[]
                    @info "Auto-update: propagating system" thread=Threads.threadid()
                    try
                        # Track start time for performance monitoring
                        start_time = time()
                        
                        # Propagate system with timeout protection
                        if current_time - last_update_time[] > 10.0
                            @warn "Long time since last update, reinitializing system"
                            # Reinitialize system if it's been too long
                            initialize_shell_system(renderer)
                            last_update_time[] = current_time
                        else
                            # Normal propagation
                            propagate_shell_system(renderer)
                        end
                        
                        prop_time = time() - start_time
                        @info "Propagation completed in $(prop_time) seconds"
                        
                        # Update visualization with timeout protection
                        viz_locked = false
                        viz_lock_start = time()
                        
                        # Try to get visualization lock with timeout
                        while !viz_locked && (time() - viz_lock_start < 2.0)
                            viz_locked = trylock(visualization_lock)
                            if !viz_locked
                                sleep(0.01)
                            end
                        end
                        
                        if viz_locked
                            try
                                @info "Updating visualization after propagation"
                                local render_plot, viz_plot
                                
                                # Use a watchdog timer to prevent visualization from taking too long
                                viz_watchdog = Timer(5.0) do t
                                    if islocked(visualization_lock)
                                        @warn "Visualization taking too long, force unlock"
                                        try unlock(visualization_lock) catch; end
                                    end
                                end
                                
                                try
                                    render_plot, viz_plot = update_visualization()
                                    close(viz_watchdog)
                                    
                                    # Update the UI in a separate task to avoid blocking
                                    @async update_ui_plots(render_plot, viz_plot)
                                    
                                    vis_time = time() - start_time - prop_time
                                    @info "Visualization completed in $(vis_time) seconds"
                                    update_successful = true
                                    consecutive_errors[] = 0 # Reset error counter on success
                                catch e
                                    close(viz_watchdog)
                                    @error "Error in visualization update" exception=(e, catch_backtrace())
                                    consecutive_errors[] += 1
                                end
                            finally
                                if islocked(visualization_lock)
                                    unlock(visualization_lock)
                                end
                            end
                        else
                            @info "Visualization lock timeout, skipping visualization"
                        end
                        
                        # Record total time
                        total_time = time() - start_time
                        @info "Total update cycle completed in $(total_time) seconds"
                    catch e
                        @error "Error in auto-update propagation" exception=(e, catch_backtrace())
                        consecutive_errors[] += 1
                    end
                end
            finally
                if islocked(update_lock)
                    unlock(update_lock)
                end
            end
            
            if update_successful
                last_update_time[] = current_time
                last_visualization_time[] = current_time
            end
        catch e
            # Catch-all for unexpected errors in the timer function
            @error "Critical error in auto-update timer" exception=(e, catch_backtrace())
            consecutive_errors[] += 1
        finally
            # Always mark update cycle as complete, regardless of success or failure
            update_cycle_running[] = false
        end
        
        # Schedule next update or perform recovery - use a timer to add a slight delay
        # This helps prevent rapid consecutive calls if there are errors
        try
            Timer(t -> schedule_next_update(), 0.1)
        catch e
            @error "Failed to create timer for scheduling next update" exception=(e, catch_backtrace())
            # Direct call as fallback
            schedule_next_update()
        end
    end
    
    # Helper function to schedule the next update with dynamic timing based on system state
    # Timer management system with improved thread safety
    timer_lock = ReentrantLock()
    
    function schedule_next_update(override_interval = nothing)
        if !is_running[]
            @info "Auto-update system is shutting down, not scheduling next update"
            return
        end
        
        # Ensure only one thread can update the timer at a time
        locked = trylock(timer_lock)
        if !locked
            @warn "Timer lock contention - skipping this timer update"
            return
        end
        
        try
            # Use override interval if provided, otherwise calculate dynamically
            interval = override_interval
            
            if interval === nothing
                # Dynamic interval based on system state
                elapsed = time() - last_update_time[]
                error_count = consecutive_errors[]
                
                # Increase interval if we're seeing errors
                if error_count > 3
                    interval = min(2.0, 0.5 * error_count) # Back off up to 2 seconds
                    @warn "Multiple errors detected ($error_count), increasing interval to $interval"
                elseif elapsed > 0.5
                    # Slow down if updates are taking too long
                    interval = 0.3
                else
                    # Normal operation
                    interval = 0.1
                end
                
                # Emergency recovery if system seems to be in a bad state
                if elapsed > 5.0 || error_count > 5
                    @warn "Emergency recovery triggered (elapsed: $elapsed, errors: $error_count)"
                    try
                        # Force release all locks before system reinitialization
                        for lock in [update_lock, visualization_lock, ui_update_lock, timer_lock]
                            if islocked(lock)
                                try unlock(lock) catch; end
                            end
                        end
                        
                        # Reset all state tracking variables
                        update_cycle_running[] = false
                        ui_update_in_progress[] = false
                        
                        # Force GC to clean up any pending resources
                        GC.gc()
                        
                        # Force reinitialize system
                        @info "Forcing system reinitialization for recovery"
                        initialize_shell_system(renderer)
                        
                        # Reset error counter on successful reinitialization
                        consecutive_errors[] = 0
                        
                        # Use a longer interval to give system time to stabilize
                        interval = 1.0
                        
                        # Update last update time to prevent immediate re-recovery
                        last_update_time[] = time()
                    catch e
                        @error "Emergency recovery failed" exception=(e, catch_backtrace())
                        # Use even longer interval on failed recovery
                        interval = 2.0
                        consecutive_errors[] += 1
                        
                        # Last resort - create fallback visualization state
                        try
                            # Try to create a minimal valid state
                            @warn "Creating fallback renderer state"
                            create_test_scene(renderer, (48, 48)) # Smaller resolution for recovery
                            initialize_shell_system(renderer)
                        catch recovery_e
                            @error "Failed to create fallback state" exception=recovery_e
                        end
                    end
                end
            end
            
            # Create and store timer with defensive error handling
            @info "Scheduling next update in $interval seconds"
            try
                old_timer = timer_ref[]
                
                # Create a unique identifier for this timer creation to avoid race conditions
                timer_id = string(rand(UInt64))
                @info "Creating timer with ID: $timer_id"
                
                # Check if we already have a timer reference and it's valid
                if old_timer !== nothing && elapsed < 10.0
                    # Only skip if we're not in emergency recovery
                    if !(elapsed > 5.0 || error_count > 5)
                        # Skip creating a new timer if we already have a recent valid one
                        @info "Existing valid timer found, skipping creation of new timer"
                        return
                    else
                        @info "Emergency recovery in progress, replacing existing timer"
                    end
                end
                
                # Create a safe wrapper for the auto-update function that tracks completion
                function safe_auto_update(timer)
                    try
                        @info "Timer $timer_id fired"
                        auto_update_timer()
                    catch e
                        @error "Error in safe_auto_update wrapper" exception=(e, catch_backtrace())
                        # Increment error counter
                        consecutive_errors[] += 1
                        
                        # Force cleanup of any locks that might be held
                        for lock in [update_lock, visualization_lock, ui_update_lock, timer_lock]
                            if islocked(lock)
                                try unlock(lock) catch; end
                            end
                        end
                        
                        # Reset state tracking variables
                        update_cycle_running[] = false
                        ui_update_in_progress[] = false
                        
                        # Schedule a recovery update after a delay
                        error_count = consecutive_errors[]
                        recovery_delay = min(5.0, 0.5 * error_count)
                        
                        # Only attempt recovery if we haven't had too many errors
                        if error_count < 20
                            try
                                Timer(t -> schedule_next_update(recovery_delay), recovery_delay)
                            catch
                                # Last resort direct call
                                @warn "Failed to create recovery timer, directly scheduling update"
                                schedule_next_update(recovery_delay + 1.0)
                            end
                        else
                            @error "Too many consecutive errors ($error_count), suspending auto-updates"
                            is_running[] = false
                        end
                    end
                end
                
                # Create the timer with the safe wrapper
                new_timer = Timer(safe_auto_update, interval)
                timer_ref[] = new_timer
                
                # Close old timer if it exists
                if old_timer !== nothing
                    try
                        close(old_timer)
                    catch e
                        @warn "Error closing old timer" exception=e
                    end
                end
            catch e
                @error "Failed to schedule next update" exception=(e, catch_backtrace())
                # Last resort - try once more with a longer delay
                try
                    # Check if system is still running
                    if is_running[]
                        timer_ref[] = Timer(t -> auto_update_timer(), 2.0)
                    end
                catch ee
                    @error "Critical failure in timer scheduling, visualization loop may be interrupted" exception=ee
                    # Force is_running to false to prevent further timer scheduling attempts
                    if consecutive_errors[] > 10
                        @warn "Too many consecutive errors, stopping auto-update system"
                        is_running[] = false
                    end
                end
            end
        finally
            if islocked(timer_lock)
                unlock(timer_lock)
            end
        end
    end
    
    # Start auto-update timer after a short delay to ensure GUI is ready
    @info "Scheduling initial auto-update timer"
    try
        timer_ref[] = Timer(t -> auto_update_timer(), 0.5)
    catch e
        @error "Failed to initialize timer" exception=(e, catch_backtrace())
    end
    controls = vbox(
        hbox(
            vbox(
                shell_count_slider, 
                alpha_slider, 
                v_ratio_slider,
                sigma_ratio_slider,
                boundary_coupling_slider,
                coupling_decay_slider,
                step_size_slider
            ),
            vbox(
                center_sphere_size,
                light_intensity,
                auto_update,
                show_visualization,
                step_button,
                reset_button
            )
        )
    )
    
    # Create plots
    plots = vbox(
        hbox(
            render_plot,
            viz_plot
        )
    )
    
    # Initial visualization - do this carefully with error handling
    @info "Performing initial visualization"
    local render_plot, viz_plot
    try
        render_plot, viz_plot = update_visualization()
    catch e
        @error "Error in initial visualization" exception=(e, catch_backtrace())
        render_plot = plot(title="Initial Render Error", axis=false)
        viz_plot = plot(title="Initial Visualization Error", axis=false)
    end
    
    # Create window layout
    @info "Creating UI layout"
    ui = vbox(
        controls,
        plots
    )
    
    # Create window with robust error handling
    @info "Creating Blink window"
    local w
    try
        # Create window with proper properties
        @info "Initializing Blink window object"
        w = Window(Dict(
            :title => "Matryoshka-Chronon Interactive Explorer",
            :width => 1200,
            :height => 900,
            :resizable => true
        ))
        
        # Setup window close handler to properly clean up resources
        @info "Setting up window close handler"
        Blink.handlers(w)["close"] = (_, _) -> begin
            @info "Window close detected, cleaning up resources"
            # Stop the auto-update system
            is_running[] = false
            
            # Clean up timer
            if timer_ref[] !== nothing
                try
                    close(timer_ref[])
                    timer_ref[] = nothing
                    @info "Timer closed successfully"
                catch e
                    @warn "Error closing timer" exception=e
                end
            end
            
            # Release any held locks
            if islocked(update_lock)
                try unlock(update_lock) catch end
            end
            if islocked(visualization_lock)
                try unlock(visualization_lock) catch end
            end
            
            @info "Resource cleanup completed"
        end
        
        # Attach UI to window with error handling
        @info "Adding UI to window"
        try
            body!(w, ui)
            @info "UI attached successfully"
        catch e
            @error "Failed to attach UI to window" exception=(e, catch_backtrace())
            error("UI attachment failed: $e")
        end
        
        # Ensure window is properly initialized
        @info "Finalizing window initialization"
        try
            # Force a refresh to ensure everything is properly rendered
            Blink.js(w, Blink.JSString("window.location.reload(false)"))
            @info "Window created and initialized successfully"
        catch e
            @warn "Window refresh failed, but continuing" exception=e
        end
    catch e
        @error "Failed to create Blink window" exception=(e, catch_backtrace())
        
        # Clean up any resources before error
        is_running[] = false
        if timer_ref[] !== nothing
            try close(timer_ref[]) catch end
            timer_ref[] = nothing
        end
        
        error("Window creation failed: $e")
    end
    
    # Return window and renderer
    return w, renderer
end

# Main function
function main()
    create_interactive_gui()
end

# Run if executed directly
if abspath(PROGRAM_FILE) == @__FILE__
    main()
end