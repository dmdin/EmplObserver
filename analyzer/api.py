from fastapi import FastAPI, UploadFile, File, Form
import uvicorn
from datetime import date
import io
import csv
from model import UserStatisticItem
#from ml_model import predict

app = FastAPI()

required_columns = [
    "sendMessagesCount",
    "receivedMessagesCount",
    "recipientCounts",
    "bccCount",
    "ccCount",
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

    reader = csv.reader(csv_file,  delimiter=';')
    headers = next(reader) 

    missed_columns = [x for x in required_columns if x not in headers]

    if len(missed_columns) > 0:
        return {"valid": False, "message": f"В файле не хватает следующих колонок: {','.join(missed_columns)}"}
    
    parsed_rows = []
    try:
        parsed_rows = parse_rows(reader)
    except Exception as ex:
        return {"valid": False, "message": str(ex)}

    return {"valid": True, "message": "", "result": predict(parsed_rows)}

def parse_rows(reader):
    rows = []

    for i, r in enumerate(reader):
        try:
            row = UserStatisticItem(
            sent_messages_count=int(r[0]),
            received_messages_count=int(r[1]), 
            recipient_counts=int(r[2]),
            bcc_count=int(r[3]),
            cc_count=int(r[4]), 
            days_between_received_and_read= int(r[5]),
            replied_messages_count=int(r[6]),
            sent_characters_count=int(r[7]),
            messages_outside_working_hours=int(r[8]),
            received_to_sent_ratio=float(r[9]),
            bytesReceivedToSentRatio=float(r[10]),
            messages_with_question_and_no_reply=int(r[11]),
            read_messages_later_than=int(r[12]),
            count_events=int(r[13]))
        
            rows.append(row)
        except Exception as ex:
            raise Exception(f'Ошибка парсинга строки: {i+1}. {ex}')


    return rows



def run_fastapi():
    uvicorn.run(app, host="0.0.0.0", port=8001)