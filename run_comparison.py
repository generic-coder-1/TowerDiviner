"""Compare the built-in agents.   Usage: python run_comparison.py --runs 500"""
import argparse

from agents import BeamSearchAgent, GreedyAgent, RandomAgent, SpecialRandomAgent, RandomGreedyAgent
from evaluation import compare_agents
from game.floors import build_tower


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs", type=int, default=500, help="runs per stochastic agent")
    parser.add_argument("--seed", type=int, default=0, help="first seed")
    parser.add_argument("--beam-width", type=int, default=100)
    args = parser.parse_args()

    # Add your own agents to this list.
    agents = [
        RandomAgent(),
        SpecialRandomAgent(),
        GreedyAgent(),
        RandomGreedyAgent(),
        BeamSearchAgent(beam_width=10),
        BeamSearchAgent(beam_width=args.beam_width),
    ]

    comparison = compare_agents(agents, n_runs=args.runs, base_seed=args.seed)
    print(comparison.report())

    best = max(comparison.reports.values(), key=lambda r: r.best_score).best_run
    print(f"Highest-scoring run: {best.agent_name} (seed {best.seed}), "
          f"won={best.won}, {best.steps} steps")
    build_tower().print_path_with_annotations(best.path)


    fastest = min(comparison.reports.values(), key=lambda r: r.shortest_win).shortest_run
    print(f"Fastest run: {fastest.agent_name} (seed {fastest.seed}), "
          f"{fastest.steps} steps")
    build_tower().print_path_with_annotations(fastest.path)


if __name__ == "__main__":
    main()
