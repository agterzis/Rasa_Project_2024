from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet  # Import SlotSet


class ActionCheckOrderId(Action):
    def name(self) -> Text:
        return "action_check_order_id"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        order_id = next(tracker.get_latest_entity_values("id"), None)

        if order_id == "12345":
            dispatcher.utter_message(text="Your order will arrive in one day.")
            return []
        else:
            dispatcher.utter_message(text="Incorrect ID, please try again.")
            return []
