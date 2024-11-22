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
                        "content": """Du bist ein Deutsch-Tutorial. Der Benutzer stellt dir einen Artikel zur Verfügung, der im <Article>-XML-Tag enthalten ist.
                                    Deine Aufgabe ist es, die mittel- und fortgeschrittenen Wörter zu identifizieren, die wichtig sind, um sie zu lernen, und sie zu erklären."""
                    },
                    {
                        "role": "user",
                        "content": """
                        <Article>
                        Dabei ist es schon schlimm genug, wenn man Siegfried Brandl zuhört. Als Geschäftsführer des Möbelhauses Brandl Home Company in bayerischen Kelheim kann er momentan seine Kunden einzeln mit Handschlag begrüßen. "Die Leute sind total verunsichert und kaufen deshalb nicht", erzählt er und merkt das jeden Tag. Was vor den Toren Regensburg passiert, zeigt sich auch bundesweit im GfK-Konsumklimaindex, der seit Jahren im negativen Bereich verharrt.Die schlechten Nachrichten, die an die Krise vor mehr als 20 Jahren erinnern, springen einem derzeit geradezu entgegen: Die Bundesregierung korrigierte ihre Prognose nach unten und erwartet einen Rückgang der Wirtschaftsleistung um 0,2 Prozent für dieses Jahr. Deutschland steckt damit das zweite Jahr in Folge in der Rezession. Für das kommende Jahr ist die Bundesregierung etwas optimistischer und erwartet ein Plus von 1,1 Prozent.Damit verharrt Deutschland international aber weiterhin im Tabellenkeller: In Rankings wird der Standort Deutschland nach unten durchgereicht. So sagt die OECD für nahezu alle andern Länder der Welt ein kräftiges Wachstum voraus - Indien etwa soll im kommenden Jahr um 6,8 Prozent wachsen, China um 4,5 Prozent, Spanien um 2,2 Prozent. Deutschland bleibt Schlusslicht und rutscht schneller nach unten als in der früheren Krise.
                        </Article>
                        Analysieren Sie diesen Text und identifizieren Sie mittel- und fortgeschrittene sowie schwierige Wörter, die Ich lernen muss.
                        Du solltest die Wörter in ihrer Originalform auflisten und sie mir erklären. 
                        Wenn es ein Nomen ist, liste auch die Artikel auf und erkläre die Bedeutung auf Deutsch.
                        Wenn es sich um ein Verb handelt, liste die Verben in ihrer Infinitivform auf und erkläre die Verwendung. Bei der Erklärung solltest du auch die passenden Präpositionen angeben, und ob Akkusativ oder Dativ folgen sollte.
                        Anschließend gib ein Anwendungsbeispiel. Du solltest das Beispiel aus dem Artikel entnehmen.
                        Bachten, dass die Erklärung nicht zu kompliziert und verständlich sein soll. 
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
                        "content": """
                        <Article>
                        Die neue Grundsteuer sorgt nicht nur bei Eigentümern für Verärgerung, sondern auch bei Mietern. Denn Vermieter können die zusätzlichen Kosten auf sie umlegen. Wahrscheinlich wird Wohnen für Millionen Menschen teurer.
                        Das Finanzamt fordert 2.500 statt 40 Euro? Nach der Reform der Grundsteuer schauen einige Hauseigentümer fassungslos auf ihre Bescheide. Die Neubewertungen ihrer Grundstücke durch die Finanzämter haben den einen oder anderen auf dem Papier regelrecht reich gemacht - und damit könnte auch die Höhe der neuen Grundsteuer drastisch steigen. In nicht mal drei Monaten tritt eine Reform in Kraft, die bundesweit alle Mieter und Eigentümer betrifft.
                        Obwohl die neue Grundsteuer erst ab dem 1. Januar 2025 gilt, haben bundesweit mehr als 6,16 Millionen Steuerzahler bereits gegen ihre Grundsteuerwert- und Messbescheide bei den Finanzämtern Einspruch erhoben. Das ergab eine aktuelle Umfrage von *Plusminus* bei den zuständigen Finanzministerien der Länder. Viele der Einsprüche berufen sich auf laufende Musterverfahren, die sich gegen das sogenannte Bundesmodell richten, das in elf Bundesländern gilt. Initiiert wurden sie von Haus und Grund und dem Bund der Steuerzahler.
                        </Article>
                        Analysieren Sie diesen Text und identifizieren Sie mittel- und fortgeschrittene sowie schwierige Wörter, die Ich lernen muss.
                        Du solltest die Wörter in ihrer Originalform auflisten und sie mir erklären. 
                        Wenn es ein Nomen ist, liste auch die Artikel auf und erkläre die Bedeutung auf Deutsch.
                        Wenn es sich um ein Verb handelt, liste die Verben in ihrer Infinitivform auf und erkläre die Verwendung. Bei der Erklärung solltest du auch die passenden Präpositionen angeben, und ob Akkusativ oder Dativ folgen sollte.
                        Anschließend gib ein Anwendungsbeispiel. Du solltest das Beispiel aus dem Artikel entnehmen.
                        Bachten, dass die Erklärung nicht zu kompliziert und verständlich sein soll. 
                        """
                    },
                    {
                        "role": "assistant",  
                        "content": """
                        {
                        "words": [
                            {
                            "Word": "sorgen",
                            "Explain": "für Verärgerung sorgen = etwas führt zur Verärgerung (Präposition: für, Akkusativ)",
                            "Example": "Die neue Grundsteuer sorgt nicht nur bei Eigentümern für Verärgerung, sondern auch bei Mietern."
                            },
                            {
                            "Word": "umlegen",
                            "Explain": "die Kosten auf jemanden umlegen (Präposition: auf, Akkusativ)",
                            "Example": "Damit werden sich auch Mietwohnungen verteuern - denn Vermieter können die Zusatzkosten durch die Grundsteuer auf die Miete umlegen."
                            },
                            {
                            "Word": "fassungslos",
                            "Explain": "ohnmächtig, ohne Fassung",
                            "Example": "Einige Hauseigentümer sehen sich auf ihre Bescheide fassungslos gegenüber."
                            },
                            {
                            "Word": "regelrecht",
                            "Explain": "geradezu, sogar; man kann sogar",
                            "Example": "Neubewertungen ihrer Grundstücke durch die Finanzämter haben den einen oder anderen auf dem Papier regelrecht reich gemacht."
                            },
                            {
                            "Word": "Einspruch erheben",
                            "Explain": "vor Gericht widersprechen",
                            "Example": "haben bundesweit mehr als 6,16 Millionen Steuerzahler bereits gegen ihre Grundsteuerwert- und Messbescheide bei den Finanzämtern Einspruch erhoben."
                            },
                            {
                            "Word": "ergeben",
                            "Explain": "sich zeigen (ohne Präposition, Akkusativ)",
                            "Example": "Das ergab eine aktuelle Umfrage von Plusminus bei den zuständigen Finanzministerien der Länder."
                            },
                            {
                            "Word": "berufen",
                            "Explain": "sich auf etwas berufen (Präposition: auf, Akkusativ)",
                            "Example": "Viele der Einsprüche berufen sich auf laufende Musterverfahren, die sich gegen das sogenannte Bundesmodell richten, das in elf Bundesländern gilt."
                            },
                            {
                            "Word": "initiieren",
                            "Explain": "etwas initiieren (ohne Präposition, Akkusativ)",
                            "Example": "Initiiert wurden sie von Haus und Grund und dem Bund der Steuerzahler."
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
                        Analysieren Sie diesen Text und identifizieren Sie wichtige Wörter, die Ich lernen muss.
                        Du solltest die Wörter in ihrer Originalform auflisten und sie dem Benutzer erklären.
                        Wenn es sich um ein Verb handelt, erkläre die Verwendung.
                        Wenn es kein Verb ist, erkläre die Bedeutung der Wörter aus dem Artikel.
                        Anschließend gib ein Anwendungsbeispiel. Du solltest das Beispiel aus dem Artikel entnehmen.
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