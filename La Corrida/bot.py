# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import ActivityHandler, MessageFactory, TurnContext
from botbuilder.schema import ChannelAccount, CardAction, ActionTypes, SuggestedActions
import scrape as houseData


class MyBot(ActivityHandler):
	"""
	This bot will respond to the user's input with suggested actions.
	Suggested actions enable your bot to present buttons that the user
	can tap to provide input.
	"""
	houseData.getHousing()
	global houseNum
	houseNum = None


	async def on_members_added_activity(
		self, members_added: [ChannelAccount], turn_context: TurnContext
	):
		"""
		Send a welcome message to the user and tell them what actions they may perform to use this bot
		"""

		return await self._send_welcome_message(turn_context)

	async def on_message_activity(self, turn_context: TurnContext):
		"""
		Respond to the users choice and display the suggested actions again.
		"""
		global houseNum

		if houseNum is None:
			houseNum = 0

		text = turn_context.activity.text.lower()
		response_text = self._process_input(text,houseNum)

		await turn_context.send_activity(MessageFactory.text(response_text))

		return await self._send_suggested_actions(turn_context)

	async def _send_welcome_message(self, turn_context: TurnContext):
		for member in turn_context.activity.members_added:
			if member.id != turn_context.activity.recipient.id:
				await turn_context.send_activity(
					MessageFactory.text(
						"Hello and Welcome!"
					)
				)

				await self._send_suggested_actions(turn_context)


	def _process_input(self, text: str, num: int):

		if text == "housing":
			numPosts = num + 3
			msg = ""
			global houseNum

			while num <= numPosts:
				msg += houseData.post_titles[num]
				msg += "\n"
				msg += "Located in " + houseData.post_areas[num] + " with " + str(houseData.post_sqft[num]) + "sqft and "  
				msg +=  str(houseData.post_br[num]) + "bedroom, priced at " + houseData.post_prices[num]
				msg += "\n"
				msg +="Learn more here: " + houseData.post_links[num]
				msg += "\n\n\n"
				num += 1
		
			houseNum = num
			return msg

		return "Please select a valid option from the provided choices"

	async def _send_suggested_actions(self, turn_context: TurnContext):
		"""
		Creates and sends an activity with suggested actions to the user. When the user
		clicks one of the buttons the text value from the "CardAction" will be displayed
		in the channel just as if the user entered the text. There are multiple
		"ActionTypes" that may be used for different situations.
		"""

		reply = MessageFactory.text("What are you interested in?")

		reply.suggested_actions = SuggestedActions(
			actions=[
				CardAction(
					title="Housing",
					type=ActionTypes.im_back,
					value="Housing",
				),
				CardAction(
					title="Food Joints",
					type=ActionTypes.im_back,
					value="Food Joints",
				),
				CardAction(
					title="Job Listings",
					type=ActionTypes.im_back,
					value="Job Listings",
				),
				CardAction(
					title="Misc Resources",
					type=ActionTypes.im_back,
					value="Misc Resources",
				),
				CardAction(
					title="Community Chat",
					type=ActionTypes.im_back,
					value="Community Chat",
				),
			]
		)

		return await turn_context.send_activity(reply)
