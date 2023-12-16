from fastapi import FastAPI, UploadFile, File, Form
import uvicorn
from pydantic import BaseModel
from datetime import date
import io
import csv
from model import UserStatisticItem

app = FastAPI()

required_columns = [
    "sendMessagesCount",
    "receivedMessagesCount",
    "recipientCounts",
    "bccCount",
    "ccCount",
    "daysBetweenReceivedAndRead",
    "repliedMessagesCount",
    "sentCharactersCount",
    "messagesOutsideWorkingHours",
    "receivedToSentRatio",
    "bytesReceivedToSentRatio",
    "messagesWithQuestionAndNoReply",
    "readMessagesMoreThan4Hours",
    "startInterval",
    "endInterval"
]

@app.post("/upload")
async def upload_file(file: UploadFile = File(...), date_diff: date= Form(...)):
    print(file.content_type)
    if file.content_type != "text/csv":
        return {"valid": False, "message": "Неверный тип файла. Ожидается CSV."}
    
    contents = await file.read()

    csv_file = io.StringIO(contents.decode('utf-8'))

    reader = csv.reader(csv_file)
    headers = next(reader) 

    missed_columns = [x for x in required_columns if x not in headers]

    if len(missed_columns) > 0:
        return {"valid": False, "message": f"В файле не хватает следующих колонок: {','.join(missed_columns)}"}
    
    parsed_rows = parse_rows(reader)

    return len(parsed_rows)

def parse_rows(reader):
    rows = []

    for r in reader:
        row = UserStatisticItem(
            sent_messages_count=r[0],
            received_messages_count=r[1], 
            recipient_counts=r[2],
            bcc_count=r[3],
            cc_count=r[4], 
            days_between_received_and_read= r[5],
            replied_messages_count=r[6],
            sent_characters_count=r[7], 
            messages_outside_working_hours=r[8], 
            received_to_sent_ratio=r[9],
            bytesReceivedToSentRatio=r[10],
            messages_with_question_and_no_reply=r[11],
            read_messages_later_than=r[12])
        
        rows.append(row)

    return rows

    

def run_fastapi():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)