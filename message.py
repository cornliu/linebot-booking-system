#這些是LINE官方開放的套件組合透過import來套用這個檔案上
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *
from Function import *

def alone_or_group():
    message = TemplateSendMessage(
        alt_text='個練or團練',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url='https://i.imgur.com/IyuRa0H.jpg',
                    title='個練',
                    text='個練只能預約隔一天的空檔喔',
                    actions=[
                        MessageTemplateAction(
                            label='選擇',
                            text='我想要個練'
                        ),
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://i.imgur.com/1Tsnrnq.jpg',
                    title='團練',
                    text='團練可以預約七天之內的空檔',
                    actions=[
                        MessageTemplateAction(
                            label='選擇',
                            text='我想要團練'
                        ),
                    ]
                ),
            ]
        )
    )
    return message

def how_long():
    message = TemplateSendMessage(
        alt_text='請問要借幾小時',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/0/08/Un1.svg/1200px-Un1.svg.png',
                    title='1小時',
                    text='個練50元、團練150元',
                    actions=[
                        MessageTemplateAction(
                            label='選擇',
                            text='1小時'
                        ),
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/Deux.svg/1024px-Deux.svg.png',
                    title='2小時',
                    text='個練100元、團練300元',
                    actions=[
                        MessageTemplateAction(
                            label='選擇',
                            text='2小時'
                        ),
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Trois.svg/1024px-Trois.svg.png',
                    title='3小時',
                    text='個練150元、團練450元',
                    actions=[
                        MessageTemplateAction(
                            label='選擇',
                            text='3小時'
                        ),
                    ]
                ),
            ]
        )
    )
    return message

def what_your_name():
    return TextSendMessage(text='請輸入您的學號以及姓名。格式:學號_姓名。範例:b07901193_林曉正')

def exitbut():
    return TextSendMessage(
                text='exit()輸入成功，請輸入任意字以重新進行預約', 
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=MessageAction(label='繼續', text='繼續')
                        )
                    ]))

def which_day(a_or_g="group"):
    days = []
    quickreply = []
    days.append(localtimetostr(time.localtime(time.time()+8*3600)))
    if a_or_g == "alone":
        days.append(next_day(days[0]))
    elif a_or_g == "group":
        for i in range(7):
            days.append(next_day(days[i]))
    for i in range(len(days)):
        quickreply.append(
            QuickReplyButton(
                action=MessageAction(label=str(days[i]), text=str(days[i]))
            )
        )
    return TextSendMessage(text='請選擇日期', quick_reply=QuickReply(items=quickreply))     

def pick_a_time():
    availabletime = find_available(Globals.state[-2] ,Globals.state[-1])
    if len(availabletime)>13:
        return TextSendMessage(text='明天全天都有空，請問要預約什麼時候開始個練呢？(請輸入24小時制)輸入格式範例：8.')
    quickreplylist = []
    for i in range(len(availabletime)):
        quickreplylist.append(
            QuickReplyButton(
                action=MessageAction(label=str(availabletime[i])+".", text=str(availabletime[i])+".")
            )
        )
    return TextSendMessage(text='請問要預約什麼時間開始',quick_reply=QuickReply(items=quickreplylist))

def booking():
    col = app.sheet.col_values(1)
    # simple verify if the id valid
    id_name = Globals.state[-1].split('_')
    if len(id_name[0]) < 6: return  TextSendMessage(text='請輸入您的學號_姓名')
    for i in Globals.special_string:
        if i in id_name[0] or i in id_name[1]: return TextSendMessage(text='請輸入您的學號_姓名')
    for i in Globals.numbers: 
        if i in id_name[1]: return TextSendMessage(text='請輸入您的學號_姓名')
    ###################
    if Globals.state[2] in col:
        pos = col.index(Globals.state[2])
        row = app.sheet.row_values(pos+1)
        for i in range(Globals.state[3]):
            app.sheet.update_cell(pos+1, Globals.state[4]-6+i, Globals.state[-1]+"_"+Globals.state[1])
        Globals.state.clear()
        return TextSendMessage(
                text='預約成功，輸入任意字以繼續', 
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=MessageAction(label='繼續', text='繼續')
                        )
                    ]))
    else:
        Globals.state.clear()
        return TextSendMessage(text='發生錯誤，請重新試試')

def erase():
    erased = Globals.state[3].split('到')
    start, end = int(erased[0]), int(erased[1])
    col = app.sheet.col_values(1)
    if Globals.state[2] in col:
        pos = col.index(Globals.state[2])
        row = app.sheet.row_values(pos+1)
        for i in range(end-start):
            app.sheet.update_cell(pos+1, start-6+i,"")
    Globals.state.clear()
    return TextSendMessage(
                text='取消預約成功，輸入任意字以繼續', 
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=MessageAction(label='繼續', text='繼續')
                        )
                    ]))


def starting():
    return TextSendMessage(
                text='請問您需要什麼樣的服務呢？\n注意：如果linebot行為怪怪的，可能是因為有人跟你同時在操作預約系統。避開後打exit()便可以刷新正常使用了\n如果您輸入錯誤也可以藉由輸入exit()來重新開始預約喔！', 
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=MessageAction(label='建立預約', text='建立預約')
                        ),
                        QuickReplyButton(
                            action=MessageAction(label='取消預約', text='取消預約')
                        )
                    ]))

def cancelling():
    col = app.sheet.col_values(1)
    counter = 0
    appointment = {}
    if Globals.state[2] in col:
        pos = col.index(Globals.state[2])
        row = app.sheet.row_values(pos+1)
        print(row)
        row.extend([""]*(15-len(row)))
        print(len(row))
        for i in range(1,len(row)):
            if '_' in row[i]:
                row_split = row[i].split('_')
                row[i] = row_split[0]+'_'+row_split[1]
            if Globals.state[1] == row[i]:
                counter += 1
            if (Globals.state[1] != row[i]) and (Globals.state[1] == row[i-1]):
                appointment[i-counter] = counter
                print("a")
                print(i)
                print(counter)
                counter = 0
            if (i == len(row)-1) and (counter != 0):
                appointment[i-counter+1] = counter
                print("b")
                print(i)
                print(counter)
    replylist = []
    for keys in appointment:
        replylist.append(
            QuickReplyButton(
                action=MessageAction(label='%i到%i'%(keys+7, keys+7+appointment[keys]), text='%i到%i'%(keys+7, keys+7+appointment[keys]))
            )
        )
    if len(replylist) == 0:
        Globals.state.clear()
        return TextSendMessage(
                text='今天無您的預約，輸入任意字詞重新開始', 
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=MessageAction(label='繼續', text='繼續')
                        )
                    ]))
    else:
        return TextSendMessage(
                    text='您預約了下列時段，請問您要取消甚麼時段呢？', 
                    quick_reply=QuickReply(
                        items=replylist
                    ))
    
# def cancelling(alist,number):
#     counter = 0
#     appointment = {}
#     for i in range(1,len(alist)):
#         if number == alist[i]:
#             counter += 1
#         if (number != alist[i]) and (number == alist[i-1]):
#             appointment[i-counter] = counter
#             counter = 0
#         if (i == (len(alist)-1)) and (counter != 0):
#             appointment[i-counter] = counter
#     return appointment
    
