#画像検索（現在のところはGoogle画像検索）を利用して画像をスクレイプするアプリです。
#APIを使用せず、celeniumを利用しています。chromedriverはwindows32bit版を利用しています。
#他OSでの実行時にはそれ用のchromedriverを用意してください。
#また、最新版のchromeとchromedriverの組み合わせのみ動作するようです。


from selenium import webdriver
import selenium.common
import os
import time
import platform
import sys
import traceback
import urllib.request
import urllib.error
import imghdr
import shutil

print("検索するキーワードを入れてください。")
Query = input()


'''
print("svgを含みますか?y or n")
while True:
    if (input() == "y"):
        SvgFlag = 1
        break
    elif(input() == "n"):
        SvgFlag = 0
        break
    else:
        print("yかnで入力してください。")
'''

SavePath = "data/images/"
# 対象ディレクトリがない場合に製作する
if os.path.exists("data/images/")==False:os.mkdir("data/images/")
DownloadPath = "data/download/"
if os.path.exists("data/download/")==False:os.mkdir("data/download/")

TmpFileName = "TmpFile"

#前回のTmpファイルが残っていれば削除する。
if os.path.exists(DownloadPath+TmpFileName)==True:os.remove(DownloadPath+TmpFileName)

if os.path.exists(SavePath+Query) ==True:
    while True:
        print("すでに同じQueryの検索結果が存在します。既存の結果を削除しますか？(削除しない場合、既存の結果が上書きされます。) y or n")
        if (input()=="y"):
            shutil.rmtree(SavePath+Query)
            break
        elif (input()=="n"):
            break
        else:print("yかnで入力してください。")
os.mkdir(SavePath+Query)

#OSを識別し、それに応じてchromedriverを切り替える。
#先頭に現在のディレクトリが来るのでpath先頭には/が必要。
CurrentPath = os.path.dirname(os.path.abspath(__file__))
if platform.system() == "Windows":
    DriverPath = "/data/chromedriver.exe"
elif platform.system() == "Darwin":
    DriverPath = "/data/chromedriver_mac"
elif platform.system() == "Linux":
    DriverPath = "/data/chromedriver_linux"
else:
    print("OSを識別できません。プログラムを終了します。")
    sys.exit()


Browser = webdriver.Chrome(executable_path = CurrentPath + DriverPath)
GoogleURL = "https://www.google.co.jp/imghp?hl=ja"
Browser.get(GoogleURL)
print("ブラウザ開いた")

try:
    #検索窓にクエリを打ち込み、検索ボタンを押す。
    SearchWindow = Browser.find_element_by_css_selector("#lst-ib").send_keys(Query)
    Browser.find_element_by_css_selector("#mKlEF > span > svg").click()


    #検索結果から画像のエレメントを取得。
    Elements = Browser.find_elements_by_class_name("rg_ic")


    #取得したエレメント(通常100件)について処理を行う。
    Count = 0
    OldSrcList = []
    OldSrcList_mut = []
    for e in Elements:
        #input()


        #画像をクリックして拡大。
        e.click()


        #irc_miが原寸画像のリンク、irc_mutが縮小画像のリンクである。
        #ものによってはmiが存在しないため、mutのほうを取得する。
        #また、irc_miのクラス名を持つエレメントは通常3つ存在する。
        #そのうち一つが現在選択している画像のもので、残りは過去に選択した画像である。
        #そのため3つのエレメントのうち、取得に成功(Noneでない)かつ新しいものからダウンロードする。

        ImageElements = Browser.find_elements_by_class_name("irc_mi")
        ImageElements_mut = Browser.find_elements_by_class_name("irc_mut")
        SrcList = []
        SrcList_mut = []
        Src = None
        Src_mut = None

        SrcCount = 0
        SrcCount_mut = 0


        try:
            for i in ImageElements:
                #print("i",i)
                iSrc = i.get_attribute("src")
                SrcList.append(iSrc)

            #print("SrcList_len",len(SrcList))
            for s in SrcList:
                if (s in OldSrcList) is False and (s is not None):
                    Src = s
                    SrcCount +=1
            if SrcCount == 0:
                print("原寸大画像見つかりませんでした。")
        except:
            print("原寸大画像の取得中にエラーが発生しました。")

        try:
            for i in ImageElements_mut:
                # print("i",i)
                iSrc_mut = i.get_attribute("src")
                SrcList_mut.append(iSrc_mut)


            # print("SrcList_len",len(SrcList))
            for s in SrcList_mut:
                if (s in OldSrcList_mut) is False and (s is not None):
                    Src_mut = s
                    SrcCount_mut += 1
        except:
            print("縮小画像の取得中にエラーが発生しました。")
        if SrcCount_mut == 0 and SrcCount == 0:
            print("見つかりませんでした")
            continue
        OldSrcList = SrcList
        OldSrcList_mut = SrcList_mut

        #print("SrcCount",SrcCount)
        #print("Src",Src)




        '''
        try:
            ImageElement = Browser.find_elements_by_class_name("irc_mi")[1]
            Src = ImageElement.get_attribute("src")
            if Src == None or Src == OldSrc:
                ImageElement = Browser.find_elements_by_class_name("irc_mut")[1]
                #print("irc_mut" + str(ImageElement))
                Src = ImageElement.get_attribute("src")
                if Src == None or Src == OldSrc:
                    print("irc_mutでもsrc取得できませんでした。")
        except:
            print("Src取得中にエラー発生")
            traceback.print_exc()
        OldSrc = Src
        '''
        print(str(Count + 1) + "枚目取得開始。")
        #print(Src)

        #いったんtmpファイルとしてダウンロードしたうえで拡張子を判別する。
        #確認した拡張子に基づき画像ファイルをリネームして移動。
        try:
            #print(DownloadPath + TmpFileName)


            #urllib.request.urlretrieve(Src,"/data/download/TmpFile")
            urllib.request.urlretrieve(Src,DownloadPath + TmpFileName)
            #print("ダウンロードした")
            Extension = imghdr.what(DownloadPath+TmpFileName,h=None)


            #svg形式をimghdrで認識できないので、個別に対応。なお()をつけないとSrc==Trueかの判別式になるみたい。
            if ("svg" in Src) == True :
                Extension = "svg"
                print("Extensionを", Extension, "に変更")
            if Extension is not None:
                os.rename(DownloadPath+TmpFileName, SavePath+Query+"/"+Query + "_" + str(Count+1)+ "."+ Extension)
                print(str(Count + 1) + "枚目取得成功。")
                Count += 1

        except (urllib.error.HTTPError,TypeError):

            if Src is not None:print("原寸大画像の取得が禁止されているため、縮小画像を取得。")
            urllib.request.urlretrieve(Src_mut, DownloadPath + TmpFileName)
            Extension = imghdr.what(DownloadPath+TmpFileName,h=None)


            #svg形式をimghdrで認識できないので、個別に対応。なお()をつけないとSrc==Trueかの判別式になるみたい。
            if ("svg" in Src_mut) == True :
                Extension = "svg"
                print("Extensionを", Extension, "に変更")
            if Extension is not None:
                os.rename(DownloadPath+TmpFileName, SavePath+Query+"/"+Query + "_" + str(Count+1)+ "."+ Extension)
                print(str(Count + 1) + "枚目取得成功。")
                Count += 1

        except:
            traceback.print_exc()
            print(str(Count+1)+ "枚目ダウンロードできませんでした。")


        time.sleep(1)







except:
    print("ブラウザ起動後にエラー発生。")
    traceback.print_exc()

print("Complete! Please press any key.")

Browser.quit()