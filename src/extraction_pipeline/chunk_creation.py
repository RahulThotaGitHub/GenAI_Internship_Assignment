import re
import json  

def create_chunk(
    chunk_counter,
    *,
    kanda="",
    sarga="",
    adhyayamu="",
    question_no="",
    question_type="preface",
    question_te="",
    question_en="",
    answer_te="",
    answer_en="",
    entities=None,
    relations=None,
    page_no="",
):
    return {
        "chunk_id": f"chunk_{chunk_counter}",
        "kanda": kanda,
        "sarga": sarga,
        "adhyayamu": adhyayamu,
        "question_no": question_no,
        "question_type": question_type,
        "question_te": question_te,
        "answer_te": answer_te,
        "question_en": question_en,
        "answer_en": answer_en,
        "entities": entities or [],
        "relations": relations or [],
        "metadata": {
            "source_language": "te",
            "target_language": "en",
            "book": "RAMAYANA PRASHNAVALI",
            "page no": page_no,
            "year": "2025",
            "author": "Marella Venkata Sesha Reddy"
        }
    }


def final_chunks(all_text_sarg, about_text, all_kanda, all_sarga, all_adhyayamu):
    chunk_counter = 0

    extra_chunk = create_chunk(
        chunk_counter,
        kanda="",
        sarga="",
        adhyayamu="",
        question_no="",
        question_type="preface",
        question_te="శ్రీరామాయణము – ప్రశ్నావళి గురించి",
        answer_te=about_text,
        question_en="",
        answer_en="",
        entities=["మారెళ్ళ వెంకట శేషారెడ్డి"],
        relations=[],
        page_no="vi(6)"
    )

    chunks = [extra_chunk]
    chunk_counter = 1


    # =====================================================
    # LOOP THROUGH EVERY SARGA
    # =====================================================

    for sarga_index, text in enumerate(all_text_sarg):

        # ---------------------------------------------
        # Metadata
        # ---------------------------------------------

        current_kanda = all_kanda[sarga_index].replace("\t", " ")
        current_sarga = all_sarga[sarga_index]
        current_adhyayamu = all_adhyayamu[sarga_index]

        # =====================================================
        # Separate Answer Key
        # =====================================================

        answer_key_match = re.search(
            r'జవాబులు\s*:(.*)$',
            text,
            flags=re.DOTALL
        )

        answer_key = ""

        if answer_key_match:
            answer_key = answer_key_match.group(1)
            questions_text = text[:answer_key_match.start()]
        else:
            questions_text = text

        # =====================================================
        # Build Answer Lookup
        # =====================================================

        answer_lookup = {}

        for match in re.finditer(
            r'(\d+)\.(\d+)\.\s*(.*?)(?=\s+\d+\.\d+\.|\s+\d+\.\s+|$)',
            answer_key,
            flags=re.DOTALL
        ):
            q_no = match.group(1)
            option_no = match.group(2)
            answer_text = match.group(3).strip()

            answer_lookup[q_no] = {
                "type": "mcq",
                "option": option_no,
                "answer": answer_text
            }

        for match in re.finditer(
            r'(\d+)\.\s*(.*?)(?=\s+\d+\.\d+\.|\s+\d+\.\s+|$)',
            answer_key,
            flags=re.DOTALL
        ):
            q_no = match.group(1)

            if q_no in answer_lookup:
                continue

            answer_text = match.group(2).strip()

            answer_lookup[q_no] = {
                "type": "direct",
                "option": None,
                "answer": answer_text
            }

        # =====================================================
        # Extract Questions
        # =====================================================

        question_pattern = r'''
        (\d+)\.\s*ప్రశ్న\s*:\s*
        (.*?)
        \s*జవాబు\s*:\s*
        (.*?)
        (?=
        \s*\d+\.\s*ప్రశ్న\s*:
        |
        $
        )
        '''

        questions = re.findall(
            question_pattern,
            questions_text,
            flags=re.DOTALL | re.VERBOSE
        )

        # =====================================================
        # Create Chunks
        # =====================================================

        for q_no, question, answer_part in questions:

            question = question.strip()
            answer_part = answer_part.strip()

            # ---------------------------------------------
            # TYPE 2: Answer Key
            # ---------------------------------------------

            if "జవాబుల" in answer_part:

                final_answer = ""

                if q_no in answer_lookup:
                    final_answer = answer_lookup[q_no]["answer"]

                chunk = create_chunk(
                    chunk_counter,
                    kanda=current_kanda,
                    sarga=current_sarga,
                    adhyayamu=current_adhyayamu,
                    question_no=q_no,
                    question_type="answer_key",
                    question_te=question,
                    answer_te=final_answer,
                    page_no=f"{current_adhyayamu[-3:]}"
                )

                chunks.append(chunk)
                chunk_counter += 1
                continue

            # ---------------------------------------------
            # TYPE 1: MCQ
            # ---------------------------------------------

            option_count = len(re.findall(r'\d+\.', answer_part))

            if option_count >= 4:

                correct_answer = ""
                correct_option = None

                if q_no in answer_lookup:
                    correct_answer = answer_lookup[q_no]["answer"]
                    correct_option = answer_lookup[q_no]["option"]

                chunk = create_chunk(
                    chunk_counter,
                    kanda=current_kanda,
                    sarga=current_sarga,
                    adhyayamu=current_adhyayamu,
                    question_no=q_no,
                    question_type="mcq",
                    question_te=question,
                    answer_te=correct_answer,
                    page_no=f"{current_adhyayamu[-3:]}"
                )

                chunk["options_te"] = answer_part
                chunk["correct_option"] = correct_option

                chunks.append(chunk)
                chunk_counter += 1
                continue

            # ---------------------------------------------
            # TYPE 3: Descriptive
            # ---------------------------------------------

            chunk = create_chunk(
                chunk_counter,
                kanda=current_kanda,
                sarga=current_sarga,
                adhyayamu=current_adhyayamu,
                question_no=q_no,
                question_type="descriptive",
                question_te=question,
                answer_te=answer_part,
                page_no=f"{current_adhyayamu[-3:]}"
            )

            chunks.append(chunk)
            chunk_counter += 1


    # =====================================================
    # FINAL CHECK
    # =====================================================

    print("Total chunks:", len(chunks))

    print(
        json.dumps(
            chunks[0],
            ensure_ascii=False,
            indent=2
        )
    )

    return chunks