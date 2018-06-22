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


    Elements = Scrape.GetElements()

    MoreImageCount = 0
    #のちに新しいエレメントと比較するためにエレメントを保存。
    AllElements = Elements
    #ページ遷移は一度しか許されていない。
    while MoreImageCount < 2:
        for e in Elements:
            try:
                Scrape.ClickAndReset(e)
                GetSrcFlag = 0
            except:
                print("画像拡大できませんでした。")
                continue
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
            if Scrape.Count >= Scrape.NumImage:
                break

            #検索画面に戻る。戻らないと、縮小画像しか取得できないエラーがあようだ。
            Scrape.SwichWindow()
            time.sleep(1)
        #下にスクロールするにしたがって新しい画像が表示される。そのエレメントを取得。
        #これまでのエレメントと比較して新しいものだけを抜き出す。
        NewElements = Scrape.GetElements()
        Elements = [i for i in NewElements if (i in AllElements) is False ]
        if Scrape.Count >= Scrape.NumImage:
            print("指定枚数の取得を完了しました。")
            break

        #新しいエレメントが存在しない場合、そのページに画像が残っていない。
        #次のページへと遷移する。
        if Elements == []:
            try:
                Scrape.ShowMoreImage()
                print("画像をさらに表示しました。")
            except:
                print("さらに画像を表示することができませんでした。すべての結果を取得したか、何らかのエラーです。")
                break
            MoreImageCount +=1

    if Scrape.Count <= Scrape.NumImage:
        print("検索結果の取得完了しました。" + str(Scrape.Count) +"枚の画像を取得しました。")

    print("Complete! Please press any key to quit.")
    input()
    Scrape.Browser.quit()


except:
    print("ブラウザ起動後にエラー発生。")
    traceback.print_exc()
    print("Error! Please press any key to quit.")
    input()
    Scrape.Browser.quit()

