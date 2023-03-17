import os
import time
import cv2
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
from tkinter import * # __all__
from tkinter import filedialog
import tkinter
from PIL import Image
import numpy as np
from PIL import ImageTk
from playsound import playsound
#-*- coding: utf-8 -*-

#pyinstaller 파일이름.py    //exe파일만들기
#pip install pyinstaller
#pip3 install opencv-python numpy
#pip3 install image
#pip3 install pillow
    #-> PIL
    
# playsound("sound.mp3" ,False)
    
    

root = Tk()
root.title("K-MOVE_5_Parasite")
root.iconbitmap(default='test.ico')

canvas = Canvas(root,width=540, height=340, bd=2)
canvas.pack(expand=True, fill="both",anchor="center")
image2 = PhotoImage(file="")


master1=""  #전역변수. 파일위치를 탐색한다
master2=""  #전역변수. 텍스트 위치를 탐색한다.
master3=""  #전역변스. 출력위치를 정할때 사용
master4=""  #전역변수. 저장파일이름 정할때 사용
glo_imgSize_x = 0
glo_imgSize_y = 0
glo_imgName = ""
def to_bin(data):
    """데이터를 이진 형태의 문자로 바꾼다."""
    if isinstance(data, str):
        return ''.join([ format(ord(i), "08b") for i in data ])
    elif isinstance(data, bytes) or isinstance(data, np.ndarray):
        return [ format(i, "08b") for i in data ]
    elif isinstance(data, int) or isinstance(data, np.uint8):
        return format(data, "08b")
    else:
        raise TypeError("타입이 올바르지 않음")



def encode(image_name, secret_data):
    # 이미지를 읽는다
    image = cv2.imread(image_name)
    # 읽은 이미지에서 몇 바이트를 사용할수있는지 계산한다.
    n_bytes = image.shape[0] * image.shape[1] * 3 // 8
    print("사용가능 바이트:", n_bytes)
    if len(secret_data) > n_bytes:
        raise ValueError("바이트 부족. 이미지를 더 크게하거나, 문자를 줄일것")
    
    # 정지기준 코드.
    secret_data += "====="
    data_index = 0
    # 숨길 문서를 바이너리 코드로 변경(2진화)
    binary_secret_data = to_bin(secret_data)
    # 숨길 데이터 크기 확인
    data_len = len(binary_secret_data)
    for row in image:
        for pixel in row:
            # RGB값을 이진 형식으로 변환
            r, g, b = to_bin(pixel)
            # if 저장할 비트가 남아있는 경우 = 최하위 비트 수정
            # 각 마지막 비트를 삭제하고 해당 데이터를 수정할 데이터로 채움
            if data_index < data_len:
                # 최하위 레드 비트 수정
                pixel[0] = int(r[:-1] + binary_secret_data[data_index], 2)
                data_index += 1
            if data_index < data_len:
                # 최하위 그린 비트 수정
                pixel[1] = int(g[:-1] + binary_secret_data[data_index], 2)
                data_index += 1
            if data_index < data_len:
                # 최하위 블루 비트 수정
                pixel[2] = int(b[:-1] + binary_secret_data[data_index], 2)
                data_index += 1
            # 인코딩 완료후 for종료
            if data_index >= data_len:
                break
    return image

def decode(image_name):
    
    # 이미지를 읽음
    image = cv2.imread(image_name)
    binary_data = ""
    for row in image:
        for pixel in row:
            r, g, b = to_bin(pixel)
            binary_data += r[-1]
            binary_data += g[-1]
            binary_data += b[-1]
    # 8비트 단위로 나눔
    all_bytes = [ binary_data[i: i+8] for i in range(0, len(binary_data), 8) ]
    # 나눈 비트를 문자로 변환
    decoded_data = ""
    for byte in all_bytes:
        decoded_data += chr(int(byte, 2))
        if decoded_data[-5:] == "=====":
                #위에서 설정한 정지기준 코드를 만나게되면 정지
            break
    return decoded_data[:-5]

#인코더 디코더 실행
def merge_codoe():
    
    global master4

    input_image = master1
    
    sumdir=str(master3+"/"+master4+".png")


    
    output_image = sumdir
    secret_data = master2

    if code_var.get()==1:
        encoded_image = encode(image_name=input_image, secret_data=secret_data)
        cv2.imwrite(output_image, encoded_image)    #  앞의 이름으로 뒤에값을 저장 
        return
    if code_var.get()==2:
        decoded_data = decode(input_image)
        print("숨겨진 문자 : ", decoded_data)

        return
# 파일 추가
def add_file():
    files = filedialog.askopenfilenames(title="이미지 파일을 선택하세요", \
        filetypes=(("PNG 파일", "*.png"), ("모든 파일", "*.*")), \
        initialdir=r"C:\Users\Nadocoding\Desktop\PythonWorkspace")
        # 최초에 사용자가 지정한 경로를 보여줌
    
    # 사용자가 선택한 파일 목록
    global master1  ## master1을 글로벌 수정이 가능하게 변경
    for file in files:
        list_file.insert(END, file)

        master1=str(file)
        

        
    #파일 사이즈 확인부 
    global glo_imgSize_x
    global glo_imgSize_y
    global glo_imgName
    # 이미지를 읽는다
    image = cv2.imread(master1)

    glo_imgName = image 
    sizeA,sizeB,sizeC = image.shape
    glo_imgSize_x = sizeB
    glo_imgSize_y = sizeA

        
        
    #이미지 출력부(코드 줄일수 있긴함)
    global image2


    # while문을 사용하여 이미지를 "적당" 한 크기로 줄인다.

    resize_x_sosu = glo_imgSize_x
    resize_y_sosu = glo_imgSize_y
    if(resize_x_sosu > 540 or resize_y_sosu > 340):
        while resize_x_sosu > 540 or resize_y_sosu > 340:
        
            resize_x_sosu = resize_x_sosu*0.99
            resize_y_sosu = resize_y_sosu*0.99

    elif(resize_x_sosu < 540 and resize_y_sosu < 340):
        while resize_x_sosu < 540 and resize_y_sosu < 340:
            resize_x_sosu = resize_x_sosu*1.01
            resize_y_sosu = resize_y_sosu*1.01

            
    resize_x = int(resize_x_sosu)
    resize_y = int(resize_y_sosu)
    

    image2 = Image.open(master1)
    image2 = image2.resize((resize_x, resize_y), Image.ANTIALIAS)
    
    image2 =  ImageTk.PhotoImage(image2)

    canvas.create_image(0,0,anchor=NW, image=image2)




# 저장 경로 (폴더)
def browse_dest_path():
    global master3
    folder_selected = filedialog.askdirectory()
    if folder_selected == "": # 사용자가 취소를 누를 때

        return

    master3=folder_selected
    txt_dest_path.delete(0, END)
    txt_dest_path.insert(0, folder_selected)

# 텍스트 인풋
def input_text(): 

    global master2
    master2=txt.get("1.0" , END)
   
# 파일이름세이브
def filename_save():
    global master4
    master4=save.get("1.0" , END)
    master4 = master4.rstrip('\n')

    
    

  
   
    
# 진행상황  
def progress_update():
    for i in range(1, 101):
        time.sleep(0.01)

        p_var.set(i)
        progress_bar.update()
        
#리셋
def reset():
    txt.delete("1.0","end")
    save.delete("1.0","end")
    list_file.delete(0, END)
    txt_dest_path.delete(0, END)
    


# 시작
def start():

    # 인코더 디코더 확인
    if code_var.get()==0:
        msgbox.showwarning("경고", "방식을 선택해주세요")
        return
    # 파일 목록 확인
    if list_file.size() == 0:
        msgbox.showwarning("경고", "이미지 파일을 추가하세요")
        return

    # 저장 경로 확인
    if len(txt_dest_path.get()) == 0 and code_var.get()==1:
        msgbox.showwarning("경고", "저장 경로를 선택하세요")
        return

    # 인코더 디코더 싱행작업
    input_text()
    filename_save()

    if(code_var.get()==2):
        print("디코딩 중--")
    
    progress_update()
    merge_codoe()
    if(code_var.get()==1):
        print("인코딩완료")
    elif(code_var.get()==2):
        print("디코딩완료")
    reset()


# 선택 프레임(인코더 디코더 선택)
choice_frame = LabelFrame(root, text="Choise")
choice_frame.pack(fill="both", padx=5, pady=5, ipady=5)

code_var = IntVar()
btn_code1 = Radiobutton(choice_frame, text="Encode", value=1, variable=code_var)
btn_code2 = Radiobutton(choice_frame, text="Decode", value=2, variable=code_var)

btn_code1.pack()
btn_code2.pack()









# 리스트 프레임
list_frame = LabelFrame(root, text="파일선택")
list_frame.pack(fill="x", padx=5, pady=5, ipady=5)
list_file = Entry(list_frame)
list_file.pack(side="left", fill="x", expand=True, padx=5, pady=5, ipady=4)


# 파일 프레임 (파일 추가, 선택 삭제)
#file_frame = Frame(root)
#file_frame.pack(fill="x", padx=5, pady=5) # 간격 띄우기

btn_add_file = Button(list_frame,  width=10, text="파일선택", command=add_file)
btn_add_file.pack(side="left", padx=5, pady=5)
txt_dest_path = Entry(list_frame)
txt_dest_path.pack(side="left", fill="x", expand=True, padx=5, pady=5, ipady=4) # 높이 변경

btn_dest_path = Button(list_frame, text="저장경로", width=10, command=browse_dest_path)
btn_dest_path.pack(side="right", padx=5, pady=5)



# 텍스트 프레임 -> input_text()
text_frame = LabelFrame(root, text="글씨를 적어주세요")
text_frame.pack(fill="x", padx=5, pady=5, ipady=5)

#inout txt
txt = Text(text_frame, width=70, height=5)
txt.pack(side="left")


# 파일이름저장 프레임
filename_save_frame = LabelFrame(root, text="저장할 파일명을 적어주세요")
filename_save_frame.pack(fill="x", padx=5, pady=5, ipady=5)

#input filename
save = Text(filename_save_frame, width=70, height=1)
save.pack(side="left", fill="x", expand=True, padx=5, pady=5, ipady=4) # 높이 변경

# 진행 상황 Progress Bar
frame_progress = LabelFrame(root, text="진행상황")
frame_progress.pack(fill="x", padx=5, pady=5, ipady=5)

p_var = DoubleVar()
progress_bar = ttk.Progressbar(frame_progress, maximum=100, variable=p_var)
progress_bar.pack(fill="x", padx=5, pady=5)

# 실행 프레임
frame_run = Frame(root)
frame_run.pack(fill="x", padx=5, pady=5)


choice_frame3 = Label(frame_run , 
text="Song Gyeongheon / Kim Minki  \n Choe Hojong / Lee Jinseop / Jo Jeongun"
,fg="#6F6FF2", font = ("HY견고딕", 8))
choice_frame3.pack(side= "left")



btn_close = Button(frame_run, padx=5, pady=5, text="닫기", width=12, command=root.quit)
btn_close.pack(side="right", padx=5, pady=5)

btn_start = Button(frame_run, padx=5, pady=5, text="시작", width=12, command=start)
btn_start.pack(side="right", padx=5, pady=5)




root.resizable(False, False)
root.mainloop()