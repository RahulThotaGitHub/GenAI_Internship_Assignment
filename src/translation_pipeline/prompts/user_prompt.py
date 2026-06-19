def build_prompt(question_te, answer_te):

    return f"""
TASK

Process the Telugu Ramayana Question-Answer pair.

Perform ALL steps.

STEP 1

Translate the Telugu question into grammatically correct English.

STEP 2

Translate the Telugu answer into grammatically correct English.

STEP 3

Preserve cultural, historical, theological, and literary meaning.

STEP 4

Use canonical transliterations provided in the transliteration guide.

STEP 5

Do NOT simplify, summarize, modernize, or reinterpret.

STEP 6

Extract entities.

STEP 7

Extract relations.

------------------------------------------------

ENTITY TYPES

Use ONLY the following types:

Person
Deity
Sage
Place
River
Mountain
Kingdom
Rakshasa
Vanara
Weapon
Yaga
Nakshatra
Kanda
Sarga
Event
Concept

------------------------------------------------

RELATION TYPES

Use concise relation names such as:

born_in
resides_in
performed
ruled
father_of
mother_of
teacher_of
disciple_of
married_to
defeated
blessed
cursed
visited
traveled_to
participated_in
belongs_to
part_of
located_in

------------------------------------------------

ENTITY EXTRACTION RULES

Extract only explicit entities.

Do not infer hidden entities.

Do not invent entities.

Do not create duplicate entities.

------------------------------------------------

RELATION EXTRACTION RULES

Extract only relations explicitly supported by the text.

Do not infer unstated facts.

Do not use pronouns.

Use canonical entity names.

------------------------------------------------

OUTPUT FORMAT

Return ONLY valid JSON.

{{
  "question_en": "",
  "answer_en": "",

  "entities": [
    {{
      "name": "",
      "type": ""
    }}
  ],

  "relations": [
    {{
      "subject": "",
      "relation": "",
      "object": ""
    }}
  ]
}}

------------------------------------------------

QUESTION (TELUGU)

{question_te}

------------------------------------------------

ANSWER (TELUGU)

{answer_te}
"""