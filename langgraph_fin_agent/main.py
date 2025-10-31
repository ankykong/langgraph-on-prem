import argparse
import asyncio
import sys
from typing import Any

from langchain_core.messages import HumanMessage

from .graph import build_app

from arize.otel import register, Transport, Endpoint
from openinference.instrumentation.langchain import LangChainInstrumentor
import os
from dotenv import load_dotenv
load_dotenv()


tracer_provider = register(
    space_id=os.getenv("ARIZE_SPACE_ID"),
    api_key=os.getenv("ARIZE_API_KEY"),
    project_name=os.getenv("ARIZE_PROJECT_NAME", "langgraph-fin-agent"),
    endpoint=os.getenv("ARIZE_ENDPOINT", Endpoint.ARIZE),
    transport = os.getenv("ARIZE_TRANSPORT", Transport.GRPC),
)

LangChainInstrumentor().instrument(tracer_provider=tracer_provider)


async def main_interactive():
    """Start an interactive session with the Finance Assistant."""
    print("Welcome to the Financial Assistant powered by LangGraph agents!")
    print("You can ask questions about stocks, companies, and financial data.")
    print(
        "The assistant has access to public company data and can browse the web for more information if needed."
    )
    print("Type 'exit' to end the session.")

    app = build_app()
    config = {"configurable": {"thread_id": "1"}}
    while True:
        query = input("\nYour question: ").strip()
        if query.lower() == "exit":
            print("Thank you for using the Finance Assistant. Goodbye!")
            break
        inputs = {"messages": [HumanMessage(content=query)]}
        async for chunk in app.astream(inputs, config, stream_mode="values"):
            chunk["messages"][-1].pretty_print()
        print("=" * 80)


async def main_eval():
    app = build_app()

    async def runnable(data: Any):
        inputs = {"messages": [HumanMessage(content=data)]}
        config = {"configurable": {"thread_id": "1"}}
        async for chunk in app.astream(inputs, config, stream_mode="values"):
            chunk["messages"][-1].pretty_print()
        return chunk["messages"][-1].content

def main():
    parser = argparse.ArgumentParser(
        description="Financial Assistant powered by LangGraph agents"
    )
    parser.add_argument(
        "--interactive", "-i", action="store_true", help="Run in interactive mode"
    )
    parser.add_argument("--eval", "-e", action="store_true", help="Run evaluation mode")

    args = parser.parse_args()

    if args.interactive and args.eval:
        print("Error: Cannot specify both interactive and eval modes")
        sys.exit(1)
    elif args.interactive:
        asyncio.run(main_interactive())
    elif args.eval:
        asyncio.run(main_eval())
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
