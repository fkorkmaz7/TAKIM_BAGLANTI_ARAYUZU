
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path
import sys
from threading import Thread
import time

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, PhotoImage
from ..utils.image_resize import image_resize
from ..interface.formats import SELECTABLE_FORMATS, JPG_exts
from ..interface.parameters_dialog import ParemetersDialog

from ..interface.widgets import CanvasButton, PauseButton
from tkinter.filedialog import askopenfilename, askdirectory
from pathlib import Path
from ..labeller.auto_labeller import AutoLabeller
from yolov5.utils.general import (cv2)
import os
from PIL import ImageTk, Image
from numpy import asarray
from yolov5.utils.plots import Annotator, colors

from ..utils.params_saver import ParamsSaver
import numpy as np

dt_frame = Path(__file__).parent/"detect_frame.jpg"

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = "./assets"


def relative_to_assets(path: str) -> Path:
    return Path(__file__).parent / ASSETS_PATH / Path(path)


class AutoLabellerUI:
    labeller: AutoLabeller = None
    after = None
    label_mapper = 'label_map_uyz_2023.txt'
    classes_txt = 'classes.txt'
    check_inilebilir = True
    hide_vid = True
    resize_image = True
    target_path = ""
    pause=False
    def __init__(self) -> None:
        self.window = Tk()
        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()
        self.window.geometry(f"{self.screen_width}x{self.screen_height}")
        # setting attribute
        self.window.attributes('-fullscreen', True)
        self.canvas = Canvas(
            self.window,
            bg="#000000",
            height=self.screen_height,
            width=self.screen_width,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)
        image_image_1 = PhotoImage(
            file=relative_to_assets("image_1.png"))
        self.current_image = self.canvas.create_image(
            960.0,
            540.0,
            image=image_image_1
        )
        
        self.pause_button=PauseButton(
            self.canvas, 42, 38.0, value=self.pause)
        self.pause_button.show(False)
        self.stop_button=CanvasButton(
            self.canvas, 258, 38, self.stop, text="Durdur")
        self.stop_button.show(False)
        self.selectbtn = CanvasButton(
            self.canvas, 42, 38, self.select_file, text="Dosya Seç")
        self.selectfolderbtn = CanvasButton(
            self.canvas, 258, 38, self.select_folder, text="Klasör Seç")
        self.labelbtn = CanvasButton(
            self.canvas, 474, 38, self.labelling_thread, text="Başlat")
        self.parbtn = CanvasButton(
            self.canvas, 690, 38, self.open_paremetre_dialog, text="Parametreler")
        self.destroy_button=CanvasButton(
            self.canvas, 1824.0, 36.0, self.destroy, text="X", back_image="button_background2.png")
        
        
        self.minimize_button=CanvasButton(
            self.canvas, 1745.0, 36.0, self.minimize, text="-", back_image="button_background2.png")
        """ self.tracker_checkbox = CanvasCheckBox(
            self.canvas, 46, 139, True, text="Tracker Kullan")
        self.sahi_checkbox = CanvasCheckBox(
            self.canvas, 268, 139, True, text="SAHI Kullan") """
        image_image_2 = PhotoImage(
            file=relative_to_assets("info_back.png"))
        self.info_back=self.canvas.create_image(
            150.0,
            991.0,
            image=image_image_2
        )

        self.infolabel = self.canvas.create_text(
            77.0,
            977.0,
            anchor="nw",
            text="0/0",
            fill="#FFFFFF",
            font=("Inter Black", 24 * -1)
        )


        self.stop=False
        self.labelbtn.show(False)

        def fun(event):
            if(event.keysym=='h'):
                self.hideall(not self.is_show_elements)

        self.window.bind("<KeyRelease>", fun)
        self.window.mainloop()
        self.window.resizable(False, False)

        self.window.mainloop()
    is_show_elements=True

    def hideall(self, value):
        self.is_show_elements=value
        self.pause_button.show(value)
        self.stop_button.show(value)
        self.selectbtn .show(value)
        self.selectfolderbtn.show(value)
        self.labelbtn.show(value)
        self.parbtn.show(value)
        self.destroy_button.show(value)
        self.minimize_button.show(value)
    def destroy(self):
        if self.after is not None:
            self.window.after_cancel(self.after)
        sys.exit()
    
    def stop(self):
        self.stop=True

    def minimize(self):
        self.window.iconify()
    
    def show_elements(self, value):
        is_show_elements=value
        self.selectbtn.show(value)
        self.selectfolderbtn.show(value)
        self.labelbtn.show(value)
        """ self.tracker_checkbox.show(value)
        self.sahi_checkbox.show(value) """
        #self.parbtn.show(value)
        self.pause_button.show(not value)
        self.stop_button.show(not value)

    def open_paremetre_dialog(self):
        d = ParemetersDialog(self.window, "Parametreleri Düzenle")

    def select_file(self):
        # show an "Open" dialog box and return the path to the selected file
        self.target_path = askopenfilename(filetypes=SELECTABLE_FORMATS)
        if self.target_path != "":
            self.labelbtn.show(True)
            if not len([x for x in JPG_exts if x in self.target_path]) > 0:
                f = cv2.VideoCapture(self.target_path)
                rval, frame = f.read()
                f.release()
            else:
                frame = cv2.imread(self.target_path)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            self.change_image(frame=frame)

    def select_folder(self):
        # show an "Open" dialog box and return the path to the selected file
        self.target_path = askdirectory()
        if self.target_path != "":
            self.labelbtn.show(True)
            self.files = os.listdir(self.target_path)
            self.files = [os.path.join(self.target_path, f)
                          for f in self.files]  # add path to each file
            paramsaver=ParamsSaver()
            self.params=paramsaver.getParams()
            if self.params.sort_files_with_time.get():
                self.files.sort(key=lambda x: os.path.getmtime(x) )
            frame = cv2.imread(self.files[0])
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.change_image(frame=frame)

    def change_image(self, frame):
        frame = image_resize(frame, width=self.screen_width, height=self.screen_height)
        img = Image.fromarray(frame)
        self.current_image_image = ImageTk.PhotoImage(image=img)
        self.canvas.itemconfig(
            self.current_image, image=self.current_image_image)

    def calculate_object_count_on_center(self, cocos):
        (h, w) = self.labeller.predictor.frame.shape[:2]
        center_bbox = [0.25, 0.25, 0.75, 0.75]
        corner_indexes = [(0, 1), (0, 3), (2, 1), (2, 3)]
        center_count = 0
        for coco in cocos:
            bbox = list(coco["bbox"])
            bbox[2] = bbox[0]+bbox[2]
            bbox[3] = bbox[1]+bbox[3]
            for corner_index in corner_indexes:
                corner = (bbox[corner_index[0]], bbox[corner_index[1]])
                if center_bbox[0] <= corner[0] <= center_bbox[2] and center_bbox[1] <= corner[1] <= center_bbox[3]:
                    center_count += 1
                    break
        return center_count

    def draw_box(self, cocos, info):
        frame = self.labeller.predictor.frame
        self.canvas.itemconfig(self.infolabel, text=info)
        im0 = asarray(frame)
        im0 = cv2.cvtColor(im0, cv2.COLOR_BGR2RGB)
        annotator = Annotator(
            im0, line_width=1, example=str(self.labeller.names))
        (h, w) = im0.shape[:2]
        for coco in cocos:
            bbox = list(coco["bbox"])
            bbox[2] = bbox[0]+bbox[2]
            bbox[3] = bbox[1]+bbox[3]
            bbox=[a*(frame.shape[1] if i%2==0 else frame.shape[0]) for i, a in enumerate(bbox)]
            c = int(coco["category_id"])  # integer class
            label = f'{coco["id"]} {coco["category_name"]} {coco["score"]:.2f} {coco["inilebilir"]}'
            color = colors(c, False)
            annotator.box_label(bbox, label, color=color)
        # Stream results
        count = self.calculate_object_count_on_center(cocos)
        bbox = [w/4, h/4, w*3/4, h*3/4]
        annotator.box_label(bbox, f"Center {count}", (0, 0, 0))
        im0 = annotator.result()
        self.after = self.window.after(50, self.change_image, im0)

    def labelling_thread(self):
        try:
            self.main_thread = Thread(
                target=self.start_labelling, daemon=True).start()
        except (KeyboardInterrupt, SystemExit):
            self.destroy()




    def isStop(self):
        if self.stop:
            self.stop=False
            return True
        return False


    def detect(self, img:str|np.ndarray, dest:str, save_txt=True, save_img=False, message=""):
        t1=time.perf_counter()
        paramsaver=ParamsSaver()
        self.params=paramsaver.getParams()
        if type(img) is not np.ndarray:
            img=cv2.imread(img)
        self.labeller.detect(dest, img, save_txt)
        if self.params.resize_img.get() and img.shape[0] > self.params.resize_height.get():
            img = image_resize(img, height=self.params.resize_height.get(), width=self.params.resize_width.get())
        cocos = self.labeller.detect(
                    img=img, source=dest, save_txt=save_txt)
        t2=time.perf_counter()
        self.draw_box(cocos, f"{message}   {(t2-t1):.2f}s")
        if save_img:
            cv2.imwrite(dest, img)
        return cocos
        
    def start_video_labelling(self):
        paramsaver=ParamsSaver()
        self.params=paramsaver.getParams()
        output_folder = str(Path(self.target_path).parent)
        if self.params.save.video_fps_to_save.get() <= 0:
            self.params.save.video_fps_to_save.set(1)

        vidcap = cv2.VideoCapture(self.target_path)
        fps = round(vidcap.get(cv2.CAP_PROP_FPS))
        length = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
        video_name = Path(self.target_path).stem
        count = 0
        image_save_folder = os.path.join(output_folder, video_name, "images")
        label_save_folder = os.path.join(output_folder, video_name, "labels")
        Path(image_save_folder).mkdir(exist_ok=True, parents=True)
        Path(label_save_folder).mkdir(exist_ok=True, parents=True)

        t_image_per_second = self.params.save.video_fps_to_save.get() if fps > self.params.save.video_fps_to_save.get() else fps
        success = True

        self.labeller = AutoLabeller(labels_output_folder=label_save_folder)
        while success and not self.isStop():  # resimleri bitene kadar devam eder
            if self.pause_button.pause:
                continue
            save = count % round(fps/t_image_per_second) == 0 or count+1==length or not self.params.save.decrease_video_frame.get()
            success, img = vidcap.read()
            if not success:
                continue
            enter= save  or not save and not  self.params.save.pass_detection_not_saved_frames.get()
            if enter:
                save_image_path = os.path.join(
                    image_save_folder, f"frame_{str(count).zfill(6)}.jpg")
                self.detect(img, save_image_path, save, save, f"{count+1}/{length}")
            count += 1


    def start_folder_labelling(self):
        label_save_folder = self.target_path.replace(
            self.target_path.split("/")[-1], "labels")
        self.labeller = AutoLabeller(labels_output_folder=label_save_folder)
        for count, file in enumerate(self.files):
            while self.pause_button.pause and not self.stop:
                continue
            if self.isStop():
                break
            self.detect(file, file, True, False, f"{count+1}/{len(self.files)}")

    def start_file_labelling(self):
        label_save_folder = os.path.join(
            str(Path(self.target_path).parent.parent), "labels")
        self.labeller = AutoLabeller(labels_output_folder=label_save_folder)
        self.detect(self.target_path, self.target_path, True, False, "Bitti.")

    def start_labelling(self):
        if self.target_path == "":
            return
        self.show_elements(False)
        if Path(self.target_path).is_file():
            if len([x for x in JPG_exts if x in self.target_path]) > 0:
                self.start_file_labelling()
            else:
                self.start_video_labelling()
        else:
            self.start_folder_labelling()
        self.pause_button.onValue(False)
        self.show_elements(True)
