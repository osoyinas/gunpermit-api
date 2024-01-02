import fitz
import re
import os
import json
import random

def extract_questions_and_answers(text: str) -> dict:
    # lista con cada linea del texto
    split_text = text.splitlines()  
    # lista sin elementos " "
    strip_text = list(filter(lambda line: line.strip() != "",
                      split_text))  

    topic = strip_text.pop(0).strip()  # El tema es la primera linea
    #los subtemas estan en MAYUS
    raw_subtopics = list(filter(lambda line: line.isupper() and ").-" not in line, strip_text))
    # eliminamos los repetidos
    subtopics = list(set(map(lambda subtopic: subtopic.
                             replace("•", "").
                             replace(".", "").
                             replace("-", "").
                             strip(),
                             raw_subtopics)))
    text = '\n'.join(strip_text)
    text = text.replace(topic, "")
    for subtopic in subtopics:
        text = text.replace(subtopic, "")

    #Quitar subtitulos como -Medidas de seguridad en el uso.
    subtitle_pattern = r'(?:^|\n)\-\s*.*?(?=\d+\.)'
    subtitles = re.findall(subtitle_pattern, text, re.DOTALL)
    
    for subtitle in subtitles:
        text = text.replace(subtitle.strip('\n'), "")

    #Obtenemos las preguntas
    question_pattern =  r'(?:^|\n)(\d+)\.\s*(.*?)(?=\nA\)|\nA\.\-|$)'
    questions = re.findall(question_pattern, text, re.DOTALL)
    #Obtenemos las respuestas, 4 patrones porque hay respuestas con ).-, ), .- e incluso . -. *HA SIDO UN INFIERNO*
    answers_pattern =  r'[A-C]\)\.\s?\-?(\s*\d*.*?)(?=(?:\n[B-C]\)|\n\d+|$))'
    answers_pattern2 = r'\n[A-C]\)\s(.*?)(?=(?:\n[B-C]\)|\n\d+|$))'
    answers_pattern3 = r'\n[A-C]\.\s?\-(.*?)(?=(?:\n[B-C]\.\-|\n\d+|$))'
    answers_pattern4 = r'\n[A-C]\)([A-Z].*?)(?=(?:\n[B-C]\)|\n\d+|$))'

    answers = re.findall(answers_pattern, text, re.DOTALL)
    answers.extend(re.findall(answers_pattern2, text, re.DOTALL))
    answers.extend(re.findall(answers_pattern3, text, re.DOTALL))
    answers.extend(re.findall(answers_pattern4, text, re.DOTALL))
    # filtrar /n y .-
    questions = list(map(lambda question: (
        question[0], question[1].replace("\n", " ").strip()), questions))
    answers = list(map(lambda answer: answer.replace(
        "\n", " ").replace(".-", "").strip(), answers))

    questions_and_answers = []
    # Deberia haber 3 respuestas por cada pregunta.
    if (len(questions)*3 != len(answers)):
        print("No coinciden el numero de preguntas con el numero de respuestas.")
        print("Numero de preguntas", len(questions))
        print("Numero de respuestas", len(answers))

    for i in range(len(questions)):
        random_true_answer = random.randint(0, 2)
        questions_and_answers.append({
            "index": questions[i][0],
            "question": questions[i][1],
            "answers": [{"answer": answer, "is_true": index == random_true_answer} for index, answer in enumerate(answers[i*3:i*3 + 3])]})

    return {"topic": topic, "subtopics": subtopics,  "questions": questions_and_answers}


def get_text_from(file_name):
    with fitz.open(file_name) as pdf_doc:
        all_text = ""
        for page in pdf_doc.pages():
            all_text += page.get_text()

    return all_text


def output_in_json(all_text, file_name, output_dir):
    if (not os.path.exists(output_dir)):
        os.mkdir(output_dir)
    output_file_name = os.path.join(output_dir, file_name+ ".json")
    data = extract_questions_and_answers(all_text)

    with open(output_file_name, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)


def extract_number(filename):
    """
    Extrae el numero del tema del nombre del archivo
    """
    try:
        return int(filename.split('tema')[1].split('_')[0])
    except:
        return 0



