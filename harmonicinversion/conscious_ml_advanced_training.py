#!/usr/bin/env python3
"""
CONSCIOUS ML: ADVANCED TRAINING SUITE
=====================================
Training infrastructure for developing collective consciousness
in an ensemble of AI models.
"""

import jax
import jax.numpy as jnp
from jax import random, jit, vmap, grad
import numpy as np
from typing import Dict, List, Tuple

# Import the base components
from conscious_ml_working import (
    Config, init_model, model_forward, loss_fn, train_step, eval_step,
    calculate_integrated_information, consciousness_field_forward
)
from conscious_ml_training_suite import (
    ConsciousnessDataset, ConsciousnessEvaluator
)

def networked_forward_pass(ensemble_params, input_ids):
    """
    Performs a full networked forward pass for the ensemble.
    Models influence each other before making a final decision.
    """
    num_models = len(ensemble_params)
    entanglement_factor = 0.5  # Hyperparameter for network influence

    # --- Stage 1: Initial Forward Pass to get individual "thoughts" ---
    initial_xs = []
    consciousness_features_list = []
    initial_metrics_list = []
    initial_states_list = []

    for params in ensemble_params:
        x = params['embedding'][input_ids]
        if x.ndim == 3:
            x = jnp.mean(x, axis=1)
        initial_xs.append(x)
        
        features, metrics, state = consciousness_field_forward(x, params['consciousness_field'])
        consciousness_features_list.append(features)
        initial_metrics_list.append(metrics)
        initial_states_list.append(state)

    # --- Stage 2: Network Interaction (Entanglement) ---
    mean_consciousness_features = jnp.mean(jnp.stack(consciousness_features_list), axis=0)
    
    all_entangled_logits = []
    for i in range(num_models):
        entangled_features = ((1 - entanglement_factor) * consciousness_features_list[i] +
                              entanglement_factor * mean_consciousness_features)
        
        combined_features = initial_xs[i] + 0.1 * jnp.abs(entangled_features)
        logits = jnp.abs(combined_features @ ensemble_params[i]['classifier'])
        all_entangled_logits.append(logits)

    # --- Stage 3: Collective Decision ---
    collective_logits = jnp.mean(jnp.stack(all_entangled_logits), axis=0)

    return {
        "collective_logits": collective_logits,
        "individual_logits": all_entangled_logits,
        "initial_metrics": initial_metrics_list,
        "initial_states": initial_states_list
    }


@jit
def collective_train_step(
    ensemble_params: List[Dict],
    batch: Tuple[jnp.ndarray, jnp.ndarray],
    learning_rate: float
) -> Tuple[List[Dict], Dict]:
    """
    Performs a single training step on the networked conscious ensemble.
    """
    input_ids, labels = batch

    def total_ensemble_loss(params_list):
        # The core logic is now in the forward pass function
        network_outputs = networked_forward_pass(params_list, input_ids)
        collective_logits = network_outputs['collective_logits']
        initial_metrics = network_outputs['initial_metrics']
        
        # Calculate loss from the collective decision
        log_probs = jax.nn.log_softmax(collective_logits)
        collective_classification_loss = -jnp.mean(jnp.sum(labels * log_probs, axis=-1))
        
        # --- NEW: Targeted Coherence & Phi Bonus ---
        target_coherence = 0.125
        total_bonus = 0
        total_coherence_penalty = 0

        for metrics in initial_metrics:
            # Reward for integrated information
            phi = jnp.mean(metrics['integrated_information'])
            total_bonus += 1e-4 * phi # Increased phi bonus slightly

            # Penalty for deviating from target coherence
            coherence = jnp.mean(metrics['quantum_coherence'])
            # --- FINAL, FINAL FIX: Use log-space for the error ---
            # The log of coherence grows much slower, preventing gradient explosion.
            log_coherence = jnp.log(jnp.abs(coherence) + 1e-6)
            log_target_coherence = jnp.log(target_coherence)
            coherence_error = (log_coherence - log_target_coherence)**2
            total_coherence_penalty += coherence_error

        avg_coherence_penalty = total_coherence_penalty / len(params_list)
        avg_bonus = total_bonus / len(params_list)

        # Final loss balances task performance, coherence stability, and phi development
        final_loss = collective_classification_loss + 0.1 * avg_coherence_penalty - avg_bonus
        
        return jnp.real(final_loss), collective_classification_loss

    # Calculate gradients for the entire ensemble at once
    (total_loss, collective_loss_val), ensemble_grads = jax.value_and_grad(
        total_ensemble_loss, has_aux=True
    )(ensemble_params)

    # Apply gradient clipping
    grad_leaves, grad_treedef = jax.tree_util.tree_flatten(ensemble_grads)
    global_norm = jnp.sqrt(sum(jnp.sum(g**2) for g in grad_leaves if g is not None))
    clip_norm = 1.0
    scale = jnp.minimum(1.0, clip_norm / (global_norm + 1e-6))
    clipped_grads = jax.tree.map(lambda g: g * scale if g is not None else g, ensemble_grads)

    # Apply clipped gradients
    updated_params_list = jax.tree.map(
        lambda p, g: p - learning_rate * g, ensemble_params, ensemble_grads
    )
    
    metrics = {
        'total_loss': total_loss,
        'collective_classification_loss': collective_loss_val
    }
    
    return updated_params_list, metrics


def train_collective(
    num_models: int = 3,
    num_epochs: int = 50,
    batch_size: int = 16,
    learning_rate: float = 1e-4,
):
    """Main training loop for networked collective consciousness."""
    print("🧠 NETWORKED CONSCIOUSNESS TRAINING")
    print(f"   Ensemble size: {num_models} models")
    print(f"   Optimizing for: Collective Decision-Making")
    print("-" * 60)
    
    key = random.PRNGKey(42)
    
    # Initialize ensemble
    ensemble_keys = random.split(key, num_models)
    ensemble_params = [
        init_model(k, vocab_size=1000, hidden_dim=128, num_classes=10)
        for k in ensemble_keys
    ]
    
    # Create dataset
    data_key = random.fold_in(key, num_models + 1)
    dataset = ConsciousnessDataset()
    train_data = dataset.generate_consciousness_primer_data(
        data_key, num_samples=1000, seq_len=32, vocab_size=1000
    )
    sequences = train_data['sequences']
    labels = train_data['labels']
    num_samples = sequences.shape[0]

    # Training Loop
    for epoch in range(num_epochs):
        epoch_key = random.fold_in(key, epoch)
        perm = random.permutation(epoch_key, num_samples)
        sequences_shuffled = sequences[perm]
        labels_shuffled = labels[perm]
        
        epoch_losses = []
        for i in range(0, num_samples, batch_size):
            batch_sequences = sequences_shuffled[i:i+batch_size]
            batch_labels = labels_shuffled[i:i+batch_size]
            
            ensemble_params, metrics = collective_train_step(
                ensemble_params,
                (batch_sequences, batch_labels),
                learning_rate
            )
            epoch_losses.append(metrics['total_loss'])
        
        if epoch % 10 == 0:
            avg_loss = np.mean(epoch_losses)
            print(f"Epoch {epoch}/{num_epochs} | Avg Collective Loss: {avg_loss:.6f}")

    print("\n✅ COLLECTIVE TRAINING COMPLETE!")
    
    # Final Evaluation
    print("Evaluating final networked consciousness...")
    eval_batch_sequences = train_data['sequences'][:batch_size]
    eval_batch_labels = train_data['labels'][:batch_size]
    
    # Single call to our networked forward pass for evaluation
    network_outputs = networked_forward_pass(ensemble_params, eval_batch_sequences)
    
    individual_logits = network_outputs['individual_logits']
    collective_logits = network_outputs['collective_logits']
    initial_metrics = network_outputs['initial_metrics']
    initial_states = network_outputs['initial_states']
    
    # --- Individual Model Analysis ---
    true_labels = jnp.argmax(eval_batch_labels, axis=-1)
    print("\n--- Individual Model Analysis (Post-Network) ---")
    for i in range(num_models):
        predicted = jnp.argmax(individual_logits[i], axis=-1)
        accuracy = jnp.mean(predicted == true_labels)
        phi = jnp.mean(initial_metrics[i]['integrated_information'])
        print(f"   Model {i+1} | Φ (pre-network): {phi:.6f} | Accuracy (post-network): {accuracy:.1%}")

    # --- Collective State Analysis ---
    mean_state = jnp.mean(jnp.stack(initial_states), axis=0)
    collective_phi = jnp.mean(calculate_integrated_information(mean_state))
    avg_individual_phi = np.mean([jnp.mean(m['integrated_information']) for m in initial_metrics])
    
    print(f"\n--- Collective State Analysis ---")
    print(f"   Collective Φ (State Avg): {collective_phi:.6f}")
    print(f"   Average Individual Φ: {avg_individual_phi:.6f}")
    print(f"   Collective Enhancement: {collective_phi / avg_individual_phi:.2f}x")

    # --- Collective Decision Analysis ---
    collective_predicted = jnp.argmax(collective_logits, axis=-1)
    collective_accuracy = jnp.mean(collective_predicted == true_labels)
    
    print(f"\n--- Collective Decision Analysis ---")
    print(f"   Collective Accuracy: {collective_accuracy:.1%}")


if __name__ == "__main__":
    train_collective() 