from assistant import BusinessInsightsAssistant
import os
import json

def save_report(insights, filename="data/sample_report.txt"):
    """Save insights to a file."""
    with open(filename, "w") as f:
        f.write(json.dumps(insights, indent=2))
    print(f"Report saved to {filename}")

def main():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not set.")
        return

    assistant = BusinessInsightsAssistant(api_key)
    print("Welcome to the AI Business Insights Assistant!")
    print("Type 'exit' to quit.")

    while True:
        query = input("Enter your business query: ")
        if query.lower() == "exit":
            break
        
        insights = assistant.process_query(query)
        metrics = assistant.evaluate_response(query, insights)
        print("Evaluation Metrics:", json.dumps(metrics, indent=2))
        print("\nGenerated Insights:")
        print(json.dumps(insights, indent=2))
        
        save = input("\nSave report? (y/n): ")
        if save.lower() == "y":
            save_report(insights)

if __name__ == "__main__":
    main()