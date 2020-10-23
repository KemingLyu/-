
import turtle
from turtle import Turtle

#from turtle import _Screen #, _Root


from tkinter import *
import random
import time

SCREENWIDTH=  640 
SCREENHEIGHT= 480

MINSTICKS= 7
MAXSTICKS= 31

HUNIT= SCREENHEIGHT // 12
WUNIT= SCREENWIDTH // ((MAXSTICKS // 5) * 11 + (MAXSTICKS % 5) * 2)

SCOLOR= (255,   0,   0)  #'red'   #(63, 63, 31)    # 原始棒子色
HCOLOR= (200, 255, 200)  #'green' #(255, 204, 204) # 玩家拿走棒子的顏色
COLOR=  (200, 200, 255)  #'blue'  #(204, 204, 255) # 電腦拿走棒子的顏色

def randomrow():
    #每一排中隨機產生棒子數
    return random.randint(MINSTICKS, MAXSTICKS)

def computerzug(state):
    '''
    此程式的必勝演算法
    '''
    nRows= len(state)  #指定排數
    xored= 0
    for s in state:
        #每一排進行判斷
        xored ^= s
    
    move= randommove(state) # 不經考慮，隨機出手。
    
    if xored != 0: 
        # 此情形，我方有機會勝利，
        # 做一個動作，使得 接下來的 xored ==0，則敵方必敗。    
        for z in range(nRows):
            s = state[z] ^ xored
            if s <= state[z]:
                move= (z, s)
                break        
    return move

def randommove(state):
    '''
    隨機出手，但需要設定一些條件
    '''
    nRows= len(state) 
    m = max(state) # m為最多那排
    while True:
        z = random.randint(0, nRows-1)
        if state[z] > (m > 1):
            break
    #為何要寫 m > 1 ??
    #好像是...
    #根據上面的迴圈，原作者似乎不想讓那排如果只有一個時，
    #被隨機挑走，以增加遊戲難度
    rand = random.randint(m > 1, state[z]-1)
    
    move = (z, rand)
    return move




class NimGame:
    '''
    整個遊戲主要的class，
    包含了執行此遊戲的函數，以及實例化其他class
    將整個程式連結起來
    '''
    CREATED= 0
    RUNNING= 1
    OVER=    2
    
    def __init__(self, nRows=3, mode=0):#, screen= None):#, level= True):
        '''
        遊戲主要執行的函數
        '''
        self.state=      NimGame.CREATED
        self.nRows=      nRows
        self.mode=       mode
        
        
        '''
        這裡將原本的turtle模組跟Tk模組合併，
        防止遊戲跑出兩個視窗。

        將turtle內部的_Screen類別內的_root屬性
        設定為Tk介面，
        再將screen屬性設定為turtle內的Screen類別
        
        turtle.Screen() 很厲害，它會自動偵測是否已被執行過，
        若是如此，則不會在生出新的，只會把舊的丟出來。
        
        '''

        self.screen=      turtle.Screen()      
        self.tk=          self.screen.getcanvas().master        
        
        
        #
        # 為了讓修改排數時清空畫面再從新開始遊戲
        #


        self.screen.clear()



        game= self # 在這個 class NimGame 裡面， self 就是 game

        #實例化按鈕
        self.level=      Level(game, x=300, y=-250)
        self.hint=       Hint(game, x=-300, y=-250)
        
        self.menu=      CvMenu(game)

        

        
        #實例化MVC
        self.model=      NimModel(game)
        self.view=       NimView(game)
        self.controller= NimController(game)

class NimModel:
    '''
    Model(模型)
    這個class是遊戲的核心，為資料及演算法存放處，
    也連結了其他兩個主要的class
    '''
    def __init__(self, game):
        self.game = game

    def setup(self):
        
        self.nRows= self.game.nRows  # 遊戲的列數可受控制，並記下來，
        
        if self.game.state not in [NimGame.CREATED, NimGame.OVER]:
            return
        '''
        #self.sticks = [randomrow(), randomrow(), randomrow()]
        self.sticks= []
        for i in range(self.nRows):
            self.sticks += [randomrow()]
        '''
        self.player = 0
        self.winner = None
        self.game.state = NimGame.RUNNING
        
        
        #self.menu = self.game.menu

        #設定當遊戲開始則無法設定排數
        #self.menu.entryconfig('棒子排數', state='disabled')

        #當遊戲結束則可以改排數
        #self.menu.entryconfig('棒子排數', state='normal') 

        #self.sticks = [randomrow(), randomrow(), randomrow()]
        self.sticks= []
        for i in range(self.nRows):
            self.sticks += [randomrow()]
        
        self.game.view.setup()
        
        #遊戲開始按鈕出現
        self.game.level.st()
        self.game.hint.st()
        
        
    # 遞迴
    def move(self, row, col):
        maxspalte = self.sticks[row]
        self.sticks[row] = col
        if self.game.mode == 0:
        
        
            self.game.view.notify_move(row, col, maxspalte, self.player)
            if self.game_over():
                self.game.state = NimGame.OVER
                self.winner = self.player         # 勝者在此決定
                self.game.view.notify_over()
                
                
                #遊戲結束按鈕隱藏
                self.game.hint.ht()
                self.game.level.ht()
            
            
            elif self.player == 0:
                self.player = 1

                #偵測智商
                if self.game.level.value == True:
                    row, col = computerzug(self.sticks)
                else:
                    row, col = randommove(self.sticks)

                self.move(row, col)
                self.player = 0
                
                
        elif self.game.mode == 1:
            self.game.view.player_move(row, col, maxspalte, self.player)
            if self.game_over():
                self.game.state = NimGame.OVER
                self.winner = self.player         # 勝者在此決定
                self.game.view.player_over()
                #遊戲結束按鈕隱藏
                self.game.hint.ht()
                self.game.level.ht()
            if self.player == 0:
                self.player = 1
            else:
                self.player = 0
            
                
    def game_over(self):
        # 檢查 是否 sticks == [0,0,....,0]
        
        allzeros= [0 for i in range(self.nRows)]
        
        trueOrFalse= (self.sticks==allzeros)
        
        return trueOrFalse  # (self.sticks == [0, 0, 0])

    def player_move(self, row, col):
        if self.sticks[row] <= col:
            return
        self.move(row, col)
    def notify_move(self, row, col):
        if self.sticks[row] <= col:
            return
        self.move(row, col)

class NimView:
    '''
    View(視圖)
    '''
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.model = game.model

        self.screen.colormode(255)
        self.screen.tracer(False)
        #背景顏色
        self.screen.bgcolor((240, 240, 255))

        self.writer = turtle.Turtle(visible=False)
        self.writer.pu()
        self.writer.speed(0)
        self.sticks = {}
        self.set_msg()
        
        #self.level = Level(game)
        self.level = game.level
        self.hint = game.hint
        '''
        #---------------------
        if self.game.hint.value == False:
            msg ='hint='
            self.writer.goto(0,-100)
            self.writer.write(msg)
        #---------------------
        '''
        
        self.nRows= game.nRows  ## 把排數(nRows)在此記住，很重要。
        
        for row in range(self.nRows):  #3):
            for col in range(MAXSTICKS):
                self.sticks[(row, col)] = Stick(row, col, game)
                
        self.display("... 等一下 ...")
        self.screen.tracer(True)

        #
        # ry: 以下開始創造 Menu
        #
        #self.menu= Menu(self.game.tk)
        #self.set_menu()
        
        self.menu= game.menu #CvMenu(game)

    def set_msg(self):
        msg = '''
                          Python 拈遊戲 (NimGame)
            
            以下是遊戲規則:
            
            1. 玩家與電腦輪流撿棒子，撿到最後一個的就贏了。
            
            2. 點擊任一棒子則玩家將會撿走該棒子右側的所有棒子。
            
            3. 點擊左下角的方塊會給予提示。
            
            4. 點擊右下角的烏龜可選擇難度(黃色代表難，橘色代表簡單)
            
            5. 遊戲開始前請選擇排數
        '''
        self.t = Turtle()
        self.t.pu()
        self.t.ht()
        self.t.goto(0,-50)
        self.t.write(msg, align="center", font=('Arial', 15, 'bold'))
    def display(self, msg1, msg2=None):
        
        self.screen.tracer(False)
        self.writer.clear()
        
        if msg2 is not None:
            self.writer.goto(0, - SCREENHEIGHT // 2 + 48)
            self.writer.pencolor("red")
            self.writer.write(msg2, align="center", font=("Courier",18,"bold"))
        self.writer.goto(0, - SCREENHEIGHT // 2 + 20)
        
        self.writer.pencolor("black")
        self.writer.write(msg1, align="center", font=("Courier",14,"bold"))
        self.screen.tracer(True)
        
        

    def setup(self):
        self.screen.tracer(False)

        #--------------------------------------------
        for row in range(self.nRows):  #3):
            for col in range(MAXSTICKS):
                #self.sticks[(row, col)] = Stick(row, col, self.game)
                self.sticks[(row, col)].showturtle()
        #--------------------------------------------       
        for row in range(self.nRows):
            for col in range(self.model.sticks[row]):
                self.sticks[(row, col)].color(SCOLOR)
        
        for row in range(self.nRows):
            for col in range(self.model.sticks[row], MAXSTICKS):
                self.sticks[(row, col)].color("white")
   
        #設定當遊戲開始則無法設定排數
        self.menu.entryconfig('棒子排數', state='disabled') 
        #設定當遊戲開始則無法選擇模式
        self.menu.entryconfig('遊戲模式', state='disabled') 
        
        #清除一開始寫的說明
        #self.game.hint.t.clear()
        self.t.clear()
        if self.game.mode == 0:
            self.display("輪到你了，請點擊棒子移除其右邊之所有棒子。")
        else:
            self.display("玩家1")
        self.screen.tracer(True)

    def notify_move(self, row, col, maxspalte, player):
        if player == 0:
            farbe = HCOLOR
            for s in range(col, maxspalte):
                self.sticks[(row, s)].color(farbe)
        else:
            self.display(" ... 想一想 ...         ")
            time.sleep(0.5)
            
            self.display(" ...  想一想 ... 啊！想出來了 ...")
            farbe = COLOR
            
            for s in range(maxspalte-1, col-1, -1):
                time.sleep(0.2)
                self.sticks[(row, s)].color(farbe)
            
            self.display("輪到你了，請點擊棒子移除其右邊之所有棒子。")
            
#---------------------------------------------------------
#---------------------------------------------------------
    def player_move(self, row, col, maxspalte, player):
        if player == 0:
            farbe = HCOLOR
            for s in range(col, maxspalte):
                self.sticks[(row, s)].color(farbe)
            self.display("")
            time.sleep(0.05)
            self.display("輪到玩家 2 了")
        else:
            farbe = COLOR
            for s in range(col, maxspalte):
                self.sticks[(row, s)].color(farbe)
            self.display("")
            time.sleep(0.05)
            self.display("輪到玩家 1 了")
#---------------------------------------------------------
#---------------------------------------------------------
    def notify_over(self):
        
        if self.game.model.winner == 0:
            msg2 = "你贏了！"
        else:
            msg2 = "你輸了。"
            
        #當遊戲結束則可以改排數
        self.menu.entryconfig('棒子排數', state='normal') 
        #當遊戲結束則可以選模式
        self.menu.entryconfig('遊戲模式', state='normal')

        self.display("按【空白鍵】再玩一次，按【Esc】鍵離開。", msg2)
    def player_over(self):
        if self.game.model.winner == 0:
            msg2 = "玩家1贏了！"
        else:
            msg2 = "玩家2贏了"
            
        #當遊戲結束則可以改排數
        self.menu.entryconfig('棒子排數', state='normal') 
        #當遊戲結束則可以選模式
        self.menu.entryconfig('遊戲模式', state='normal')
        
        self.display("按【空白鍵】再玩一次，按【Esc】鍵離開。", msg2)
    def clear(self):
        if self.game.state == NimGame.OVER:
            self.screen.clear()

class NimController:
    '''
    Controller(控制器)
    '''
    def __init__(self, game):
        self.game= game
        
        self.sticks = game.view.sticks
        self.BUSY = False
        
        self.level = game.level#.value
        self.level.onclick(self.level.changevalue)
        self.hint = game.hint
        #self.hint.onclick(self.hint.changevalue)
        
        
        for stick in self.sticks.values():
            #stick.onclick(stick.makemove)
            if self.game.mode == 0:
                stick.onclick(stick.makemove)
            elif self.game.mode == 1:
                stick.onclick(stick.playermove)
            '''
            #--------------------------
            self.hint.value = True
            self.hint.color('blue')
            self.game.view.writer.undo()
            #--------------------------
            '''
        #self.level = game.view.level
        self.level = game.level#.value
        self.level.onclick(self.level.changevalue)
        self.hint = game.hint
        self.hint.onclick(self.hint.changevalue)
        
        
        # 將用 "space" 來 開始遊戲
        self.game.screen.onkey(self.game.model.setup, "space")
        #self.game.screen.onkeyrelease(self.hint.showturtle, "space")
        #self.game.screen.onkey(self.game.hint.t.clear, "space")
        
        # 將用 "Esc" 來 清除 畫面
        self.game.screen.onkey(self.game.view.clear, "Escape")
        
        self.game.view.display("按空白鍵開始遊戲。")
        
        self.game.screen.listen()

    def notify_move(self, row, col):
        if self.BUSY:
            return
        self.BUSY = True
        self.game.model.notify_move(row, col)
        self.BUSY = False

class Stick(Turtle):
    
    def __init__(self, row, col, game):
        Turtle.__init__(self, visible=False)
        self.row= row
        self.col= col
        self.game= game
        self.nRows= self.game.nRows
        x, y= self.coords(row, col)
        
        self.shape("square")
        a = 25.0#+(self.nRows-3)*(20/7) #計算棒子在不同排樹的高度 25.0
        self.shapesize(HUNIT/a, WUNIT/25.0)
        self.speed(0)
        self.pu()
        self.goto(x,y)
        self.color('gray')
        #self.showturtle()
        #self.hideturtle()
        
    def coords(self, row, col):
        #
        # 這段也得調整，不然位置算錯。
        #
        # 為何數學公式為如此？？
        #
        packet, remainder = divmod(col, 5)
        x = (3 + 11 * packet + 2 * remainder) * WUNIT
        
        #y = (2 + 3 * row) * HUNIT
        y = (row) * HUNIT#*(3 - (self.nRows-3)*(3/7)) #計算棒子在不同排樹的位置
        
        x0=  x -SCREENWIDTH//2   + WUNIT//2 
        y0= -y +SCREENHEIGHT//2  - HUNIT//2
        return x0, y0 

    def makemove(self, x, y):
        if self.game.state != NimGame.RUNNING:
            return
        self.game.controller.notify_move(self.row, self.col)
        
    def playermove(self, x, y):
        if self.game.state != NimGame.RUNNING:
            return
        self.game.model.player_move(self.row, self.col)

class Level(Turtle): ###自己加的
    '''
    這個class用來決定在玩的過程中，控制電腦是否要以計算的方式(computerzug)，
    或以隨機的方式(randommove)，跟玩家玩。
    '''
    def __init__(self, game=None, x=0, y=0):
        
        
        Turtle.__init__(self, visible=False)
        
        
        self.value = True
        self.shape('turtle')
        self.shapesize(HUNIT/15, WUNIT/5)
        self.speed(0)
        self.left(90)
        self.pu()
        self.goto(x,y)
        self.color('yellow')
        #self.pencolor('black')
        #self.write('compute', align='center')
        self.onclick(self.changevalue)
        
        
    def changevalue(self, x, y):
        if(self.value==True):
            self.value = False
            self.color('orange')
        else:
            self.value = True
            self.color('yellow')

class Hint(Turtle):
    
    def __init__(self, game, x=0, y=0):
        
        Turtle.__init__(self, visible=False)
        
        self.game = game
        self.value = True
        self.shape('square')
        self.shapesize(HUNIT/15, WUNIT/5)
        self.speed(0)
        self.pu()
        self.goto(x,y)
        self.color('blue')
        
        self.onclick(self.changevalue)
        self.onrelease(self.changevalue02)
 
    def changevalue(self, x, y):
        
        if(self.value==True):
            self.value = False
            self.color('violet')
            self.game.view.writer.goto(0,-100)
            move = computerzug(self.game.model.sticks)
            
            #z= '提示:'+'第'+str(move[0]+1)+'排拿到剩下'+str(move[1])+'個'
            
            z= '提示：第 {} 排，拿到剩下 {} 個。'.format(move[0]+1, move[1])
            
            self.game.view.writer.write(z,
                                        align="center", 
                                        font=("Courier",14,"bold"))
    
    def changevalue02(self, x, y):
        
        if(self.value == False):
            self.value = True
            self.color('blue')
            self.game.view.writer.undo()

import pygame

class CvMenu(Menu):
    '''
    在這裡的有些地方使用了dictionary，
    但我發現這會造成遊戲開始後，目錄的順序會改變。
    例如：原本順序為--顏色1，顏色2，顏色3，顏色4
    而遊戲開始後順序變成--顏色4，顏色1，顏色2，顏色3
    之類的。
    '''
    def __init__(self, game):
        Menu.__init__(self, game.tk)
        aMenu= self #Menu(game.tk)
    #    self.set_menu(aMenu)
    #def set_menu(self, menu):
        #self.nRows = game.nRows
        #self.mode = game.mode
        #-------------------------------------------------
        bMenu = Menu(aMenu, tearoff=0)
        #bLabel = ['單人模式', '雙人模式']
        bLabel = {'單人模式': 0,
                  '雙人模式': 1}
        keyL = sorted(bLabel)
        for k in keyL:
            def cmd(x=k):
                nRows = game.nRows
                mode = bLabel[x]
                aNimGame= NimGame(nRows, mode)
            bMenu.add_command(label=k, command=cmd)


        #-------------------------------------------------
        cMenu = Menu(aMenu, tearoff=0)
        cLabel = ['3', '4', '5', '6', '7', '8', '9', '10']
        for i in cLabel:
            def cmd(x=i):
                nRows = int(x)
                mode = game.mode
                #print('nRows= ', nRows)
                aNimGame= NimGame(nRows, mode)  
                            
            cMenu.add_command(label=i, command=cmd)

        
        #-------------------------------------------------
        
        dMenu = Menu(aMenu, tearoff=0)
        
        #
        # 下面這 6 行 OK，但可以改成使用 dictionary ，會比較精簡。
        #
        '''
        colist = ['顏色 1', '顏色 2', '顏色 3', '顏色 4']
        bgcol = ['#F0F0FF', '#DDDDDD', '#FFFFBB', '#EEFFBB']
        
        for i in range(4):
            def cmd(x=i):
                game.screen.bgcolor(bgcol[x])

            dMenu.add_command(label=colist[i], command=cmd)
        '''
        #
        # 把上面改成 使用 dictionary 如下，比較好看。
        #
        dLabel= {'顏色 1': '#F0F0FF', 
                 '顏色 2': '#DDDDDD', 
                 '顏色 3': '#FFFFBB', 
                 '顏色 4': '#EEFFBB'}
        keyL = sorted(dLabel)
        '''
        for k in dLabel:
            def cmd(x=k):
                game.screen.bgcolor(dLabel[x])
        '''
        for k in keyL:
            def cmd(x=k):
                game.screen.bgcolor(dLabel[x])
            dMenu.add_command(label= k, command= cmd)
        

        #-------------------------------------------------
        #
        # 練習把下段改成像上面的樣子。
        #
        eMenu = Menu(aMenu, tearoff=0)
        
        '''
        picist = ['無圖案','圖案 1', '圖案 2', '圖案 3']
        bgpic = ['nopic',
                 'pictures/background.png', 
                 'pictures/dog01.png', 
                 'pictures/calvin.png']
        '''
                 
        eLabel = {'無圖案': 'nopic',
                  '圖案 1': 'pictures/background.png',
                  '圖案 2': 'pictures/dog01.png',
                  '圖案 3': 'pictures/calvin.png'}
        keyL = sorted(eLabel)
        for k in keyL:
            def cmd(x=k):
                game.screen.bgpic(eLabel[x])
            eMenu.add_command(label = k, command=cmd)

        #-------------------------------------------------
        #  加音樂囉
        #
        fMenu = Menu(aMenu, tearoff=0)
        fLabel= {'音樂停止': '__0__.mid',
                 '音樂01': 'musics/background.mid',
                 '音樂02': 'musics/canon.mid',
                 '音樂03': 'musics/Sundial Dreams.mp3'}
        keyL = sorted(fLabel)
        for k in keyL:
            def cmd(x=k):
                musicFile= fLabel[x]
                if musicFile != '__0__.mid':
                    #musicIsPlaying= True
                    pygame.mixer.music.load(musicFile)
                    pygame.mixer.music.play(-1, 0.0)
                else:
                    #musicIsPlaying= False
                    pygame.mixer.music.stop()
                

            fMenu.add_command(label= k, command= cmd)
        #-------------------------------------------------  
        '''
        gMenu = Menu(aMenu, tearoff=0)
        def cmd():
            aNimGame= NimGame(nRows, mode)
        gMenu.add_command(label = '重新開始', command = cmd)
        '''
        #-------------------------------------------------        
        aMenu.add_cascade(label= '遊戲模式', menu= bMenu)
        aMenu.add_cascade(label= '棒子排數', menu= cMenu)
        aMenu.add_cascade(label= '背景顏色', menu= dMenu)        
        aMenu.add_cascade(label= '背景圖案', menu= eMenu)
        aMenu.add_cascade(label= '背景音樂', menu= fMenu)
        #--------------------------------------------------
        def cmd():
            aNimGame= NimGame(game.nRows, game.mode)
        aMenu.add_command(label= '重新開始', command= cmd)
               
        game.tk.config(menu= aMenu)

#
#
# 排數 (nRows = [1,2,3,4,5,....]) 可控制
# 電腦的 智商 = [True, False] 也可控制
#
# 也可嘗試按某個鍵就可輸出【提示】，必勝法則！
# 如何設計使用者介面讓使用者來方便設定。
#
# 也可加入聲音，及影像，贏的時候如何喝采，輸的時候如何安慰。
#
#
#
#
if __name__=='__main__':
    
    
    aNimGame= NimGame()

    pygame.init()    
    
    aNimGame.tk.mainloop()
    
    pygame.quit()
    



