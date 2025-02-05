import json

from modules.query_processor import QueryProcessor


def main():
    # Load JSON Config
    config_path = "config/recommender_config.json"
    with open(config_path, "r") as f:
        config = json.load(f)

    # Ensure there is a query in the config
    if not config.get("query"):
        print("⚠️ No query found in config file. Please add a query before running.")
        return

    # Run Recommender System
    query_processor = QueryProcessor(config_path=config_path)
    query_processor.generate_recommendation_report()

if __name__ == "__main__":
    main()
