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
            model="gpt-4",
            messages=[
                    {
                        "role": "system",
                        "content": """Du bist ein Assistent, der deutsche Texte in ein gutes Markdown-Format umwandelt, um das Leseerlebnis zu verbessern. Der Benutzer wird dir einen Text zur Verfügung stellen, der im <Text>-XML-Tag enthalten ist.
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

                        Heute ist es deutlich ruhiger,
                        der Kanzler ist zurück aus Rio,

                        er hatte keine öffentlichen Termine.

                        Und damit viel Zeit,
                        zu telefonieren.

                        In der SPD sieht man,

                        dass die Debatte der letzten Tage
                        der Partei schadet.

                        SPD-Chef Klingbeil hat deshalb eine
                        zügige Entscheidung angekündigt,

                        ohne konkret zu sagen wann.

                        Man kann davon ausgehen, dass das
                        spätestens am Wochenende passiert

                        und dann am Montag nach der Sitzung
                        des Parteivorstands verkündet wird.

                        Was man – mit aller Vorsicht -
                        heute raushört:

                        Es sieht nicht
                        nach einem Putsch aus.

                        Pistorius wird wohl nur Kandidat,
                        wenn Scholz verzichtet.

                        Das macht auch Sinn, denn sonst wäre
                        nicht nur der Kanzler beschädigt –

                        sondern auch die SPD-Chefs
                        Klingbeil und Esken.

                        Kann es sich die SPD
                        überhaupt erlauben,

                        nicht mit dem beliebteren Pistorius
                        in die Wahl zu gehen?

                        Das klingt in der Tat
                        nicht besonders logisch –

                        aber es ist möglich.

                        Zuletzt hat man sehr auf Schwächen
                        von Olaf Scholz geschaut.

                        Je länger diskutiert wird, werden
                        auch die von Pistorius angeschaut.

                        Dass er kein Wirtschaftsfachmann
                        ist, aber die Frage,

                        wie Jobs und Firmen gerettet werden,
                        wohl zentral wird im Wahlkampf.

                        Dass Pistorius Deutschland
                        "kriegstüchtig" machen will –

                        ein Wort, das keinesfalls
                        für Begeisterung in der SPD sorgt.

                        Nicht zuletzt wird
                        immer wieder erwähnt,

                        dass die SPD schon mal mit
                        einem beliebten Politiker antrat.

                        Der ist krachend gescheitert –
                        das war 2017 mit Martin Schulz.

                        Sie selbst
                        nennen es Mission Silberlocke:

                        Damit die angeschlagene Linkspartei
                        in den nächsten Bundestag kommt,

                        wollen die drei bekannten
                        Linken-Politiker

                        Ramelow, Gysi und Bartsch
                        als Direktkandidaten antreten.

                        Wie sie in Berlin erklärten,

                        geht es ihnen um
                        die sogenannte Grundmandatsklausel:

                        Danach würden drei direkt
                        gewonnene Wahlkreise ausreichen,

                        um mit der Stärke der Zweitstimmen
                        in den Bundestag einzuziehen.

                        Selbst, wenn die Linke
                        unter der Fünf-Prozent-Hürde bleibt.

                        In Thüringen wurde
                        vor gut zweieinhalb Monaten gewählt.

                        CDU, BSW und SPD nahmen Verhandlungen
                        über eine Regierung auf -

                        und sie sind sich einig geworden:

                        Am Entwurf des Koalitionsvertrags
                        seien nur noch Feinarbeiten nötig,

                        hieß es aus den Parteien.

                        Sie wollen den Text
                        am Freitag vorstellen.

                        Auch die Friedens-Forderungen des BSW
                        sollen darin eine Rolle spielen.
                        </Text>
                        Lesen und verstehlen Sie diesen Text zu erst. Und dann bringen Sie ihn in ein gutes Format um das Leseerlebnis zu verbessern. 
                        Bitte beachte folgende Punkte:
                        - Du solltest den Inhalt und die ursprüngliche Bedeutung des Textes nicht verändern. 
                        - Bitte verändere kein einziges Wort. Du fokussierst dich auf die Formatierung.
                        - Wenn ein vollständiger Satz in verschiedene Zeilen aufgeteilt ist, muss der ganze Satz wieder zusammengesetzt werden.  
                        - Du solltest Markdown verwenden, um dieses Ergebnis zu produzieren.
                        - Um diesen Artikel besser zu formatieren, kannst du einige dieser Wörter in Überschriften umwandeln.
                        - Du kannst den Artikel in Absätze unterteilen.
                        Gib mir am Ende nur den Text in Markdown Format.
                        """
                    },
                    {
                        "role": "assistant",
                        "content": """
                            # Unklarheit in der SPD: Wer führt die Partei in den Bundestagswahlkampf?

                            In der SPD ist weiterhin unklar, wer die Partei in den Bundestagswahlkampf führen soll: Kanzler Olaf Scholz oder Verteidigungsminister Boris Pistorius. Ein Gespräch der Parteispitze brachte kein Ergebnis. Man wolle aber zeitnah über die Kanzlerkandidatur entscheiden.

                            ## Wie wird die Kanzlerfrage entschieden – und wann?

                            In den vergangenen Tagen sah es nach einem Showdown aus. Heute ist es deutlich ruhiger. Der Kanzler ist zurück aus Rio, hatte keine öffentlichen Termine und damit viel Zeit zu telefonieren. 

                            In der SPD sieht man, dass die Debatte der letzten Tage der Partei schadet. SPD-Chef Lars Klingbeil hat deshalb eine zügige Entscheidung angekündigt, ohne konkret zu sagen, wann. Man kann davon ausgehen, dass das spätestens am Wochenende passiert und dann am Montag nach der Sitzung des Parteivorstands verkündet wird.

                            Mit aller Vorsicht: Es sieht nicht nach einem Putsch aus. Pistorius wird wohl nur Kandidat, wenn Scholz verzichtet. Das ergibt auch Sinn, denn sonst wäre nicht nur der Kanzler beschädigt, sondern auch die SPD-Chefs Klingbeil und Saskia Esken.

                            ## Kann sich die SPD Pistorius als Kanzlerkandidat leisten?

                            Das klingt in der Tat nicht besonders logisch – aber es ist möglich. Zuletzt hat man sehr auf Schwächen von Olaf Scholz geschaut. Je länger diskutiert wird, werden auch die von Pistorius betrachtet: 

                            - **Kein Wirtschaftsfachmann:** Die Frage, wie Jobs und Firmen gerettet werden, wird wohl zentral im Wahlkampf. 
                            - **"Kriegstüchtigkeit":** Pistorius wolle Deutschland "kriegstüchtig" machen – ein Wort, das keinesfalls für Begeisterung in der SPD sorgt.

                            Nicht zuletzt wird immer wieder erwähnt, dass die SPD schon einmal mit einem beliebten Politiker antrat – und krachend scheiterte. Das war 2017 mit Martin Schulz.

                            ---

                            # Die Mission Silberlocke der Linkspartei

                            Damit die angeschlagene Linkspartei in den nächsten Bundestag kommt, wollen die bekannten Linken-Politiker Bodo Ramelow, Gregor Gysi und Dietmar Bartsch als Direktkandidaten antreten. Wie sie in Berlin erklärten, geht es ihnen um die sogenannte Grundmandatsklausel. Danach würden drei direkt gewonnene Wahlkreise ausreichen, um mit der Stärke der Zweitstimmen in den Bundestag einzuziehen – selbst, wenn die Linke unter der Fünf-Prozent-Hürde bleibt.

                            ---

                            # Fortschritte in Thüringen: CDU, BSW und SPD einigen sich

                            In Thüringen wurde vor gut zweieinhalb Monaten gewählt. CDU, BSW und SPD nahmen Verhandlungen über eine Regierung auf – und sie sind sich einig geworden. Am Entwurf des Koalitionsvertrags seien nur noch Feinarbeiten nötig, hieß es aus den Parteien. Sie wollen den Text am Freitag vorstellen. Auch die Friedens-Forderungen des BSW sollen darin eine Rolle spielen.
                        """
                    },
                    {
                        "role": "user",
                        "content": f"""
                        <Text>
                        {text}
                        </Text>
                        Lesen und verstehlen Sie diesen Text zu erst. Und dann bringen Sie ihn in ein gutes Format um das Leseerlebnis zu verbessern. 
                        Bitte beachte folgende Punkte:
                        - Du solltest den Inhalt und die ursprüngliche Bedeutung des Textes nicht verändern. 
                        - Bitte verändere kein einziges Wort. Du fokussierst dich auf die Formatierung.
                        - Wenn ein vollständiger Satz in verschiedene Zeilen aufgeteilt ist, muss der ganze Satz wieder zusammengesetzt werden.  
                        - Du solltest Markdown verwenden, um dieses Ergebnis zu produzieren.
                        - Um diesen Artikel besser zu formatieren, kannst du einige dieser Wörter in Überschriften umwandeln.
                        - Du kannst den Artikel in Absätze unterteilen.
                        Gib mir am Ende nur den Text in Markdown Format.
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