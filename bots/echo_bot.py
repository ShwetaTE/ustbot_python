# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import ActivityHandler, MessageFactory, TurnContext
from botbuilder.schema import ChannelAccount


class EchoBot(ActivityHandler):
    async def on_members_added_activity(
        self, members_added: [ChannelAccount], turn_context: TurnContext  # type: ignore
    ):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello and welcome!")

    async def on_message_activity(self, turn_context: TurnContext):
        message = str(turn_context.activity.text).lower()
        response = ""
        
        if message == "hi":
            response = "Hello User"
        elif message == "weather":  # Corrected the equality operator
            response = "It's cold"  # Fixed "Its" to "It's"
        
        # Send the response back to the user
        return await turn_context.send_activity(
            MessageFactory.text(response)  # Corrected the return statement
        )
