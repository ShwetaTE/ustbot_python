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



# import aiohttp  # For making asynchronous HTTP requests
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
#         user_message = turn_context.activity.text  # Get user message from activity
#         api_url = "https://ust-bot.azurewebsites.net/bot-endpoint/"
        
#         try:
#             async with aiohttp.ClientSession() as session:
#                 async with session.post(
#                     api_url, 
#                     json={"text": user_message}
#                 ) as response:
#                     if response.status == 200:
#                         api_response = await response.json()
#                         response_text = api_response.get("text", "Sorry, I couldn't understand the response.")
#                     else:
#                         response_text = f"Error: API returned status code {response.status}"
#         except Exception as e:
#             response_text = f"Failed to reach API: {str(e)}"
        
#         # Send the API response text to the user
#         return await turn_context.send_activity(
#             MessageFactory.text(response_text)
#         )













import aiohttp
from botbuilder.core import ActivityHandler, MessageFactory, TurnContext
from botbuilder.schema import ChannelAccount
from bots.authentication_connect import get_user_email  # Import authentication module

class EchoBot(ActivityHandler):
    async def on_members_added_activity(self, members_added: [ChannelAccount], turn_context: TurnContext):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                print("[DEBUG] New member added: Sending welcome message.")
                await turn_context.send_activity("Hello and welcome!")

    async def on_message_activity(self, turn_context: TurnContext):
        user_message = turn_context.activity.text
        print(f"[DEBUG] Received message: {user_message}")

        print("[DEBUG] Fetching user email...")
        user_email = await get_user_email()

        if not user_email:
            print("[ERROR] Failed to retrieve user email.")
            return await turn_context.send_activity(MessageFactory.text("Failed to retrieve user email."))

        api_url = "https://ust-chatbot-01.eastus.inference.ml.azure.com/score"
        request_payload = {
            "chat_history": [],
            "question": user_message,
            "user_email": user_email
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer 3pxsibh45K4g5bCdGlyWTpv30LXgl76f"
        }

        print(f"[DEBUG] Sending JSON payload to API: {request_payload}")

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(api_url, json=request_payload, headers=headers) as response:
                    print(f"[DEBUG] API response status: {response.status}")
                    
                    if response.status == 200:
                        try:
                            api_response = await response.json()
                            print(f"[DEBUG] API response JSON: {api_response}")

                            # ✅ Fix: Extract "answer" instead of "text"
                            response_text = api_response.get("answer", "Sorry, I couldn't understand the response.")
                        except Exception as e:
                            print(f"[ERROR] JSON decoding error: {str(e)}")
                            response_text = "Error: Failed to parse API response."
                    else:
                        error_message = await response.text()
                        print(f"[ERROR] API error response: {error_message}")
                        response_text = f"Error: API returned status code {response.status}. Message: {error_message}"
        except Exception as e:
            response_text = f"Failed to reach API: {str(e)}"
            print(f"[ERROR] Exception: {response_text}")

        return await turn_context.send_activity(MessageFactory.text(response_text))
