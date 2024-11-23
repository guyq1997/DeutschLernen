from typing import List
from pydantic import BaseModel
from openai import OpenAI
import os
from fastapi import HTTPException
import logging
from dotenv import load_dotenv
import json

class GeneratedWord(BaseModel):
    Wort: str
    Erklärung: str
    Beispiel: str

class GeneratedWordList(BaseModel):
    Wörter: List[GeneratedWord]

async def generate_formatted_text(text: str) -> str:
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
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                    {
                        "role": "system",
                        "content": """Du bist ein Assistent, der deutsche Texte in ein gutes HTML-Format umwandelt, um das Leseerlebnis zu verbessern. Der Benutzer wird dir einen Text zur Verfügung stellen, der im <Text>-XML-Tag enthalten ist.
                        """
                    },
                    {
                        "role": "user",
                        "content": """
                        <Text>
                        In der SPD ist weiter unklar,

                        wer die Partei in
                        den Bundestagswahlkampf führen soll.

                        Kanzler Scholz oder
                        Verteidigungsminister Pistorius.

                        Ein Gespräch der Parteispitze
                        brachte kein Ergebnis.

                        Man wolle aber zeitnah über
                        die Kanzlerkandidatur entscheiden.

                        Markus Preiß in Berlin -
                        Scholz oder Pistorius -

                        wie soll diese Frage in der SPD
                        entschieden werden? Und wann?

                        In den vergangenen Tagen
                        sah es nach einem Showdown aus.

                        </Text>
                        Lesen und verstehen Sie diesen Text zu erst. Und dann bringen Sie ihn in ein gutes Format um das Leseerlebnis zu verbessern. 
                        Bitte beachte folgende Punkte:
                        - Du solltest den Inhalt und die ursprüngliche Bedeutung des Textes nicht verändern. 
                        - Wenn ein vollständiger Satz in verschiedene Zeilen aufgeteilt ist, muss der ganze Satz wieder zusammengesetzt werden.  
                        - Bitte verändere kein einziges Wort. Du fokussierst dich auf die Formatierung.
                        - Du solltest HTML verwenden, um den Text zu formatieren.
                        - Um diesen Artikel besser zu formatieren und gliedernd zu gestalten, kannst du Überschriften hinzufügen.
                        Gib mir am Ende nur den HTML body, und nicht generieren ```html und ``` in Output.
                        """
                    },
                    {
                        "role": "assistant",
                        "content": """
                        <body>
                            <h1>Unklarheit in der SPD: Kanzlerkandidatur</h1>

                            <p>In der SPD ist weiter unklar, wer die Partei in den Bundestagswahlkampf führen soll: Kanzler Scholz oder Verteidigungsminister Pistorius.</p>

                            <h2>Ergebnisloses Gespräch der Parteispitze</h2>
                            <p>Ein Gespräch der Parteispitze brachte kein Ergebnis. Man wolle aber zeitnah über die Kanzlerkandidatur entscheiden.</p>

                            <h2>Markus Preiß in Berlin: Scholz oder Pistorius?</h2>
                            <p>Markus Preiß in Berlin - Scholz oder Pistorius - wie soll diese Frage in der SPD entschieden werden? Und wann?</p>

                            <h2>Showdown in den vergangenen Tagen</h2>
                            <p>In den vergangenen Tagen sah es nach einem Showdown aus.</p>
                        </body>
                        """
                    },
                    {
                        "role": "user",
                        "content": f"""
                        <Text>
                        {text}
                        </Text>
                        Lesen und verstehen Sie diesen Text zu erst. Und dann bringen Sie ihn in ein gutes Format um das Leseerlebnis zu verbessern. 
                        Bitte beachte folgende Punkte:
                        - Du solltest den Inhalt und die ursprüngliche Bedeutung des Textes nicht verändern. 
                        - Wenn ein vollständiger Satz in verschiedene Zeilen aufgeteilt ist, muss der ganze Satz wieder zusammengesetzt werden.  
                        - Bitte verändere kein einziges Wort. Du fokussierst dich auf die Formatierung.
                        - Du solltest HTML verwenden, um den Text zu formatieren.
                        - Um diesen Artikel besser zu formatieren und gliedernd zu gestalten, kannst du Überschriften hinzufügen.
                        Gib mir am Ende nur den HTML body, und nicht generieren ```html und ``` in Output.
                        """
                    }
            ]
        )
        logging.info("Received response from OpenAI")
        
        # Parse the response content
        content = response.choices[0].message.content
        print(content)

        return content
        
    except Exception as e:
        logging.error(f"Error in generate_words_from_text: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error generating words: {str(e)}") 

async def generate_words_from_text(satz: str) -> str:
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
        logging.info(f"Sending request to OpenAI with text length: {len(satz)}")
        response = client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=[
                    {
                        "role": "system",
                        "content": """Du bist ein Deutsch-Tutorial. Der Benutzer stellt dir einen Satz zur Verfügung, der im <Satz>-XML-Tag enthalten ist.
                                    Deine Aufgabe ist es, die mittel- und fortgeschrittenen Wörter zu identifizieren, und sie zu erklären."""
                    },
                    {
                        "role": "user",
                        "content": """
                        <Satz>
                        Was vor den Toren Regensburg passiert, zeigt sich auch bundesweit im GfK-Konsumklimaindex, der seit Jahren im negativen Bereich verharrt.
                        </Satz>
                        Analysieren Sie diesen Text und identifizieren Sie mittel- und fortgeschrittene sowie schwierige Wörter.
                        Du solltest die Wörter in ihrer Originalform auflisten und sie mir erklären. 
                        Wenn es ein Nomen ist, liste auch die Artikel auf und erkläre die Bedeutung auf Deutsch.
                        Wenn es sich um ein Verb handelt, liste die Verben in ihrer Infinitivform auf und erkläre die Verwendung. Bei der Erklärung solltest du auch die passenden Präpositionen angeben, und ob Akkusativ oder Dativ folgen sollte.
                        Anschließend gib ein ganzes Satz als Anwendungsbeispiel. Du solltest das Beispiel aus dem gegebenen Satz formulieren.
                        Bachten, dass die Erklärung nicht zu kompliziert und verständlich sein soll. 
                        """
                    },
                    {
                        "role": "assistant",
                        "content": """
                            {
                            "Wörter": [
                                {
                                "Wort": "verharren",
                                "Erklärung": "in etwas verharren (Dativ, Präposition: in)",
                                "Beispiel": "Der GfK-Konsumklimaindex verharrt seit Jahren im negativen Bereich."
                                }
                            ]
                            }
                        """
                    },
                    {
                        "role": "user",
                        "content": """
                        <Satz>
                        Obwohl die neue Grundsteuer erst ab dem 1. Januar 2025 gilt, haben bundesweit mehr als 6,16 Millionen Steuerzahler bereits gegen ihre Grundsteuerwert- und Messbescheide bei den Finanzämtern Einspruch erhoben.
                        </Satz>
                        Analysieren Sie diesen Text und identifizieren Sie mittel- und fortgeschrittene sowie schwierige Wörter.
                        Du solltest die Wörter in ihrer Originalform auflisten und sie mir erklären. 
                        Wenn es ein Nomen ist, liste auch die Artikel auf und erkläre die Bedeutung auf Deutsch.
                        Wenn es sich um ein Verb handelt, liste die Verben in ihrer Infinitivform auf und erkläre die Verwendung. Bei der Erklärung solltest du auch die passenden Präpositionen angeben, und ob Akkusativ oder Dativ folgen sollte.
                        Anschließend gib ein ganzes Satz als Anwendungsbeispiel. Du solltest das Beispiel aus dem gegebenen Satz formulieren.
                        Bachten, dass die Erklärung nicht zu kompliziert und verständlich sein soll. 
                        """
                    },
                    {
                        "role": "assistant",  
                        "content": """
                        {
                        "Wörter": [
                            {
                            "Wort": "der Einspruch",
                            "Erklärung": "mit der die eigene Ablehnung einer Sache ausgedrückt und versucht wird, diese zu verhindern",
                            "Beispiel": "Mehr als 6,16 Millionen Steuerzahler haben bundesweit bereits gegen ihre Grundsteuerwert- und Messbescheide bei den Finanzämtern Einspruch erhoben."
                            },
                            {
                            "Wort": "erheben",
                            "Erklärung": "etwas erheben (ohne Präposition, Akkusativ)",
                            "Beispiel": "Mehr als 6,16 Millionen Steuerzahler haben bundesweit bereits gegen ihre Grundsteuerwert- und Messbescheide bei den Finanzämtern Einspruch erhoben."
                            }
                        ]
                        }
                        """
                    },
                    {
                        "role": "user",
                        "content": f"""
                        <Satz>
                        {satz}
                        </Satz>
                        Analysieren Sie diesen Text und identifizieren Sie mittel- und fortgeschrittene sowie schwierige Wörter.
                        Du solltest die Wörter in ihrer Originalform auflisten und sie mir erklären. 
                        Wenn es ein Nomen ist, liste auch die Artikel auf und erkläre die Bedeutung auf Deutsch.
                        Wenn es sich um ein Verb handelt, liste die Verben in ihrer Infinitivform auf und erkläre die Verwendung. Bei der Erklärung solltest du auch die passenden Präpositionen angeben, und ob Akkusativ oder Dativ folgen sollte.
                        Anschließend gib ein ganzes Satz als Anwendungsbeispiel. Du solltest das Beispiel aus dem gegebenen Satz formulieren.
                        Bachten, dass die Erklärung nicht zu kompliziert und verständlich sein soll. 
                        """
                    }
            ],
            response_format=GeneratedWordList,
        )
        logging.info("Received response from OpenAI")
        
        # Parse the response content
        content = response.choices[0].message.parsed.Wörter
        print(content)
        
        generated_words = []

        for item in content:
            word = item.Wort
            explain = item.Erklärung
            example = item.Beispiel
            generated_words.append({'Word': word, 'Explaination': explain, 'Example': example})
        
        print(generated_words)
        logging.info(f"Successfully parsed response with {len(content)} words")

        return generated_words
        
    except Exception as e:
        logging.error(f"Error in generate_words_from_text: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error generating words: {str(e)}") 