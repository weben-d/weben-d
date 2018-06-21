#画像検索（現在のところはGoogle画像検索）を利用して画像をスクレイプするアプリです。
#APIを使用せず、celeniumを利用しています。chromedriverはwindows32bit版を利用しています。
#他OSでの実行時にはそれ用のchromedriverを用意してください。
#また、最新版のchromeとchromedriverの組み合わせのみ動作するようです。


from ScrapeGoogleImage import ScrapeGoogleImage
import urllib.error
import traceback
import time

Scrape = ScrapeGoogleImage()

Scrape.GetQuery()
Scrape.MakeDirectory()

Scrape.OpenBrowser()
try:
    Scrape.SearchImage()

    while True:
        Elements = Scrape.GetElements()
        for e in Elements:


            Scrape.ClickAndReset(e)
            GetSrcFlag = 0
            try:
                GetSrcFlag = Scrape.GetSrc(0)
            except:
                Scrape.SrcCount[0] = -1
                traceback.print_exc()
                print("原寸大画像取得中にエラーが発生しました。")
            try:
                #print("縮小画像の取得開始。")
                GetSrcFlag = Scrape.GetSrc(1)
            except:
                traceback.print_exc()
                print("縮小画像の取得中にエラーが発生しました。")

            if GetSrcFlag == 2:
                print("次の画像に移ります。")
                continue
            #print("GetSrcFlag",GetSrcFlag)
            #print("SrcCount",Scrape.SrcCount)
            print(str(Scrape.Count + 1) + "枚目取得開始。")

            try:
                Scrape.DonloadAndIdentify(0)
            except (urllib.error.HTTPError,TypeError):
                if Scrape.Src[0] is not None: print("原寸大画像の取得が禁止されているため、縮小画像を取得。")
                Scrape.DonloadAndIdentify(1)

            except:
                traceback.print_exc()
                print(str(Scrape.Count+1)+ "枚目ダウンロードできませんでした。")


            if Scrape.Count >= Scrape.NumImage:break
            time.sleep(1)


        if Scrape.Count >= Scrape.NumImage:
            print("目標枚数の収集が完了しました。")
            break
            #ページ遷移するときのためのbreak



    print("Complete! Please press any key to quit.")
    input()
    Scrape.Browser.quit()


except:
    print("ブラウザ起動後にエラー発生。")
    traceback.print_exc()
    print("Error! Please press any key to quit.")
    input()
    Scrape.Browser.quit()



"""
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

print("Complete! Please press any key to exit.")

input()
Browser.quit()
"""
