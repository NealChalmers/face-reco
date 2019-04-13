import tkinter as tk
import face_recognition
import cv2
import os
from PIL import Image, ImageTk, ImageDraw, ImageFont
from tkinter import filedialog

file_dir = r'/home/neal/Picture/rrr'  # 已知人像的目录
main_dir = r'/home/neal/Picture/unknownpicture/hezhao.jpg'  # 主图人像文件


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

face_known = []  # 已知人脸
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

face_cor = []  # 主图人脸坐标
pic_main = face_recognition.load_image_file(main_dir)
loc_main = face_recognition.face_locations(pic_main)
for i in loc_main:
    face_cor.append(i)

face_names = []
face_main = face_recognition.face_encodings(pic_main)
for face in face_main:
    name = 'Unknown'
    for i in range(len(face_known)):
        matches = face_recognition.compare_faces(face_known[i], face, tolerance=0.39)
        # print('matches:', matches)
        if True in matches:
            name = names[i]
    face_names.append(name)

print(face_names)

#print(filedialog.askopenfilename())

cv_img = cv2.imread(main_dir)
text_size = 1
ratio = 1
if cv_img.shape[1] * 0.6 < cv_img.shape[1]:
    ratio = cv_img.shape[0] / 600
    text_size = cv_img.shape[0] / 720 + 1
else:
    ratio = cv_img.shape[1] / 1000
    text_size = cv_img.shape[1] / 1200 + 1

for i in range(len(face_names)):
    cv2.rectangle(cv_img, (loc_main[i][3] - 3, loc_main[i][0] - 3), (loc_main[i][1] + 2, loc_main[i][2] + 2),
                  (255, 0, 255), int(text_size))
    if face_names[i] != 'Unknown':
        cv2.putText(cv_img, face_names[i].split('.')[0], (loc_main[i][3] - 2, loc_main[i][0] - 20),
                    cv2.FONT_HERSHEY_DUPLEX, text_size / 2, (255, 0, 255), thickness=int(text_size))
# cv2.imwrite(r'/home/neal/Picture/unknownpicture/3_3.jpg', cv_img)

# img_main = Image.open(main_dir).resize((700, 420))  # 主图的读取与显示

photo_main = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)).resize(
    (int(cv_img.shape[1] / ratio), int(cv_img.shape[0] / ratio))))
label_main = tk.Label(image=photo_main, width=1100, height=660)
label_main.place(relx=0.5 - 550 / windowWidth, rely=0.02)

img_known = []
photo_known = []
label_known = []
label_name = []

face_names_show = face_names.copy()
while face_names_show.count('Unknown') != 0:
    face_names_show.remove('Unknown')

for i in range(len(face_names_show)):
    img_known.append(Image.open('{}/{}'.format(file_dir, face_names_show[i])).resize((200, 250)))
    photo_known.append(ImageTk.PhotoImage(img_known[i]))
    label_known.append(tk.Label(image=photo_known[i], width=200, height=250))
    label_known[i].place(relx=1 / (len(face_names_show) * 2 + 1) * (1 + i * 2), rely=0.72)
    label_name.append(tk.Label(text=face_names_show[i].split('.')[0], font=('Arial', 15, 'normal')))
    label_name[i].place(relx=1 / (len(face_names_show) * 2 + 1) * (1 + i * 2), rely=0.68)

Window.mainloop()
