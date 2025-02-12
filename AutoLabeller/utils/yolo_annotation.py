class YoloAnnotation():
    def __init__(self, txt_path) -> None:
        self.txt_path = txt_path
        self.text = ""

    def addObject(self, cls, x_ctr, y_ctr, width, height):
        object_line = f'{cls} {x_ctr} {y_ctr} {width} {height}\n'
        self.text = f"{self.text}{object_line}"

    def write_output(self):
        with open(self.txt_path, 'w') as f:
            f.write(f'{self.text}')
            f.close()
    
    def write_cocos(self, cocos):
        for coco in cocos:
            bbox = list(coco["bbox"])
            bbox[2] = bbox[0]+bbox[2]
            bbox[3] = bbox[1]+bbox[3]
            xmin = bbox[0]
            ymin = bbox[1]
            xmax = bbox[2]
            ymax = bbox[3]
            o_w = xmax-xmin
            o_h = ymax-ymin
            c_x = (xmin+xmax)/2
            c_y = (ymin+ymax)/2
            self.addObject(coco["category_id"], c_x, c_y, o_w, o_h)
        self.write_output()