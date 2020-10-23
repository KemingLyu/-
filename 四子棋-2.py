
# coding: utf-8

# # 四子棋
# ### 玩家為1, 電腦為2, 悔棋輸入b

# In[1]:


import numpy as np
import math
import random as rd


# In[2]:


value2 = [0, -math.inf, math.inf] #平手, 玩家, 電腦
value1 = [0, math.inf, -math.inf]


# In[3]:


def draw(board):
    pieces = ['.', 'O', 'X']
    print()
    for i in range(WIDTH):
        print(i, end=' ')
    print()
    for i in range(HEIGHT):
        for j in range(WIDTH):
            k = int(board[i][j])
            try:
                print(pieces[k],end=' ')
            except:
                print(pieces[k],end=' ')
        print()


# In[4]:


def winner(board):
   #橫的
   for i in range(HEIGHT):
       for j in range(WIDTH-3):
           if board[i][j]==board[i][j+1]==board[i][j+2]==board[i][j+3]!=0:
               return board[i][j]
   #直的
   for j in range(WIDTH):
       for i in range(HEIGHT-3):
           if board[i][j]==board[i+1][j]==board[i+2][j]==board[i+3][j]!=0:
               return board[i][j]

   #斜的(左上右下)
   for i in range(HEIGHT-3):
       for j in range(WIDTH-3):
           if board[i][j]==board[i+1][j+1]==board[i+2][j+2]==board[i+3][j+3]!=0:
               return board[i][j]

   #斜的(右上左下)
   for i in range(3,HEIGHT):
       for j in range(3, WIDTH):
           if board[i][j-3]==board[i-1][j-2]==board[i-2][j-1]==board[i-3][j]!=0:
               return board[i][j-3]
   #還沒結束
   for i in range(HEIGHT):
       for j in range(WIDTH):
           if board[i][j]==0:
               return 3  # 3代表遊戲還沒結束
   #平手
   return 0


# In[5]:


def evaluate_window(window, piece):
    score = 0
    opp_piece = -piece
    '''
    if window.count(piece) == 4:
        score += 100'''
    if window.count(piece) == 3 and window.count(0) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(0) == 1:
        score -= 4

    return score


# In[6]:


def score_position(board, piece):
    score = 0

    ## Score center column
    ######這裡代表中間的這行有幾個piece###########
    center_array = [int(i) for i in list(board[:, WIDTH//2])] ### board[0][3]~board[5][3]###
    center_count = center_array.count(piece) #####中間這排有幾個piece
    score += center_count * 3  # score為中間的piece數目乘以三。

    ## Score Horizontal
    for r in range(HEIGHT):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(WIDTH-3):
            window = row_array[c:c+4]
            score += evaluate_window(window, piece)

    ## Score Vertical
    for c in range(WIDTH):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(HEIGHT-3):
            window = col_array[r:r+4]
            score += evaluate_window(window, piece)

    ## Score posiive sloped diagonal
    for r in range(HEIGHT-3):
        for c in range(WIDTH-3):
            window = [board[r+i][c+i] for i in range(4)]
            score += evaluate_window(window, piece)

    for r in range(HEIGHT-3):
        for c in range(WIDTH-3):
            window = [board[r+3-i][c+i] for i in range(4)]
            score += evaluate_window(window, piece)

    return score


# In[7]:


def minimax(board, piece, value, depth, is_AI_turn):
    global countX
    countX += 1
    win = int(winner(board))
    opp_piece = -piece #piece, opp_piece為 1,-1

    if win!=3 or depth==0:
        if win!=3:
            return value[win]
        else:
            return score_position(board, piece)

    if is_AI_turn:
        bestscore = -math.inf
        for j in range(WIDTH):
            i = D[j]
            if i==-1:
                continue
            elif board[i][j] == 0:
                board[i][j] = piece
                D[j] -= 1
                score = minimax(board, piece, value, depth-1, False)
                #countX += 1
                board[i][j] = 0
                D[j] += 1
                bestscore = max(bestscore, score)
        return bestscore
    else:
        bestscore = math.inf
        for j in range(WIDTH):
            i = D[j]
            if i == -1:
                continue
            elif board[i][j] == 0:
                board[i][j] = opp_piece
                D[j] -= 1
                score = minimax(board, piece, value, depth-1, True)
                #countX += 1
                board[i][j] = 0
                D[j] += 1
                bestscore = min(bestscore, score)
        return bestscore


# In[8]:


def ai_move(board, piece, value, depth):
    bestscore = -math.inf
    y = -1
    #if c<=2:
    #    return rd.randint(0,WIDTH-1)
    for j in range(WIDTH):
        i = D[j]
        if i==-1:
            continue
        elif board[i][j]==0:
            board[i][j] = piece
            D[j]-=1
            score = minimax(board, piece, value, depth, False)
            board[i][j] = 0
            D[j]+=1
            if score > bestscore:
                bestscore = score
                y = j
            #D[j]-=1
    print(bestscore)
    return y


# In[9]:


def minimax_alphabeta(board, piece, value, depth, is_AI_turn, alpha=-math.inf, beta=math.inf):
    global countX
    countX += 1
    win = int(winner(board))
    opp_piece = -piece #piece, opp_piece為 1,-1

    if win!=3 or depth==0:
        if win!=3:
            return value[win]
        else:
            return score_position(board, piece)

    if is_AI_turn:
        bestscore = -math.inf
        for j in range(WIDTH):
            i = D[j]
            if i==-1:
                continue
            elif board[i][j] == 0:
                board[i][j] = piece
                D[j] -= 1
                score = minimax_alphabeta(board, piece, value, depth-1, False)
                #countX += 1
                board[i][j] = 0
                D[j] += 1
                bestscore = max(bestscore, score)
                alpha = max(alpha, bestscore)
                if beta <= alpha:
                    break
        return bestscore
    else:
        bestscore = math.inf
        for j in range(WIDTH):
            i = D[j]
            if i == -1:
                continue
            elif board[i][j] == 0:
                board[i][j] = opp_piece
                D[j] -= 1
                score = minimax_alphabeta(board, piece, value, depth-1, True)
                #countX += 1
                board[i][j] = 0
                D[j] += 1
                bestscore = min(bestscore, score)
                beta = min(beta, bestscore)
                if alpha >= beta:
                    break
        return bestscore


# In[10]:


def ai_move_alphabeta(board, piece, value, depth):
    bestscore = -math.inf
    y = -1
    #if c<=2:
    #    return rd.randint(0,WIDTH-1)
    for j in range(WIDTH):
        i = D[j]
        if i==-1:
            continue
        elif board[i][j]==0:
            board[i][j] = piece
            D[j]-=1
            score = minimax_alphabeta(board, piece, value, depth, False)
            board[i][j] = 0
            D[j]+=1
            if score > bestscore:
                bestscore = score
                y = j
            #D[j]-=1
    print(bestscore)
    return y


# In[11]:


def regret(board, move):
    ##悔棋##
    board[move[-1][0]][move[-1][1]] = 0
    board[move[-2][0]][move[-2][1]] = 0
    #下過的排的深度要加回來
    D[move[-1][1]]+=1
    D[move[-2][1]]+=1
    move.pop()
    move.pop()


# In[12]:


def game(board):

    global countX
    print('四子棋 connect-4')
    print('輸入r悔棋')
    draw(board)
    while winner(board)== 3:  #遊戲還沒結束
        #-------玩家---------#
        while True:
            k = input('第幾排：')
            try:
                ##悔棋##
                if k == 'r':
                    regret(board, move)
                    draw(board)
                else:
                    y = int(k)
                    if D[y]!=-1:
                        x = D[y]
                        move.append([x,y])
                        board[x][y] = PIECE1
                        D[y]-=1
                        break
                    else:
                        print('這排滿了')
            except:
                print('重新輸入')
        #-------電腦---------#
        '''
        ai1 = ai_move_alphabeta(board, PIECE1, value1, 4)
        x = D[ai1]
        board[x][ai1] = PIECE1
        D[ai1]-=1
        draw(board, x, ai1)
        print('countO = ', countO)
        #print_b(board)
        #print(D)
        '''
        if winner(board)==PIECE1:
            print('你贏了')
            #print_b(board)
            break
        if winner(board)==PIECE2:
            print('電腦贏了')
            break
        if winner(board)==0:
            print('平手')
            break
        #-------玩家---------#

        #-------電腦---------#
        print('計算中...')
        ai2 = ai_move_alphabeta(board, PIECE2, value2, DEPTH)
        #ai2 = ai_move(board, PIECE2, value2, DEPTH)
        x = D[ai2]
        board[x][ai2] = PIECE2
        D[ai2]-=1
        move.append([x,ai2])
        draw(board)
        print('countX = ', countX)
        countX = 0
        global c
        c += 1
        #print(D)
        #print(HEIGHT, WIDTH)
        if winner(board)==PIECE1:
            print('你贏了')
            #print_b(board)
            break
        if winner(board)==PIECE2:
            ouput = rd.choice(['菜雞', '嫩', '有夠廢哈哈', '484要刪game了','再來啊', '好爛喔', '阿不4很厲害'])
            print('你輸了 '+ouput)
            break
        if winner(board)==0:
            print('平手')
            break


# In[13]:


HEIGHT = 6
WIDTH = 7
board = np.zeros((HEIGHT,WIDTH))
PIECE1 = 1
PIECE2 = -1
countX = 0
countO = 0
DEPTH = 4
c = 0
h = HEIGHT-1
D = [h,h,h,h,h,h,h]
move = []
game(board)

