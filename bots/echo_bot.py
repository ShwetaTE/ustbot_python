# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

# from botbuilder.core import ActivityHandler, MessageFactory, TurnContext
# from botbuilder.schema import ChannelAccount


# class EchoBot(ActivityHandler):
#     async def on_members_added_activity(
#         self, members_added: [ChannelAccount], turn_context: TurnContext
#     ):
#         for member in members_added:
#             if member.id != turn_context.activity.recipient.id:
#                 await turn_context.send_activity("Hello and welcome!")

#     async def on_message_activity(self, turn_context: TurnContext):
#         return await turn_context.send_activity(
#             MessageFactory.text(f"Echo: {turn_context.activity.text}")
#         )



import aiohttp  # For making asynchronous HTTP requests
from botbuilder.core import ActivityHandler, MessageFactory, TurnContext
from botbuilder.schema import ChannelAccount


class EchoBot(ActivityHandler):
    async def on_members_added_activity(
        self, members_added: [ChannelAccount], turn_context: TurnContext
    ):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello and welcome!")

    async def on_message_activity(self, turn_context: TurnContext):
        user_message = turn_context.activity.text  # Get user message from activity
        api_url = "https://ust-bot.azurewebsites.net/bot-endpoint/"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    api_url, 
                    json={"text": user_message}
                ) as response:
                    if response.status == 200:
                        api_response = await response.json()
                        response_text = api_response.get("text", "Sorry, I couldn't understand the response.")
                    else:
                        response_text = f"Error: API returned status code {response.status}"
        except Exception as e:
            response_text = f"Failed to reach API: {str(e)}"
        
        # Send the API response text to the user
        return await turn_context.send_activity(
            MessageFactory.text(response_text)
        )

