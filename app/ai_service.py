from typing import List
from pydantic import BaseModel
from openai import OpenAI
import os
from fastapi import HTTPException
import logging
from dotenv import load_dotenv
import json

class GeneratedWord(BaseModel):
    Word: str
    Explain: str
    Example: str

class GeneratedWordList(BaseModel):
    words: List[GeneratedWord]

async def generate_words_from_text(text: str) -> List[GeneratedWord]:
    load_dotenv()
    logging.info("Starting generate_words_from_text function")
    
    api_key = os.getenv('OPENAI_API_KEY')
    logging.info(f"API key found: {bool(api_key)}")
    if not api_key:
        logging.error("OpenAI API key not found")
        raise HTTPException(
            status_code=500,
            detail="OpenAI API key not found. Please set the OPENAI_API_KEY environment variable."
        )
    
    client = OpenAI()
    logging.info("OpenAI client initialized")
    
    try:
        logging.info(f"Sending request to OpenAI with text length: {len(text)}")
        response = client.beta.chat.completions.parse(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": """You are a German tutorial. User will provide you with an article, which is in the <Article> xml tag.
                     Your task is to identify the intermediate and advanced words that are important to learn and explain them.
                     You should list the words in its original form and explain it to the user.
                     If it is a verb explain the usage. If it is not a verb explain the meaning of the words in the article. Then provide a usage example. You should take the example from the article."""
                },
                {
                    "role": "user",
                    "content": f"""
                    <Article>
                    Dabei ist es schon schlimm genug, wenn man Siegfried Brandl zuhört. Als Geschäftsführer des Möbelhauses Brandl Home Company in bayerischen Kelheim kann er momentan seine Kunden einzeln mit Handschlag begrüßen. "Die Leute sind total verunsichert und kaufen deshalb nicht", erzählt er und merkt das jeden Tag. Was vor den Toren Regensburg passiert, zeigt sich auch bundesweit im GfK-Konsumklimaindex, der seit Jahren im negativen Bereich verharrt.Die schlechten Nachrichten, die an die Krise vor mehr als 20 Jahren erinnern, springen einem derzeit geradezu entgegen: Die Bundesregierung korrigierte ihre Prognose nach unten und erwartet einen Rückgang der Wirtschaftsleistung um 0,2 Prozent für dieses Jahr. Deutschland steckt damit das zweite Jahr in Folge in der Rezession. Für das kommende Jahr ist die Bundesregierung etwas optimistischer und erwartet ein Plus von 1,1 Prozent.Damit verharrt Deutschland international aber weiterhin im Tabellenkeller: In Rankings wird der Standort Deutschland nach unten durchgereicht. So sagt die OECD für nahezu alle andern Länder der Welt ein kräftiges Wachstum voraus - Indien etwa soll im kommenden Jahr um 6,8 Prozent wachsen, China um 4,5 Prozent, Spanien um 2,2 Prozent. Deutschland bleibt Schlusslicht und rutscht schneller nach unten als in der früheren Krise.
                    </Article>
                    Analyze this text and identify important words to learn.
                    """
                },
                {
                    "role": "assistant",
                    "content": """
                        {
                        "words": [
                            {
                            "Word": "verharren",
                            "Explain": "in etwas verharren (Dativ, Präposition: in)",
                            "Example": "Der GfK-Konsumklimaindex verharrt seit Jahren im negativen Bereich."
                            },
                            {
                            "Word": "entgegenspringen",
                            "Explain": "jemandem entgegenspringen (Dativ; Umgangssprache)",
                            "Example": "Die schlechten Nachrichten, die an die Krise vor mehr als 20 Jahren erinnern, springen einem derzeit geradezu entgegen."
                            },
                            {
                            "Word": "geradezu",
                            "Explain": "direkt, sogar; man kann sogar",
                            "Example": "Die schlechten Nachrichten, die an die Krise vor mehr als 20 Jahren erinnern, springen einem derzeit geradezu entgegen."
                            },
                            {
                            "Word": "die Rezession",
                            "Explain": "Rückgang der Konjunktur",
                            "Example": "Deutschland steckt das zweite Jahr in Folge in der Rezession."
                            },
                            {
                            "Word": "der Tabellenkeller",
                            "Explain": "Tabellenende",
                            "Example": "Deutschland verharrt international im Tabellenkeller."
                            },
                                {
                            "Word": "durchreichen",
                            "Explain": "etwas durchreichen (Akkusativ)",
                            "Example": "Deutschland wird in Rankings nach unten durchgereicht."
                            }
                        ]
                        }
                    """
                },
                {
                    "role": "user",
                    "content": f"""
                    <Article>
                    {text}
                    </Article>
                    Analyze this text and identify important words to learn.
                    """
                }
            ],
            response_format=GeneratedWordList,
        )
        logging.info("Received response from OpenAI")
        
        # Parse the response content
        content = response.choices[0].message.parsed.words
        print(content)
        
        generated_words = []

        for item in content:
            word = item.Word
            explain = item.Explain
            example = item.Example
            generated_words.append({'Word': word, 'Explaination': explain, 'Example': example})
        
        print(generated_words)
        logging.info(f"Successfully parsed response with {len(content)} words")

        return generated_words
        
    except Exception as e:
        logging.error(f"Error in generate_words_from_text: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error generating words: {str(e)}") 