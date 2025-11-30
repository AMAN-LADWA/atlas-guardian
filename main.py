"""
Simple CLI entrypoint to run the ATLAS pipeline for one object.
"""
import argparse
import json
from agent.atlas_agent import AtlasAgent


def main():
    p = argparse.ArgumentParser(description="Run ATLAS pipeline for an object id")
    p.add_argument("object_id", help="Object identifier (e.g., 2025-AB)")
    args = p.parse_args()

    agent = AtlasAgent()
    report = agent.run_pipeline(args.object_id)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
