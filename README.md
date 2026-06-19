Steps to run this pipeline:
Step 1> Create environment [Download relevant packages and set them up]
Step 2> Api key is asked when running the program, this make it safe and easy for everyone.
Step 3> After downloading relevant packages and this repository , Run python main.py.
This will run the program and provide us with a rag_chunk.jsonl file, which has the ouput for all chunks in following manner-

OUTPUT FORMAT:
{
  "chunk_id": "chunk_4",
  "kanda": "Bala Kandamu",
  "sarga": "1-6",
  "adhyayamu": "1",
  "question_no": "4",
  "question_type": "descriptive",
  "question_te": "...",     #prasna in telugu 
  "answer_te": "...",       #javabu in telugu
  "question_en": "...",    #contains the question translation
  "answer_en": "...",      #conatins the answer translation
  "options_te": [ "వైవశవిత మనువును", "చత్రుముఖ బ్రహ్మను", "మరీచిని","నారద మహర్షిని"],  #available only for questions with options
  "correct_option": "2", #To get the correct answer[Given in seperate javabulu coloumn] for mcq type questions
  "correct_answer_te": "చత్రుముఖ బ్రహ్మను", #Correct answer[Given in seperate javabulu coloumn] for 1 word answer type question
  "entities": [...],  # For indepth understanding
  "relations": [...], # Finding relationships between things
  "metadata": {
    "source_language": "te",
    "target_language": "en",
    "book": "RAMAYANA PRASHNAVALI",
    "author":,
    "page no":,
     
  }
}

This format is chossen because there is not much relationship between the chunks, if a person ask question regarding page numbers, topics , vague questions, the model will not have any problems with tackling those questions. It can easily understand the relationship between each question with entities and relation coloumn.
Data parsing is then based on the recurring patterns in the pdf, instead of relying on ai , this decreased the reliance on ai .
