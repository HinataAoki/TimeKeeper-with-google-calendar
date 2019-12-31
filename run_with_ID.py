from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import tkinter
import time

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def main(title,starttime,finishtime):
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    event = {
      'summary': title,
      'location': 'Japan',
      'description': '',
      'start': {
        'dateTime': starttime.isoformat(),
        'timeZone': 'Japan',
      },
      'end': {
        'dateTime': finishtime.isoformat(),
        'timeZone': 'Japan',
      },
    }

    event = service.events().insert(calendarId='自分のIDを入力(IDの取得の仕方はほかのページで)',
                                    body=event).execute()
    print (event['id'])


#tkinter表示設定
tki = tkinter.Tk()
tki.geometry('300x200')
tki.title('TimeKeeper')

#時刻取得
nowtime=datetime.datetime.now()

#btnクリック時イベント
pin=False
text="START"
def dd():
    nowtime=datetime.datetime.now()
    global pin,text,starttime,finishtime
    if pin==False:
        pin=True
        text="FINISH"
        lbl_1["text"]=text
        btn["text"]=text
        timelabel["text"]=nowtime.strftime('%Y/%m/%d %H:%M:%S')
        starttime=nowtime
    else:
        wyd=txt_1.get()
        if wyd=="":
            timelabel["text"]="Please input title"
        else:
            pin=False
            text="START"
            lbl_1["text"]=text
            btn["text"]=text
            timelabel["text"]=nowtime.strftime('%Y/%m/%d %H:%M:%S')
            finishtime=nowtime
            title=wyd
            txt_1.delete(0,tkinter.END)
            main(title,starttime,finishtime)


# ラベル
lbl_1 = tkinter.Label(text=text)
lbl_1.place(x=30, y=70)

# テキストボックス
txt_1 = tkinter.Entry(width=20)
txt_1.place(x=90, y=70)

#時刻表記
timelabel = tkinter.Label(text=nowtime.strftime('%Y/%m/%d %H:%M:%S'))
timelabel.place(x=90,y=100)

# ボタン
btn = tkinter.Button(tki, text=text, command=dd)
btn.place(x=140, y=170)

# 画面をそのまま表示
if __name__=="__main__":
    tki.mainloop()
