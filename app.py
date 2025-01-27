# # Copyright (c) Microsoft Corporation. All rights reserved.
# # Licensed under the MIT License.

# import sys
# import traceback
# from datetime import datetime
# from http import HTTPStatus
# import os

# from aiohttp import web
# from aiohttp.web import Request, Response, json_response
# from botbuilder.core import (
#     TurnContext,
# )
# from botbuilder.core.integration import aiohttp_error_middleware
# from botbuilder.integration.aiohttp import CloudAdapter, ConfigurationBotFrameworkAuthentication
# from botbuilder.schema import Activity, ActivityTypes

# from bots import EchoBot
# from config import DefaultConfig

# CONFIG = DefaultConfig()

# # Create adapter.
# # See https://aka.ms/about-bot-adapter to learn more about how bots work.
# ADAPTER = CloudAdapter(ConfigurationBotFrameworkAuthentication(CONFIG))


# # Catch-all for errors.
# async def on_error(context: TurnContext, error: Exception):
#     # This check writes out errors to console log .vs. app insights.
#     # NOTE: In production environment, you should consider logging this to Azure
#     #       application insights.
#     print(f"\n [on_turn_error] unhandled error: {error}", file=sys.stderr)
#     traceback.print_exc()

#     # Send a message to the user
#     await context.send_activity("The bot encountered an error or bug.")
#     await context.send_activity(
#         "To continue to run this bot, please fix the bot source code."
#     )
#     # Send a trace activity if we're talking to the Bot Framework Emulator
#     if context.activity.channel_id == "emulator":
#         # Create a trace activity that contains the error object
#         trace_activity = Activity(
#             label="TurnError",
#             name="on_turn_error Trace",
#             timestamp=datetime.utcnow(),
#             type=ActivityTypes.trace,
#             value=f"{error}",
#             value_type="https://www.botframework.com/schemas/error",
#         )
#         # Send a trace activity, which will be displayed in Bot Framework Emulator
#         await context.send_activity(trace_activity)


# ADAPTER.on_turn_error = on_error

# # Create the Bot
# BOT = EchoBot()


# # Listen for incoming requests on /api/messages
# async def messages(req: Request) -> Response:
#     return await ADAPTER.process(req, BOT)


# APP = web.Application(middlewares=[aiohttp_error_middleware])
# APP.router.add_post("/api/messages", messages)

# if __name__ == "__main__":
#     try:
#         web.run_app(APP, host="ust-python.azurewebsites.net", port=CONFIG.PORT)
#     except Exception as error:
#         raise error






# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import sys
import traceback
import asyncio
from datetime import datetime
from http import HTTPStatus
import os

from aiohttp import web
from aiohttp.web import Request, Response, json_response
from botbuilder.core import TurnContext
from botbuilder.core.integration import aiohttp_error_middleware
from botbuilder.integration.aiohttp import CloudAdapter, ConfigurationBotFrameworkAuthentication
from botbuilder.schema import Activity, ActivityTypes

from bots import EchoBot
from config import DefaultConfig

CONFIG = DefaultConfig()

# Create adapter with authentication
ADAPTER = CloudAdapter(ConfigurationBotFrameworkAuthentication(CONFIG))

# Global error handler
async def on_error(context: TurnContext, error: Exception):
    print(f"\n [on_turn_error] Unhandled error: {error}", file=sys.stderr)
    traceback.print_exc()

    # Send error message to user
    await context.send_activity("The bot encountered an error or bug.")
    await context.send_activity("Please try again later or contact support.")

    # Send a trace activity for debugging in Bot Framework Emulator
    if context.activity.channel_id == "emulator":
        trace_activity = Activity(
            label="TurnError",
            name="on_turn_error Trace",
            timestamp=datetime.utcnow(),
            type=ActivityTypes.trace,
            value=f"{error}",
            value_type="https://www.botframework.com/schemas/error",
        )
        await context.send_activity(trace_activity)

# Assign error handler to adapter
ADAPTER.on_turn_error = on_error

# Create bot instance
BOT = EchoBot()

# API endpoint for bot messages
async def messages(req: Request) -> Response:
    return await ADAPTER.process(req, BOT)

# Initialize aiohttp application
APP = web.Application(middlewares=[aiohttp_error_middleware])
APP.router.add_post("/api/messages", messages)

if __name__ == "__main__":
    try:
        PORT = CONFIG.PORT if hasattr(CONFIG, "PORT") and CONFIG.PORT else 3978
        web.run_app(APP, host="ust-python.azurewebsites.net", port=PORT)
    except Exception as error:
        print(f"Error starting the bot: {error}", file=sys.stderr)
        raise
