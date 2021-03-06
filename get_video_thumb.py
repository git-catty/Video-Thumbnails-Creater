# !/usr/bin/env python
# -*- coding:utf-8 -*-

# 作者：AMII
# 时间：20210310
# 更新内容：竖向视频默认5张每行，新增繁体、日语支持，韩语日后更新，其中124行的TW-Kai-98_1.ttf 字体请自行搜索下载或替换为其他字体，用于繁体字及日语的识别。

import datetime
import fractions
import os
import re
import time
import ffmpeg
from io import BytesIO
from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont
Image.MAX_IMAGE_PIXELS = None

alldirs = []
logfilename = 'get_video_thumb_log.json'
logpath = 'log\\'
fontpath = 'fonts\\'
now = time.strftime('%Y-%m-%d_%H-%M-%S',time.localtime(time.time()))
fontType = os.path.join(fontpath, "杨任东竹石体-Heavy.ttf")
fontTTF = TTFont(fontType)
uniMap = fontTTF['cmap'].tables[0].ttFont.getBestCmap()

def main():
    alldirs.append(rootpath)
    get_dirs(rootpath)
    get_dirs_check(alldirs)
    # print (alldirs)
    save_log(logpath + logfilename,'a+',now + '  ' + rootpath + ':{\n')
    for x in range(len(alldirs)):
        begin(alldirs[x])
    save_log(logpath + logfilename,'a+','}\n')

def get_dirs(root_path):    #遍历目录
    dirs = os.scandir(root_path)
    # print (root_path)
    for x in dirs:
        if x.is_dir():
            if x.name != '$RECYCLE.BIN' and x.name != 'System Volume Information':
                alldirs.append(root_path + '\\' + x.name)
                get_dirs(root_path + '\\' + x.name)

def get_dirs_check(alldirs):    #遍历目录检查机制
    if re.search('\\\\\\\\',alldirs[-1]):
        for x in range(len(alldirs)):
            temp = alldirs[x].replace('\\\\','\\')
            alldirs[x] = temp

def begin(path):        #开始程序
    files,nfiles,path_files = get_list(path)
    for x in range(len(files)):
        if os.path.exists(path + '\\' + nfiles[x] + '_thumb.jpg'):      #判断是否已有缩略图
            print ('已有缩略图____',nfiles[x],'\n')
            continue
        try:
            if get_thumb(files[x],nfiles[x],path_files[x],path):        #跳过长度过短的视频
                save_log(logpath + logfilename,'a+','0,less],\n')
                print ('视频长度小于10s，跳过____',files[x])
                continue
            save_log(logpath + logfilename,'a+','\"Done\"],\n')
        except:
            save_log(logpath + 'get_video_thumb_errlog_' + str(now) + '.txt','a+',path_files[x] + '\n')
            save_log(logpath + logfilename,'a+','0,\"err\"],\n')
            print ('\n【【【Error File】】】',path_files[x],'\n')    #运行出错，保留日志

def get_thumb(file,nfile,path_file,path):       #获取视频截图并生成缩略图总图
    col_def = int(col_default)
    save_log(logpath + logfilename,'a+','    [\"' + path_file + '\",')
    temp = 0
    ftype = check_font(nfile)
    xs = width_default/3840             #比例系数
    tsize_info = int((64 * xs)//1)      #视频信息文字大小
    tsize_filename = int((60 * xs)//1)  #文件名文字大小
    tsize_time = int((36 * xs)//1)      #时间信息文字大小
    logo = "-- by AMII"
    byte,size,bl,width,height,fps,sec,vtime = get_info(path_file)
    # print(byte,size,bl,width,height,fps,sec,vtime)
    img = Image.open(BytesIO(get_frame(path_file, sec//2)))
    if (img.size[0]!=width):            #判断长宽是否颠倒并纠正
        temp = width
        width = height
        height = temp
    width_each_pic = int((width_default/col_def)//1)            #定义每张缩略图宽度
    height_each_pic = int(((height*width_each_pic)/width)//1)       #定义每张缩略图高度
    if (sec < 10):                                                  #判断时间长短
        return 1
    info = '文件名 :\n' + '大    小 :  ' + size + ' (' + \
           str(byte) + ' Byte)\n' + '长宽比 :  ' + str(width) + 'x' + \
           str(height) + ' (' + bl + '), FPS: ' + fps + '\n时    长 :  ' + vtime
    info_name = '文件名 :  '
    tname = path + '\\' + nfile + '_thumb.jpg'
    num, row, jg = get_row(sec)
    lw = 0                                      #左上角坐标宽度
    lh = int((300 * xs)//1)                     #左上角坐标高度
    height_full = height_each_pic * row + lh    #总图高度
    if (height_each_pic/width_each_pic) > 1 and (col_def <= 4):
        col_def += 1
        width_each_pic = int((width_default/col_def)//1)
        height_each_pic = int(((height*width_each_pic)/width)//1)
        row = int((num + col_def -1) // col_def)
        height_full = height_each_pic * row + lh
    while (height_full > 65530):
        col_def += 1
        width_each_pic = int((width_default/col_def)//1)
        height_each_pic = int(((height*width_each_pic)/width)//1)
        row = int((num + col_def -1) // col_def)
        height_full = height_each_pic * row + lh
    save_log(logpath + logfilename,'a+',str(sec) + ',\"' + vtime + '\",' + str(num) + ',')
    print ('图片数：',num,'  行数：',row,'  ',file)
    fullimg = Image.new('RGB',(width_default,height_full),"white")      #新建总图底图
    
    vinfo_img = Image.new('RGB',(width_default,lh),"white")             #新建信息条底图
    font = ImageFont.truetype(fontpath + '杨任东竹石体-Heavy.ttf',tsize_info)
    font_filename = ImageFont.truetype(fontpath + 'TW-Kai-98_1.ttf',tsize_filename)
    name_size = font.getsize(info_name)
    filename_size = font_filename.getsize(file)
    if ftype:
        while (filename_size[0] > (width_default - name_size[0] - int((40*xs)//1))):        #文件名过长缩小字体
            tsize_filename -= 2
            font_filename = ImageFont.truetype(fontpath + 'TW-Kai-98_1.ttf',tsize_filename) #【【【【【【【【【【该字体需自行下载或更换，用于繁体及日语标题】】】】】】】】】】】
            filename_size = font_filename.getsize(file)
    else :
        filename_size = font.getsize(file)
        tsize_filename = tsize_info
        font_filename = ImageFont.truetype(fontpath + '杨任东竹石体-Heavy.ttf',tsize_filename)
        while (filename_size[0] > (width_default - name_size[0] - int((40*xs)//1))):        #文件名过长缩小字体
            tsize_filename -= 2
            font_filename = ImageFont.truetype(fontpath + '杨任东竹石体-Heavy.ttf',tsize_filename)
            filename_size = font_filename.getsize(file)
    draw = ImageDraw.Draw(vinfo_img)
    logo_size = font.getsize(logo)
    if ftype:
        draw.text((int((40*xs)//1) + name_size[0],int((20*xs)//1)),text=file,fill=(0,0,0),font=font_filename,stroke_width=1,stroke_fill="black")
    else :
        draw.text((int((40*xs)//1) + name_size[0],int((20*xs)//1)),text=file,fill=(0,0,0),font=font_filename)
    draw.text((int((40*xs)//1),int((20*xs)//1)),text=info,fill=(0,0,0),font=font)       #绘制信息条，上下同
    draw.text((width_default - logo_size[0] - 10, lh - logo_size[1] - 10), text=logo, fill=(0, 0, 0), font=font)
    fullimg.paste(vinfo_img,(0,0))              #粘贴信息条至总图
    for i in range(num):                        #循环截取视频截图并粘贴至总图
        # print (i)
        save_log(logpath + logfilename,'a+',str(i) + ',')
        time = jg * i + jg
        if (sec - time < 3):                    #截图时间与视频总时长过于接近时回退以避免截图出错
            time -= 3
        # if (time < 26):                 ####【调试】####
        #     continue
        #    time -= (jg/2)//1
        tt = '0' + str(datetime.timedelta(seconds=time))
        frame = get_frame(path_file, time)      #截图
        img = Image.open(BytesIO(frame)).resize((width_each_pic,height_each_pic),Image.ANTIALIAS)
        font = ImageFont.truetype(fontpath + '杨任东竹石体-Heavy.ttf',tsize_time)
        draw = ImageDraw.Draw(img)              #下为绘制截图时间至截图
        time_size = font.getsize(tt)
        draw.text((width_each_pic - time_size[0] - 10, 2),text=tt,fill="white",font=font,stroke_width=3,stroke_fill="black")
        fullimg.paste(img,(lw,lh))              #粘贴截图至总图
        lw += width_each_pic
        if ((i+1)%col_def==0):              #判断是否需要换行
            lh += height_each_pic
            lw = 0
    fullimg.save(tname, quality = 80)           #保存总图
    print ('Well Done~~~~  \n')                 #搞定~~

def check_font(file):       #检查字体是否能显示文件名(单确认版)
    for x in file:
        if (ord(x) < 128):
            continue
        if not (ord(x) in uniMap.keys()):
            return True
    return False

def get_frame(path_file,time):      #获并返回取帧
    out, err = (
        ffmpeg.input(path_file, ss = time)
              .output('pipe:', vframes=1, format='image2', vcodec='mjpeg')
              .run(capture_stdout=True)
    )
    return out

def get_info(path_file):        #获取并返回视频基本信息
    vv = 0
    probe = ffmpeg.probe(path_file)
    for x in range(6):
        if (probe['streams'][x]['codec_type']=='video'):
            vv = x
            break
    bytes = re.sub(r"(\d)(?=(\d\d\d)+(?!\d))", r"\1,", probe['format']['size'])
    size = hum_convert(int(probe['format']['size']))
    bl = str(fractions.Fraction(str(probe['streams'][vv]['width']) + '/' + str(probe['streams'][vv]['height'])))
    width = probe['streams'][vv]['width']
    height = probe['streams'][vv]['height']
    fpss = probe['streams'][vv]['r_frame_rate'].split('/')
    fps = str(round(int(fpss[0])/int(fpss[1]),2))
    tim = int(float(probe['format']['duration'])//1)
    time = '0' + str(datetime.timedelta(seconds=tim))
    return (bytes,size,bl,width,height,fps,tim,time)

def get_list(path):     #获取并返回目录下视频文件及目录等
    all_files = os.listdir(path)
    rule = r"\.(avi|wmv|wmp|wm|asf|mpg|mpeg|mpe|m1v|m2v|mpv2|mp2v|ts|tp|tpr|trp|vob|ogm|ogv|mp4|m4v|m4p|m4b|3gp|3gpp|3g2|3gp2|mkv|rm|ram|rmvb|rpm|flv|swf|mov|qt|nsv|dpg|m2ts|m2t|mts|dvr-ms|k3g|skm|evo|nsr|amv|divx|webm|wtv|f4v|mxf)$"
    path_file_list = []
    file_list = []
    nfile_list = []
    for files in all_files:
        if re.search(rule, files, re.IGNORECASE):
            file_list.append(files)
            nfile_list.append(os.path.splitext(files)[0])
            path_file_list.append(path + '\\' + files)
    return (file_list,nfile_list,path_file_list)

def hum_convert(value):     #格式化并返回文件大小
    units = [" B", " KB", " MB", " GB", " TB", " PB"]
    size = 1024.0
    for i in range(len(units)):
        if (value / size) < 1:
            return "%.2f%s" % (value, units[i])
        value = value / size

def get_row(sec):       #设定并返回图片个数、行数、间隔
    jg = 0
    num = 0
    if (sec <= 120):
        jg = s2
    elif (sec <= 601):
        jg = s10
    elif (sec <= 1801):
        jg = s30
    elif (sec <= 3601):
        jg = s60
    else :
        jg = sot
    num = sec//jg
    row = int((num + col_default -1) // col_default)
    return (num, row, jg)

def save_log(logname,mode,mess):     #写入日志
    with open (logname,mode,encoding='utf-8') as f:
        f.write(mess)

if __name__ == '__main__':
    if not os.path.exists(logpath):
        os.makedirs(logpath)
    rootpath = input('请输入文件夹地址：')
    col_default = int(input('你想一行几张图片（默认横版4,竖版5）：') or 4)
    width_default = int(input('缩略图宽度（默认3840）：') or 3840)
    print('默认间隔2分钟以下：2s，10分钟：5s，30分钟：15s，1小时：30s，其他：60s【输入数字修改，回车跳过】')
    s2 = int(input('2分钟内间隔：') or 2)
    s10 = int(input('10分钟内间隔：') or 5)
    s30 = int(input('30分钟内间隔：') or 15)
    s60 = int(input('60分钟内间隔：') or 30)
    sot = int(input('大于60分钟间隔：') or 60)
    main()
