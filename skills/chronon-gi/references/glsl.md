# GLSL Implementation

## Coupling Function

```glsl
uniform float u_kappa0;  // 1.0
uniform float u_beta;    // 1.0
uniform float u_gamma;   // 1.5
uniform float u_lambda;  // 0.15

float kappa(float r) {
    float powerLaw = u_kappa0 / (1.0 + u_beta * pow(max(r, 0.001), u_gamma));
    return powerLaw * exp(-u_lambda * r);
}
```

## Spectral Coupling

```glsl
vec3 kappaSpectral(float r, vec3 lambdaRGB) {
    float powerLaw = u_kappa0 / (1.0 + u_beta * pow(max(r, 0.001), u_gamma));
    return vec3(powerLaw) * exp(-lambdaRGB * r);
}
```

## Refraction (Snell's Law)

Refraction changes RAY DIRECTION. This is separate from optical distance.

```glsl
// Returns refracted direction, or reflected if TIR
vec3 refractRay(vec3 I, vec3 N, float eta) {
    float cosI = -dot(I, N);
    float sin2T = eta * eta * (1.0 - cosI * cosI);
    if (sin2T > 1.0) {
        return reflect(I, N);  // Total internal reflection
    }
    float cosT = sqrt(1.0 - sin2T);
    return eta * I + (eta * cosI - cosT) * N;
}

// Fresnel reflectance (Schlick)
float fresnel(float cosI, float ior) {
    float r0 = (1.0 - ior) / (1.0 + ior);
    r0 *= r0;
    float x = 1.0 - cosI;
    return r0 + (1.0 - r0) * x * x * x * x * x;
}
```

## Tracing Through Refractive Media

```glsl
struct PathResult {
    vec3 endPoint;
    vec3 endDir;
    float opticalLength;
    bool valid;
};

// Trace ray through scene, handling refraction at interfaces
PathResult traceWithRefraction(vec3 origin, vec3 dir, float maxDist) {
    PathResult result;
    result.opticalLength = 0.0;
    result.valid = false;
    
    vec3 pos = origin;
    vec3 ray = dir;
    float traveled = 0.0;
    
    for (int bounce = 0; bounce < 8; bounce++) {
        // March to next surface
        float t = 0.01;
        for (int i = 0; i < 64; i++) {
            float d = sceneSDF(pos + ray * t);
            if (abs(d) < 0.001) break;
            
            // Accumulate optical distance
            float ior = (d < 0.0) ? getMaterialIOR(getMaterialID(pos + ray * t)) : 1.0;
            float step = max(abs(d), 0.01);
            result.opticalLength += step * ior;
            
            t += step;
            traveled += step;
            if (traveled > maxDist) {
                result.valid = false;
                return result;
            }
        }
        
        vec3 hitP = pos + ray * t;
        vec3 hitN = sceneNormal(hitP);
        int matID = getMaterialID(hitP);
        
        // Is this material refractive?
        if (!isRefractive(matID)) {
            result.endPoint = hitP;
            result.endDir = ray;
            result.valid = true;
            return result;
        }
        
        // Refract through interface
        float ior = getMaterialIOR(matID);
        bool entering = dot(ray, hitN) < 0.0;
        float eta = entering ? (1.0 / ior) : ior;
        vec3 N = entering ? hitN : -hitN;
        
        ray = refractRay(ray, N, eta);
        pos = hitP - N * 0.02;  // Step slightly past interface
    }
    
    return result;
}
```

## Unified Transport with Refraction

```glsl
vec3 computeRadiance(vec3 P, vec3 N) {
    vec3 total = vec3(0.0);
    int numSamples = 64;
    
    for (int i = 0; i < numSamples; i++) {
        // Hemisphere sampling
        float theta = float(i) * PI * 2.0 * 0.618034;
        float cosEl = (float(i) + 0.5) / float(numSamples);
        float sinEl = sqrt(1.0 - cosEl * cosEl);
        vec3 localDir = vec3(sinEl * cos(theta), cosEl, sinEl * sin(theta));
        
        vec3 T = abs(N.y) < 0.99 ? normalize(cross(N, vec3(0,1,0))) : vec3(1,0,0);
        vec3 B = cross(N, T);
        vec3 dir = T * localDir.x + N * localDir.y + B * localDir.z;
        
        // Trace with refraction
        PathResult path = traceWithRefraction(P + N * 0.02, dir, 100.0);
        if (!path.valid) continue;
        
        vec3 Q = path.endPoint;
        vec3 Qn = sceneNormal(Q);
        vec3 Qalb = getMaterialColor(getMaterialID(Q));
        
        // Now trace Q → Light (also with refraction)
        vec3 toLight = u_lightPos - Q;
        float lightDist = length(toLight);
        vec3 lightDir = toLight / lightDist;
        
        PathResult lightPath = traceWithRefraction(Q + Qn * 0.02, lightDir, lightDist);
        
        // Total optical distance = P→Q path + Q→Light path
        float totalOptical = path.opticalLength + lightPath.opticalLength;
        
        float vis = lightPath.valid ? 1.0 : 0.0;
        float geom = max(0.0, dot(Qn, lightDir));
        
        // ONE kappa on total optical path
        total += Qalb * u_lightEmit * geom * kappa(totalOptical) * vis;
    }
    
    return total / float(numSamples);
}
```

## Key Points

**Refraction:** Changes ray DIRECTION (geometric path shape)
**Optical distance:** Changes coupling STRENGTH (κ evaluation)

Both are needed. Refraction determines where light goes. κ determines how strongly it couples.

```glsl
// WRONG — ignores refraction geometry
float wrong = kappa(straightLineDistance);

// RIGHT — optical distance along refracted path
float right = kappa(opticalDistanceAlongRefractedPath);
```
