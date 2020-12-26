import os
from tkinter import * 
import tkinter.ttk as ttk
from tkinter import filedialog
import tkinter.messagebox as msgbox
from PIL import Image

root = Tk()
root.title('Nado Gui')

# 파일 추가 
def add_file():
    files = filedialog.askopenfilenames(title='이미지 파일을 선택하세요', \
        filetypes=(('PNG 파일', '*.png'), ('모든 파일', '*.*')), \
            initialdir=r'C:\Users\user\Desktop\python_practce\이미지 데모') # 최초에 C:/ 로 경로를 보여줌
            #최초에 사용자가 지정한 경로를 보여줌

    # 사용자가 선택한 파일 목록
    for file in files:
        list_file.insert(END, file)

def delete_file():
    #print(list_file.curselection())

    # list = [1, 2, 3, 4, 5]
    # list.reverse()
    for index in reversed(list_file.curselection()):
        list_file.delete(index)

# 저장 경로(폴더)
def browse_dest_path():
    forder_selective = filedialog.askdirectory()
    
    if forder_selective == '': # 사용자가 취소를 누를 때
        return
    txt_dest_path.delete(0, END)
    txt_dest_path.insert(0, forder_selective)

#이미지 통합
def merge_image():
    try:
        # 가로 넓이
        img_width = cmb_width.get()
        if img_width == '원본유지':
            img_width = -1 # -1 일 때는 원본 기준으로
        else:
            img_width = int(img_width)

        # 간격
        img_space = cmb_space.get()
        if img_space == '좁게':
            img_space = 30
        elif img_space == '보통':
            img_space = 60
        elif img_space == '넓게':
            img_space = 90
        else: # 없음
            img_space = 0

        # 포멧
        img_format = cmb_format.get().lower() #  소문자 변경

        ##########################################################

        images = [Image.open(x) for x in list_file.get(0, END)]

        # 이미지 사이즈를 리스트에 넣어 하나씩 처리
        image_sizes = [] # (width1, heigth1), (width2, height2) ...
        if img_width > -1:
            image_sizes = [(int(img_width), int(img_width * x.size[1] / x.size[0])) for x in images]
        else:
            # 원본 사이즈 사용
            image_sizes = [(x.size[0], x.size[1]) for x in images]

        # 계산식
        # 100 * 60 이미지 -> width 를 80으로 줄이면 height?
        # 원본 width : height = 수정된 width : 수정된 hegiht
        # 100 : 60 = 80 : ?
        # x : y = x' : y'
        # xy' = x'y
        # y' = x'y / x
        
        # 코드 대입
        # x = width = size[0]
        # y = height = size[1]
        # x' = img_width
        # y' = img_width * size[1] / size[0]

        # size -> size[0] : width, size[1] : height
        widths, heights = zip(*(image_sizes))

        max_width, total_heigth = max(widths), sum(heights)
        
        # 스케치북 준비
        if img_space > 0:
            total_heigth += (img_space * (len(images) - 1))

        result_image = Image.new('RGB', (max_width, total_heigth), (255, 255, 255)) # 배경 흰 색
        y_offset = 0 # y 위치

        for idx, img in enumerate(images):
            # width 가 원본이 아닐 경우, 이미지 크기 조정
            if img_width > -1:
                img = img.resize(image_sizes[idx])

            result_image.paste(img, (0,  y_offset))
            y_offset += (img.size[1] + img_space) # height 값 만큼을 더해줌 + 사용자가 지정한 간격

            progress = (idx + 1) / len(images) * 100 # 실제 퍼센트 정보를 계산 
            p_var.set(progress)
            progressbar.update()

        # 포멧 옵션 처리
        file_name = 'nado_photo.' + img_format
        dest_path = os.path.join(txt_dest_path.get(), file_name)
        result_image.save(dest_path)
        msgbox.showinfo('알림', '작업이 완료되었습니다.')
    
    except Exception as arr:
        msgbox.showwarning('에러', arr)

# 시작
def start():
    # 각 옵션들 값을 확인
    print('가로 넓이 옵션: ', cmb_width.get())
    print('간격', cmb_space.get())
    print('포멧', cmb_format.get())

    # 파일 목록 확인
    if list_file.size() == 0:
        msgbox.showwarning('경고', '이미지 파일을 추가하세요')
        return

    # 저장 경로 확인
    if len(txt_dest_path.get()) == 0:
        msgbox.showwarning('경고', '저장 경로를 선택하세요')
        return

    # 이미지 통합 작업
    merge_image()
    
# 파일 프레임(파일추가, 파일선택)
flie_frame = Frame(root)
flie_frame.pack(fill='x', padx=5, pady=5)

btn_add_flie = Button(flie_frame, padx=5, pady=5, width=12, text='파일 추가', command = add_file)
btn_add_flie.pack(side='left')

btn_del_flie = Button(flie_frame, padx=5, pady=5, width=12, text='선택삭제', command = delete_file)
btn_del_flie.pack(side='right')

# 리스트 프레임
list_frame = Frame(root)
list_frame.pack(fill='both', padx=5, pady=5)

scrollbar = Scrollbar(list_frame)
scrollbar.pack(side=RIGHT, fil=Y)

list_file = Listbox(list_frame, selectmode="extended", height=15, yscrollcommand=scrollbar.set)
list_file.pack(side='left', fill='both', expand=True)
scrollbar.config(command=list_file.yview)

# 저장 경로 프레임
path_frame = LabelFrame(root, text='저장경로')
path_frame.pack(fill='x', padx=5, pady=5, ipady=5)

txt_dest_path = Entry(path_frame)
txt_dest_path.pack(side='left', fill='x', expand=True, ipady=4, padx=5, pady=5) # 높이 변경

btn_dest_path = Button(path_frame, text='찾아보기', padx=5, pady=5, width=10, command=browse_dest_path)
btn_dest_path.pack(side='right', padx=5, pady=5)

# 옵션 프레임
frame_option = LabelFrame(root, text='옵션')
frame_option.pack(padx=5, pady=5)

# 1. 가로 넓이 옵션
# 가로 넓이 레이블
lbl_width = Label(frame_option, text='가로 넓이', width=8)
lbl_width.pack(side='left', padx=5, pady=5)

# 가로 넓이 콤보
opt_width = ['원본유지', '1024', '800', '640']
cmb_width = ttk.Combobox(frame_option, state='readonly', values=opt_width, width=10)
cmb_width.current(0)
cmb_width.pack(side='left', padx=5, pady=5)

# 2. 간격 옵션
# 간격 옵션 레이블
lbl_space = Label(frame_option, text='간격', width=8)
lbl_space.pack(side='left', padx=5, pady=5)

# 간격 옵션 콤보
opt_space = ['간격 없음', '좁게', '보통', '넓게']
cmb_space = ttk.Combobox(frame_option, state='readonly', values=opt_space, width=10)
cmb_space.current(0)
cmb_space.pack(side='left', padx=5, pady=5)

# 3. 파일 포멧 옵션
#  포멧 옵션 레이블
lbl_format = Label(frame_option, text='포멧', width=8)
lbl_format.pack(side='left', padx=5, pady=5)

# 포멧 옵션 콤보
opt_format = ['PNG', 'JPG', 'BMP']
cmb_format = ttk.Combobox(frame_option, state='readonly', values=opt_format, width=10)
cmb_format.current(0)
cmb_format.pack(side='left', padx=5, pady=5)

# 진행 상황 프로그레스 바 넣기
frame_progress = LabelFrame(root, text='진행상황')
frame_progress.pack(fill='x', padx=5, pady=5, ipady=5)

p_var = DoubleVar()
progressbar = ttk.Progressbar(frame_progress, maximum=100, variable=p_var)
progressbar.pack(fill='x', padx=5, pady=5, ipady=5)

# 실행 프레임 정보
frame_run = Frame(root)
frame_run.pack(fill='x', padx=5, pady=5)

btn_close = Button(frame_run, padx=5, pady=5, text='닫기', width=12, command=root.quit)
btn_close.pack(side='right', padx=5, pady=5)

btn_start = Button(frame_run, padx=5, pady=5, text='시작', width=12, command=start)
btn_start.pack(side='right', padx=5, pady=5)

root.resizable(False, False) # 창 크기 변경 불가
root.mainloop()