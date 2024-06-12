from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionCheckOrderId(Action):
    def name(self) -> Text:
        return "action_check_order_id"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        order_id = tracker.get_slot("id")
        # intent_name = tracker.latest_message['intent'].get('name')
        # current_story = tracker.get_slot("current_story")
        exchange_requested = tracker.get_slot("exchange")  # Παίρνουμε την τιμή του slot
        refund_requested = tracker.get_slot("refund")  # Παίρνουμε την τιμή του slot

        if refund_requested:  # Λογική για επιστροφή χρημάτων
            dispatcher.utter_message(text=f"Okay, a refund will be issued for the order with ID {order_id}. "
                                          f"Can I help you with something else? ")
            return []
        elif exchange_requested:  # Λογική για ανταλλαγή
            dispatcher.utter_message(text=f"Nice, I'll change your order with ID {order_id} with something new. What "
                                          f"would you like to buy?")
            return []
        else:
            if order_id == "12345":
                dispatcher.utter_message(text=f"Your order with ID: {order_id} will arrive in one day.")
                return []
            else:
                dispatcher.utter_message(text=f"Sorry, I couldn't find any order with ID {order_id}. Can I help you "
                                              f"with something else?")
                return []


class ActionCheckStoreLocation(Action):
    def name(self) -> Text:
        return "action_check_store_location"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        location = tracker.get_slot("location")

        if location.lower() == "thessaloniki":
            dispatcher.utter_message(
                text="We have two stores. The first one is located at 10 Egnatia Street and the second one is at "
                     "5 Tsimiski Street.")
        else:
            dispatcher.utter_message(
                text=f"Unfortunately, we don't have any store in {location} at the moment. We only have stores in "
                     f"Thessaloniki.")
        return []
