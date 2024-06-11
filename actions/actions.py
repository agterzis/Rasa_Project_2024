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


class ActionRecommendProduct(Action):

    def name(self) -> Text:
        return "action_recommend_product"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        product_type = tracker.get_slot("product_type")
        product_color = tracker.get_slot("product_color")
        gender = tracker.get_slot("gender")
        size = tracker.get_slot("size")
        
        # Predefined shoe data with type, color, gender, and size
        shoes_catalog = [
            {"name": "Nike Air Zoom Pegasus", "type": "running", "color": "white", "gender": "men", "sizes": [8, 9, 10, 11]},
            {"name": "Adidas Ultraboost", "type": "running", "color": "black", "gender": "women", "sizes": [6, 7, 8, 9]},
            {"name": "Salomon X Ultra 3", "type": "hiking", "color": "blue", "gender": "any", "sizes": [9, 10, 11]},
            {"name": "Merrell Moab 2", "type": "hiking", "color": "green", "gender": "men", "sizes": [8, 9, 10]},
            {"name": "Converse Chuck Taylor", "type": "sneakers", "color": "red", "gender": "women", "sizes": [6, 7, 8]},
            {"name": "Adidas Superstar", "type": "sneakers", "color": "white", "gender": "any", "sizes": [8, 9, 10, 11]},
            {"name": "Air Jordan 1", "type": "basketball", "color": "black", "gender": "men", "sizes": [10, 11, 12]},
            {"name": "Under Armour Curry 7", "type": "basketball", "color": "blue", "gender": "any", "sizes": [9, 10, 11]},
            {"name": "New Balance 990v5", "type": "walking", "color": "grey", "gender": "women", "sizes": [6, 7, 8]},
            {"name": "Skechers GOwalk", "type": "walking", "color": "black", "gender": "any", "sizes": [8, 9, 10, 11]},
            {"name": "Clarks Tilden Cap", "type": "formal", "color": "brown", "gender": "men", "sizes": [8, 9, 10]},
            {"name": "Johnston & Murphy Melton", "type": "formal", "color": "black", "gender": "men", "sizes": [9, 10, 11]},
            {"name": "Reebok Nano X1", "type": "gym", "color": "white", "gender": "women", "sizes": [6, 7, 8]},
            {"name": "Nike Metcon 6", "type": "gym", "color": "black", "gender": "any", "sizes": [8, 9, 10, 11]},
            {"name": "Havaianas Top", "type": "slippers", "color": "blue", "gender": "any", "sizes": [8, 9, 10, 11]},
            {"name": "UGG Scuff", "type": "slippers", "color": "brown", "gender": "men", "sizes": [9, 10, 11]},
            {"name": "Teva Hurricane XLT2", "type": "hiking", "color": "green", "gender": "any", "sizes": [8, 9, 10, 11]},
            {"name": "Chaco Z/1 Classic", "type": "hiking", "color": "black", "gender": "women", "sizes": [6, 7, 8]},
            {"name": "Adidas Copa Mundial", "type": "soccer", "color": "white", "gender": "men", "sizes": [8, 9, 10]},
            {"name": "Nike Mercurial Vapor 13", "type": "soccer", "color": "black", "gender": "any", "sizes": [9, 10, 11]},
        ]

        # Filter shoes based on user input
        filtered_shoes = []
        for shoes in shoes_catalog:
            if product_type and shoes["type"] != product_type.lower():
                continue
            if product_color and shoes["color"] != product_color.lower():
                continue
            if gender and shoes["gender"] != gender.lower() and shoes["gender"] != "any":
                continue
            if size and size not in shoes["sizes"]:
                continue
            filtered_shoes.append(shoes["name"])
        
        # Prepare the response
        if filtered_shoes:
            recommendations = ", ".join(filtered_shoes)
            message = f"Based on your preferences for {product_type} shoes"
            if product_color:
                message += f" in {product_color}"
            if gender:
                message += f" for {gender}"
            if size:
                message += f" in size {size}"
            message += f", here are some recommendations: {recommendations}"
        else:
            message = "Sorry, I couldn't find any shoes matching your preferences. Would you like to try a different type or style?"

        dispatcher.utter_message(text=message)

        return []
