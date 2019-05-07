import tkinter as tk
import face_recognition
import cv2
import os
import time
from PIL import Image, ImageTk, ImageDraw, ImageFont
from tkinter import filedialog
from tkinter.simpledialog import askstring

file_dir = r'/home/neal/Picture/knownpeople'  # 已知人像的目录
main_dir = r'/home/neal/Picture/unknownpicture/hezhao.jpg'  # 主图人像文件

face_known = []  # 已知人脸
names = []  # 已知名字


def get_people(file_dir):  # 获取已知人名
    for root, dirt, file in os.walk(file_dir):
        return file


'''
def get_face(names):  # 已知人脸的数据
    pic_known = []
    print(names)
    for i in range(len(names)):
        pic_known.append(face_recognition.load_image_file(r'{}/{}'.format(file_dir, names[i])))
    return pic_known
'''


def list_found(people_name):  # 列出在图片中找到的人像
    # 图像加载
    for p in range(people_num):
        img_people = Image.open(r'/home/neal/Picture/unknownpicture/{}.jpg'.format(p)).resize((200, 200))
        photo_people.append(ImageTk.PhotoImage(img_people))

    for p in range(people_num):
        x = tk.Label(image=photo_people[p], width=200, height=200)
        label_people.append(tk.Label(image=photo_people[p], width=200, height=200))
        label_people[p].place(relx=1 / (2 * people_num + 1) * (2 * p + 1), rely=0.6)


def b_choose_main():
    global main_dir
    main_dir = filedialog.askopenfilename()  # 主图人脸的目录


def b_choose_dir():
    global file_dir
    file_dir = filedialog.askdirectory()  # 已知人脸的目录
    get_face()
    print(file_dir)


def main_reco():
    pic_main = face_recognition.load_image_file(main_dir)
    loc_main = face_recognition.face_locations(pic_main)

    global face_names
    global photo_main

    face_names.clear()
    face_main = face_recognition.face_encodings(pic_main)
    for face in face_main:
        name = 'Unknown'
        for i in range(len(face_known)):
            matches = face_recognition.compare_faces(face_known[i], face, tolerance=0.38)
            # print('matches:', matches)
            if True in matches:
                name = names[i]
        face_names.append(name)

    print(face_names)

    cv_img = cv2.imread(main_dir)
    text_size = 1
    ratio = 1
    if cv_img.shape[1] * 0.6 < cv_img.shape[1]:
        ratio = cv_img.shape[0] / 840
        text_size = cv_img.shape[0] / 720 + 1
    else:
        ratio = cv_img.shape[1] / 1400
        text_size = cv_img.shape[1] / 1200 + 1

    for i in range(len(face_names)):
        cv2.rectangle(cv_img, (loc_main[i][3] - 3, loc_main[i][0] - 3), (loc_main[i][1] + 2, loc_main[i][2] + 2),
                      (255, 0, 255), int(text_size))
        if face_names[i] != 'Unknown':
            cv2.putText(cv_img, face_names[i].split('.')[0], (loc_main[i][3] - 2, loc_main[i][0] - 20),
                        cv2.FONT_HERSHEY_DUPLEX, text_size / 2, (255, 0, 255), thickness=int(text_size))

    photo_main = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)).resize(
        (int(cv_img.shape[1] / ratio), int(cv_img.shape[0] / ratio))))
    label_main.config(image=photo_main)
    label_main.image = photo_main


def get_face():
    global face_known
    global names
    face_known.clear()
    names.clear()
    names = get_people(file_dir)  # 获取已知人脸
    names_num = len(names)
    n = 0
    while n < names_num:
        pic_known = face_recognition.load_image_file(r'{}/{}'.format(file_dir, names[n]))
        temp_face = face_recognition.face_encodings(pic_known)
        if len(temp_face) == 1:
            face_known.append(temp_face)
            n += 1
        else:
            print('{}无法找到主角人像'.format(names[n]))
            names.remove(names[n])
            names_num = len(names)

    print('names len:', len(names))
    print('faces len:', len(face_known))


windowWidth = 1920
windowHeight = 1080
screenWidth = 1920
screenHeight = 1080

people_num = 4  # 识别人数
label_people = []  # 人像显示
photo_people = []  # 人像数据

# 窗口的创建
geometrySize = '{}x{}+{}+{}'.format(windowWidth, windowHeight, int((screenWidth - windowWidth) / 2),
                                    int((screenHeight - windowHeight) / 2))
Window = tk.Tk()
Window.title('一个简单的窗口')
Window.geometry(geometrySize)

photo_main = None
face_names = []


def b_take_face():
    inp_name = askstring("请输入你的名字", "姓名：")
    print(inp_name)
    if inp_name is None or inp_name == '':
        return
    print('what', inp_name)
    video_capture = cv2.VideoCapture(0)
    cv2.namedWindow("press space to take, r to retake", cv2.WINDOW_AUTOSIZE)
    while True:
        ret, frame = video_capture.read()
        cv2.imshow("press space to take, r to retake", frame)
        k = cv2.waitKey(1)
        if k == 32:
            cv2.imshow("press space to take, r to retake", frame)
            k = cv2.waitKey(3000)
            if k != ord('r') and k != ord('R'):
                cv2.imwrite(file_dir + '/{}.jpg'.format(inp_name), frame)
                print(file_dir + '/{}.jpg'.format(inp_name))
                video_capture.release()
                cv2.destroyAllWindows()
                get_face()
                break
        if k == ord('Q') or k == ord('q'):
            video_capture.release()
            cv2.destroyAllWindows()
            return


def b_take_main():
    global main_dir
    video_capture = cv2.VideoCapture(0)
    cv2.namedWindow("press space to take, r to retake", cv2.WINDOW_AUTOSIZE)
    while True:
        ret, frame = video_capture.read()
        cv2.imshow("press space to take, r to retake", frame)
        k = cv2.waitKey(1)
        if k == 32:
            cv2.imshow("press space to take, r to retake", frame)
            k = cv2.waitKey(3000)
            if k != ord('r') and k != ord('R'):
                main_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                main_dir = os.path.dirname(main_dir) + '/{}.jpg'.format(main_time)
                cv2.imwrite(main_dir, frame)
                print(main_dir)
                break
        if k == ord('Q') or k == ord('q'):
            break
    video_capture.release()
    cv2.destroyAllWindows()


choose_main = tk.Button(Window, text='选择识别主图文件', command=b_choose_main)
choose_dir = tk.Button(Window, text='选择已知人脸目录', command=b_choose_dir)
take_main = tk.Button(Window, text='录入识别主图文件', command=b_take_main)
take_face = tk.Button(Window, text='录入人脸', command=b_take_face)
reco_main = tk.Button(Window, text='开始识别', command=main_reco)
label_main = tk.Label(Window, width=1200, height=720)

choose_main.place(relx=0.06, rely=0.1)
choose_dir.place(relx=0.06, rely=0.2)
take_face.place(relx=0.06, rely=0.3)
take_main.place(relx=0.06, rely=0.4)
reco_main.place(relx=0.06, rely=0.5)
label_main.place(relx=0.53 - 600 / windowWidth, rely=0.05)

Window.mainloop()
