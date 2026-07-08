"""
AITL V2 — Phase 2: Agent-Critic Architecture
Orchestrates a dual-agent loop:
  1. ReviewerAgent (Thinker) analyzes history and sets the strategy.
  2. CoderAgent (Worker) executes the strategy.
  3. Reviewer decides when to stop.
"""
import os
import sys
import json
import time
import argparse
import datetime
import traceback
import numpy as np

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from data_loader import get_data
from trainer import execute_agent_code
from reviewer import ReviewerAgent
from coder import CoderAgent

SAFETY_MAX_ITERATIONS = 100
TIMEOUT_PER_ITERATION = 300

def run_experiment(reviewer_model="ollama/ministral:8b", coder_model="ollama/deepseek-coder:6.7b", dataset="tabular", n_samples=10000):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    results_dir = os.path.join(os.path.dirname(__file__), "results")
    os.makedirs(results_dir, exist_ok=True)
    
    # Safe naming
    rev_safe = reviewer_model.replace('/', '_').replace(':', '-')
    cod_safe = coder_model.replace('/', '_').replace(':', '-')
    
    print("=" * 70)
    print("  AEOS Phase 2 — Agent-Critic Architecture")
    print(f"  Reviewer: {reviewer_model} | Coder: {coder_model}")
    print(f"  Dataset: {dataset}")
    print(f"  Started: {timestamp}")
    print("=" * 70)
    
    # ─── Step 1: Load data ───
    X_train, y_train, X_val, y_val, n_features, n_classes, dataset_hint = get_data(
        dataset=dataset, n_samples=n_samples, seed=42
    )
    n_train, n_val = len(X_train), len(X_val)
    
    # ─── Step 2: Initialize agents ───
    # For phase 2, we assume Ollama is mainly used, but litellm handles anything.
    reviewer = ReviewerAgent(model=reviewer_model, dataset_hint=dataset_hint)
    coder = CoderAgent(model=coder_model, dataset_hint=dataset_hint)
    
    # ─── Step 3: The Dual-Agent Loop ───
    all_results = []
    stop_reason = None
    start_time = time.time()
    
    best_loss = float('inf')
    best_acc = 0.0
    best_code = None
    best_iteration = None
    
    iteration = 0
    try:
        while iteration < SAFETY_MAX_ITERATIONS:
            iteration += 1
            iter_start = time.time()
            
            print(f"\n{'='*70}")
            print(f"  ITERATION {iteration}")
            print(f"{'='*70}")
            
            # --- PHASE A: THINKER (REVIEWER) ---
            print("  [Reviewer] Analyzing history and forming directive...")
            directive = reviewer.get_directive(
                n_features, n_classes, n_train, n_val, all_results
            )
            
            if directive.upper() == "STOP" or directive.upper().startswith("STOP"):
                stop_reason = f"Reviewer autonomously stopped at iteration {iteration}"
                print(f"\n  [STOP] Reviewer ordered loop termination.")
                break
                
            print(f"  [Directive] {directive}")
            
            # --- PHASE B: WORKER (CODER) ---
            print("  [Coder] Generating code based on directive...")
            try:
                code = coder.generate_code(
                    n_features=n_features,
                    n_classes=n_classes,
                    n_train=n_train,
                    n_val=n_val,
                    directive=directive,
                    history=all_results,
                    best_code=best_code,
                    timeout=TIMEOUT_PER_ITERATION
                )
            except Exception as e:
                print(f"  [ERROR] Coder LLM call failed: {e}")
                all_results.append({
                    "iteration": iteration,
                    "val_accuracy": 0,
                    "val_loss": 0,
                    "family": "ERROR",
                    "error": str(e),
                    "is_best": False,
                    "directive": directive,
                    "code": ""
                })
                continue
                
            family = coder._detect_model_family(code)
            print(f"  [Model Family] {family}")
            
            # --- PHASE C: EXECUTION ---
            print(f"  [Trainer] Executing code (timeout={TIMEOUT_PER_ITERATION}s)...")
            result, error = execute_agent_code(
                code, X_train, y_train, X_val, y_val, 
                n_classes, timeout=TIMEOUT_PER_ITERATION
            )
            
            iter_time = time.time() - iter_start
            
            if error:
                print(f"  [FAILED] {error[:200]}")
                all_results.append({
                    "iteration": iteration,
                    "val_accuracy": 0,
                    "val_loss": 0,
                    "family": family,
                    "error": error[:500],
                    "is_best": False,
                    "time_seconds": round(iter_time, 1),
                    "directive": directive,
                    "code": code,
                })
                continue
                
            val_acc = result["val_accuracy"]
            val_loss = result["val_loss"]
            
            # Check if best
            is_best = False
            if val_acc > best_acc or (val_acc == best_acc and val_loss < best_loss):
                is_best = True
                best_acc = val_acc
                best_loss = val_loss
                best_code = code
                best_iteration = iteration
                
            marker = " * NEW BEST *" if is_best else ""
            print(f"  [RESULT] Accuracy: {val_acc:.4f} | Loss: {val_loss:.4f} | "
                  f"Family: {family} | Time: {iter_time:.1f}s{marker}")
                  
            all_results.append({
                "iteration": iteration,
                "val_accuracy": val_acc,
                "val_loss": val_loss,
                "family": family,
                "is_best": is_best,
                "time_seconds": round(iter_time, 1),
                "directive": directive,
                "code": code,
            })
            
        else:
            stop_reason = f"Safety cap reached ({SAFETY_MAX_ITERATIONS} iterations)"
            
    except KeyboardInterrupt:
        stop_reason = f"Experiment manually aborted by user at iteration {iteration}"
        print(f"\n  [ABORT] Caught Ctrl+C. Saving partial results...")
    except Exception as e:
        stop_reason = f"Experiment crashed: {e}"
        print(f"\n  [ERROR] {traceback.format_exc()}")
        
    total_time = time.time() - start_time
    
    # ─── Step 4: Save results ───
    print("\n" + "=" * 70)
    print("  EXPERIMENT COMPLETE")
    print("=" * 70)
    print(f"  Stop reason: {stop_reason}")
    print(f"  Total iterations: {iteration}")
    print(f"  Best accuracy: {best_acc:.4f} at iteration {best_iteration}")
    
    run_data = {
        "run_id": timestamp,
        "reviewer_model": reviewer_model,
        "coder_model": coder_model,
        "dataset": dataset,
        "best_accuracy": best_acc,
        "best_iteration": best_iteration,
        "total_iterations": iteration,
        "stop_reason": stop_reason,
        "total_time_seconds": round(total_time, 1),
        "iterations": all_results,
    }
    
    json_path = os.path.join(results_dir, f"exp2_{rev_safe}_{cod_safe}_{dataset}_{timestamp}.json")
    with open(json_path, "w") as f:
        json.dump(run_data, f, indent=2)
    print(f"\n  [Saved] Results: {json_path}")
    
    return run_data

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AEOS Phase 2 — Agent-Critic Architecture")
    parser.add_argument("--reviewer", default="ollama/ministral:14b", help="Reviewer LLM")
    parser.add_argument("--coder", default="ollama/deepseek-v2:16b", help="Coder LLM")
    parser.add_argument("--dataset", choices=["tabular", "text", "vision"], default="tabular")
    parser.add_argument("--samples", type=int, default=10000)
    args = parser.parse_args()
    
    run_experiment(
        reviewer_model=args.reviewer,
        coder_model=args.coder,
        dataset=args.dataset,
        n_samples=args.samples
    )
