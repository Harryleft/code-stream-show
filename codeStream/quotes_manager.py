import json
import random
from datetime import date
from tkinter import messagebox


class QuotesManager:
    """
    A class to manage quotes, providing functionality to load quotes and get
    the daily quote.

    Attributes:
        quotes_file (str): The path to the quotes file.
        quotes (list): The list of quotes.
    """

    def __init__(self, quotes_file):
        """
        Initialize the QuotesManager instance.

        Args:
            quotes_file (str): The path to the quotes file.
        """
        self.quotes_file = quotes_file
        self.quotes = self.load_quotes()

    def load_quotes(self):
        """
        Load the JSON quotes file.

        Returns:
            list: The list of quotes, or an empty list if loading fails.
        """
        try:
            with open(self.quotes_file, "r", encoding="utf-8") as file:
                data = json.load(file)
                return data.get("quotes", [])
        except FileNotFoundError:
            messagebox.showwarning(
                "Warning", f"Quotes file not found: {self.quotes_file}"
            )
            return []
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Quotes file format error")
            return []
        except Exception as e:
            messagebox.showerror(
                "Error", f"An error occurred while loading quotes: {str(e)}"
            )
            return []

    def get_daily_quote(self):
        """
        Get the daily quote.

        Returns: str: The daily quote, or a default message if the quotes
        list is empty.
        """
        if not self.quotes:
            return "Keep going today!"

        # Use the date as a random seed to ensure the same quote is shown
        # each day
        random.seed(date.today().toordinal())
        quote = random.choice(self.quotes)
        return f"{quote['text']} \n\n—— {quote['author']}"
