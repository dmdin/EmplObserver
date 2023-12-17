from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware

import uvicorn
from datetime import date, datetime
import io
import csv
from model import UserStatisticItem
from ml_model import predict
import bisect
import os

from dotenv import load_dotenv

load_dotenv()

origins = os.getenv('ORIGINS')

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

def calc_stats(parsed_rows):
    start = min(parsed_rows, key=lambda x: x.startInterval).startInterval
    end = max(parsed_rows, key=lambda x: x.endInterval).endInterval

    total_messages_sent = sum([x.sent_messages_count for x in parsed_rows])
    total_messages_received = sum([x.received_messages_count for x in parsed_rows])
    total_messages_replied = sum([x.replied_messages_count for x in parsed_rows])
    total_messages_messages_outside_working_hours = sum([x.messages_outside_working_hours for x in parsed_rows])

    total_weeks = (end - start).days // 7

    return {
        "avg_messages_received_per_week": (total_messages_received*1.0)/total_messages_received,
        "avg_messages_sended_per_week": (total_messages_sent*1.0)/total_weeks,
        "sum_messages_sent": total_messages_sent,
        "sum_messages_sent_outside_working_hours": total_messages_messages_outside_working_hours,
        "percent_replied_messages": (total_messages_replied*100.0)/total_messages_received
    }


@app.post("/get_dates")
async def get_dates(file: UploadFile = File(...)):
    try:
        if file.content_type != "text/csv" and file.content_type != "application/vnd.ms-excel":
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
        
        parsed_rows = sorted(parsed_rows, key=lambda row: row.endInterval)

        return{
            "valid": True, 
            "message":"", 
            "min_date":min(parsed_rows, key=lambda x: x.endInterval).endInterval, 
            "max_date": max(parsed_rows, key=lambda x: x.endInterval).endInterval,
            "stats": calc_stats(parsed_rows)}
    except Exception as ex:
        print(ex)
        return {"valid": False, "message": f"Переданный файл невалиден"}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...), date_diff: date= Form(...)):
    try:
        if file.content_type != "text/csv" and file.content_type != "application/vnd.ms-excel":
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
        
        parsed_rows = sorted(parsed_rows, key=lambda row: row.endInterval)

        if len(parsed_rows) == 0:
            return {"valid": False, "message": "В файле нет записей"}

    if parsed_rows[0].endInterval > date_diff or parsed_rows[-1].endInterval < date_diff:
            return {"valid": False, "message": f"Выбранная дата разделения некорректна. Должны быть записи как больше, так и меньше выбранной даты"}

        index = 0

        for idx, row in enumerate(parsed_rows):
            if row.endInterval > date_diff:
                index = idx
                break

        left = parsed_rows[:index]
        right = parsed_rows[index:]

        return {"valid": True, "message": "", "result": predict(left, right)}
    except Exception as ex:
        print(ex)
        return {"valid": False, "message": f"Переданный файл невалиден"}
        

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
            replied_messages_count=int(r[5]),
            sent_characters_count=int(r[6]),
            days_between_received_and_read = 0,
            messages_outside_working_hours=int(r[7]),
            received_to_sent_ratio=float(r[8]),
            bytesReceivedToSentRatio=float(r[9]),
            messages_with_question_and_no_reply=int(r[10]),
            read_messages_later_than=int(r[11]),
            count_events=int(r[12]),
            startInterval=datetime.strptime(r[13], '%Y-%m-%d').date(),
            endInterval=datetime.strptime(r[14], '%Y-%m-%d').date()
            )

        
            rows.append(row)
        except Exception as ex:
            raise Exception(f'Ошибка парсинга строки: {i+1}. {ex}')


    return rows



def run_fastapi():
    uvicorn.run(app, host="0.0.0.0", port=8000)