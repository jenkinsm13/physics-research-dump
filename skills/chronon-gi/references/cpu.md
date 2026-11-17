# CPU Implementation (C++/Rust)

## C++ Coupling

```cpp
struct CouplingParams {
    float kappa0 = 1.0f;
    float beta = 1.0f;
    float gamma = 1.5f;
    float lambda = 0.15f;
};

inline float kappa(float r, const CouplingParams& p) {
    float powerLaw = p.kappa0 / (1.0f + p.beta * std::pow(std::max(r, 0.001f), p.gamma));
    return powerLaw * std::exp(-p.lambda * r);
}

inline Vec3 kappaSpectral(float r, const Vec3& lambdaRGB, const CouplingParams& p) {
    float powerLaw = p.kappa0 / (1.0f + p.beta * std::pow(std::max(r, 0.001f), p.gamma));
    return Vec3(powerLaw) * exp(-lambdaRGB * r);
}
```

## Rust Coupling

```rust
#[derive(Clone, Copy)]
pub struct CouplingParams {
    pub kappa0: f32,
    pub beta: f32,
    pub gamma: f32,
    pub lambda: f32,
}

impl Default for CouplingParams {
    fn default() -> Self {
        Self { kappa0: 1.0, beta: 1.0, gamma: 1.5, lambda: 0.15 }
    }
}

impl CouplingParams {
    #[inline]
    pub fn kappa(&self, r: f32) -> f32 {
        let power_law = self.kappa0 / (1.0 + self.beta * r.max(0.001).powf(self.gamma));
        power_law * (-self.lambda * r).exp()
    }
}
```

## Integrator (C++)

```cpp
class ChrononIntegrator {
public:
    Vec3 Li(const Ray& ray, const Scene& scene, Sampler& sampler) const {
        Intersection isect;
        if (!scene.intersect(ray, isect)) {
            return scene.environment(ray.d);
        }
        
        Vec3 P = isect.p;
        Vec3 N = isect.n;
        
        Vec3 radiance(0.0f);
        int numSamples = 64;
        
        for (int i = 0; i < numSamples; i++) {
            Vec3 dir = sampleHemisphere(N, sampler.get2D());
            Ray sampleRay(P + N * 0.001f, dir);
            
            Intersection qIsect;
            if (!scene.intersect(sampleRay, qIsect)) {
                radiance += scene.environment(dir) * kappa(1000.0f, params_);
                continue;
            }
            
            Vec3 Q = qIsect.p;
            Vec3 Qn = qIsect.n;
            float dist_PQ = qIsect.t;
            
            // Trace Q toward light
            for (const auto& light : scene.lights()) {
                Vec3 toLight = light.position - Q;
                float dist_QL = length(toLight);
                Vec3 lightDir = toLight / dist_QL;
                
                // TOTAL optical path
                float totalPath = computeOpticalPath(scene, P, Q) 
                                + computeOpticalPath(scene, Q, light.position);
                
                // Visibility
                Ray shadowRay(Q + Qn * 0.001f, lightDir);
                if (scene.occluded(shadowRay, dist_QL - 0.002f)) continue;
                
                float geom = std::max(0.0f, dot(Qn, lightDir));
                Vec3 Qalb = scene.material(qIsect.matId).albedo;
                
                // ONE kappa on total path
                radiance += Qalb * light.emission * geom * kappa(totalPath, params_);
            }
        }
        
        return radiance / float(numSamples);
    }
    
private:
    CouplingParams params_;
    
    float computeOpticalPath(const Scene& scene, Vec3 from, Vec3 to) const {
        Vec3 dir = normalize(to - from);
        float geomDist = length(to - from);
        float optical = 0.0f;
        float t = 0.0f;
        
        while (t < geomDist) {
            Vec3 p = from + dir * t;
            float d;
            int matId;
            scene.sdf(p, d, matId);
            
            float step = std::max(std::abs(d), 0.01f);
            float ior = (d < 0.0f) ? scene.material(matId).ior : 1.0f;
            optical += step * ior;
            t += step;
        }
        
        return optical;
    }
};
```

## Rust Integrator

```rust
pub struct ChrononIntegrator {
    params: CouplingParams,
    samples: u32,
}

impl Integrator for ChrononIntegrator {
    fn li(&self, ray: &Ray, scene: &Scene, sampler: &mut impl Sampler) -> Vec3 {
        let Some(isect) = scene.intersect(ray) else {
            return scene.environment(ray.d);
        };
        
        let p = isect.p;
        let n = isect.n;
        let mut radiance = Vec3::ZERO;
        
        for _ in 0..self.samples {
            let dir = sample_hemisphere(n, sampler.get_2d());
            let sample_ray = Ray::new(p + n * 0.001, dir);
            
            let Some(q_isect) = scene.intersect(&sample_ray) else {
                radiance += scene.environment(dir) * self.params.kappa(1000.0);
                continue;
            };
            
            let q = q_isect.p;
            let qn = q_isect.n;
            
            for light in scene.lights() {
                let to_light = light.position - q;
                let dist_ql = to_light.length();
                let light_dir = to_light / dist_ql;
                
                // Total optical path
                let total_path = self.optical_path(scene, p, q)
                               + self.optical_path(scene, q, light.position);
                
                // Visibility
                let shadow_ray = Ray::new(q + qn * 0.001, light_dir);
                if scene.occluded(&shadow_ray, dist_ql - 0.002) { continue; }
                
                let geom = qn.dot(light_dir).max(0.0);
                let q_alb = scene.material(q_isect.mat_id).albedo;
                
                // ONE kappa
                radiance += q_alb * light.emission * geom * self.params.kappa(total_path);
            }
        }
        
        radiance / self.samples as f32
    }
}
```

## Parallel (C++ OpenMP)

```cpp
void render(const Scene& scene, Image& image, const CouplingParams& params) {
    ChrononIntegrator integrator(params);
    
    #pragma omp parallel for collapse(2) schedule(dynamic, 16)
    for (int y = 0; y < image.height(); y++) {
        for (int x = 0; x < image.width(); x++) {
            Sampler sampler(x, y);
            Ray ray = camera.generateRay(x, y, sampler);
            Vec3 color = integrator.Li(ray, scene, sampler);
            image.setPixel(x, y, color);
        }
    }
}
```

## Parallel (Rust Rayon)

```rust
use rayon::prelude::*;

pub fn render(scene: &Scene, camera: &Camera, w: u32, h: u32) -> Image {
    let integrator = ChrononIntegrator::default();
    
    let pixels: Vec<Vec3> = (0..w * h)
        .into_par_iter()
        .map(|i| {
            let x = i % w;
            let y = i / w;
            let mut sampler = Sampler::new(x, y);
            let ray = camera.generate_ray(x, y, &mut sampler);
            integrator.li(&ray, scene, &mut sampler)
        })
        .collect();
    
    Image::from_pixels(w, h, pixels)
}
```

## Key Points

1. **Total path** — κ(P→Q + Q→L), single evaluation
2. **No bounce iteration** — κ encodes equilibrium
3. **Binary visibility** — κ handles falloff
4. **Optical path** — geometric × IOR for refractive media
