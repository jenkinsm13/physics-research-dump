# Compute Shader Implementation (HLSL/WGSL)

## HLSL Coupling

```hlsl
cbuffer Params : register(b0) {
    float kappa0;  // 1.0
    float beta;    // 1.0
    float gamma;   // 1.5
    float lambda;  // 0.15
};

float kappa(float r) {
    float powerLaw = kappa0 / (1.0 + beta * pow(max(r, 0.001), gamma));
    return powerLaw * exp(-lambda * r);
}

float3 kappaSpectral(float r, float3 lambdaRGB) {
    float powerLaw = kappa0 / (1.0 + beta * pow(max(r, 0.001), gamma));
    return float3(powerLaw, powerLaw, powerLaw) * exp(-lambdaRGB * r);
}
```

## WGSL Coupling

```wgsl
struct Params {
    kappa0: f32,
    beta: f32,
    gamma: f32,
    lambda: f32,
}

@group(0) @binding(0) var<uniform> params: Params;

fn kappa(r: f32) -> f32 {
    let powerLaw = params.kappa0 / (1.0 + params.beta * pow(max(r, 0.001), params.gamma));
    return powerLaw * exp(-params.lambda * r);
}
```

## Compute Kernel

```hlsl
RWTexture2D<float4> output : register(u0);

[numthreads(8, 8, 1)]
void CSMain(uint3 DTid : SV_DispatchThreadID) {
    float2 uv = float2(DTid.xy) / float2(width, height);
    
    float3 ro, rd;
    generateRay(uv, ro, rd);
    
    float t = raymarch(ro, rd);
    if (t < 0.0) {
        output[DTid.xy] = float4(0, 0, 0, 1);
        return;
    }
    
    float3 P = ro + rd * t;
    float3 N = sceneNormal(P);
    
    float3 radiance = computeRadiance(P, N);
    output[DTid.xy] = float4(radiance, 1.0);
}

float3 computeRadiance(float3 P, float3 N) {
    float3 total = float3(0, 0, 0);
    
    for (int i = 0; i < NUM_SAMPLES; i++) {
        float3 dir = hemisphereDir(N, i, NUM_SAMPLES);
        
        float dist;
        float3 Q;
        if (!traceRay(P + N * 0.001, dir, dist, Q)) continue;
        
        float3 Qn = sceneNormal(Q);
        float3 Qalb = getMaterialColor(Q);
        
        // Path to light
        float3 toLight = lightPos - Q;
        float lightDist = length(toLight);
        float3 lightDir = toLight / lightDist;
        
        // TOTAL path: P→Q→Light
        float totalPath = dist + lightDist;
        
        float vis = visibility(Q + Qn * 0.001, lightDir, lightDist);
        float geom = max(0.0, dot(Qn, lightDir));
        
        // ONE kappa
        total += Qalb * lightEmit * geom * kappa(totalPath) * vis;
    }
    
    return total / float(NUM_SAMPLES);
}
```

## Parallel Accumulation

```hlsl
// Each thread handles one sample direction
[numthreads(64, 1, 1)]
void AccumulateSamples(uint3 DTid : SV_DispatchThreadID) {
    uint pixelIdx = DTid.x / SAMPLES_PER_PIXEL;
    uint sampleIdx = DTid.x % SAMPLES_PER_PIXEL;
    
    float3 P = positions[pixelIdx];
    float3 N = normals[pixelIdx];
    
    float3 dir = hemisphereDir(N, sampleIdx, SAMPLES_PER_PIXEL);
    
    float dist;
    float3 Q;
    if (!traceRay(P + N * 0.001, dir, dist, Q)) {
        sampleBuffer[DTid.x] = float4(0, 0, 0, 0);
        return;
    }
    
    float totalPath = computeTotalPathToLight(P, Q);
    float3 contrib = computeContribution(Q) * kappa(totalPath);
    
    sampleBuffer[DTid.x] = float4(contrib, 1.0);
}

// Reduction pass
[numthreads(256, 1, 1)]
void ReduceSamples(uint3 DTid : SV_DispatchThreadID) {
    uint pixel = DTid.x;
    float3 sum = float3(0, 0, 0);
    
    for (uint i = 0; i < SAMPLES_PER_PIXEL; i++) {
        sum += sampleBuffer[pixel * SAMPLES_PER_PIXEL + i].rgb;
    }
    
    output[pixelCoords[pixel]] = float4(sum / SAMPLES_PER_PIXEL, 1);
}
```

## Optical Path Computation

```hlsl
float computeOpticalPath(float3 from, float3 to) {
    float3 dir = normalize(to - from);
    float geomDist = length(to - from);
    float optical = 0.0;
    float t = 0.0;
    
    [loop]
    for (int i = 0; i < 64; i++) {
        float3 p = from + dir * t;
        float d = sceneSDF(p);
        float step = max(abs(d), 0.01);
        
        float ior = (d < 0.0) ? getMaterialIOR(p) : 1.0;
        optical += step * ior;
        
        t += step;
        if (t >= geomDist) break;
    }
    
    return optical;
}
```

## Key Points

1. **Total path length** — κ(P→Q + Q→L), not κ(P→Q) × κ(Q→L)
2. **No bounce iteration** — κ is the equilibrium
3. **Binary visibility** — κ handles all falloff
4. **Per-material λ** — different absorption, same κ structure
