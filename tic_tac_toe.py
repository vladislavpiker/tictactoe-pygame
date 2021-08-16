import pygame as pg
from colors import *

pg.init()

width = 620
height = 680
restart_img = pg.image.load('restart.png')
icon = pg.image.load("cells.jpg")
srfc = pg.display.set_mode((width, height))
pg.display.set_caption('Tic Tac Toe')
pg.display.set_icon(icon)
FPS = 30
clock = pg.time.Clock()


# Coordinates, lengths and heights of rects dividing cells:
sep_lines = ((200, 0, 10, 620), (410, 0, 10, 620), (0, 200, 620, 10), (0, 410, 620, 10), (0, 620, 620, 10))
# cell centers:
figCenterPoses = ( (100, 100), (310, 100), (520, 100),
                 (100, 310), (310, 310), (520, 310),
                 (100, 520), (310, 520), (520, 520) )
# combinations of cells required to win:
win_cond = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))
# coordinates of the lines that cross out the cells (after the victory):
strikethrough_lines = ( (20, 100, 600, 100), (20, 310, 600, 310), (20, 520, 600, 520),
        (100, 20, 100, 600), (310, 20, 310, 600), (520, 20, 520, 600),
        (20, 20, 600, 600), (600, 20, 20, 600) )
# combination of the winning condition and the strikethrough line:
win_cond_lines = tuple(zip(win_cond, strikethrough_lines))

cell_frames = ( (0, 0, 200, 200), (210, 0, 410, 200), (420, 0, 620, 200), 
                (0, 210, 200, 410), (210, 210, 410, 410), (420, 210, 620, 410),
                (0, 420, 200, 620), (210, 420, 410, 620), (420, 420, 620, 620) )
win_msg_inf = pg.font.Font(None, 40)


def drawCursor(cursor, pos):
    """ draw cursor(cross or circle) on the current position """
    if cursor == 0:
        x, y = pos
        pg.draw.line(srfc, RED, (x-20, y-20), (x+20, y+20), 5)
        pg.draw.line(srfc, RED, (x+20, y-20), (x-20, y+20), 5)
    elif cursor == 1:
        pg.draw.circle(srfc, BLUE, pos, 20, 2)


def drawCross(x, y):
    """ draw cross on cell """
    pg.draw.line(srfc, RED, (x-80, y-80), (x+80, y+80), 15)
    pg.draw.line(srfc, RED, (x+80, y-80), (x-80, y+80), 15)


def drawCircle(x, y):
    """  draw circle on cell """
    pg.draw.circle(srfc, BLUE, (x, y), 80, 15)


def checkWinner(game_tuple):
    """ returns the winner number (0 or 1) and the corresponding strikethrough line if there is a winner
    or return None, None if there isn`t a winner """
    wl1 = [cell[0] for cell in game_tuple]
    wl2 = [cell[1] for cell in game_tuple]
    for player, wl in ( (0, wl1), (1, wl2) ):
        for cond, strike_line in win_cond_lines:
            winlist = [wl[cell] for cell in cond]
            if all(winlist):
                return player, strike_line
    return None, None


def tictactoe():
    """ the main game function """
    cell_status = tuple(map(list, zip([0] * 9, [0] * 9, cell_frames, figCenterPoses)))

    _is_end = False
    # pg.mouse.set_visible(False)
    drawFigureList = []
    move_counter = 0
    while 1:
        srfc.fill(WHITE)
        for coord_line in sep_lines:
            pg.draw.rect(srfc, BLACK, coord_line) # draw cells
        for fig in drawFigureList:
            fig[0](*fig[1]) # draw figures(crosses and circles
        srfc.blit(restart_img.convert_alpha(), (570, 631))
        pg.display.update()

        if not _is_end:
            if move_counter % 2 == 0:
                player = 0
                drawFigure = drawCross
            elif move_counter % 2 == 1:
                player = 1
                drawFigure = drawCircle

            mouse_pos = pg.mouse.get_pos()
            if 0 < mouse_pos[0] < 620 and 0 < mouse_pos[1] < 620: # if mouse on the cells
                pg.mouse.set_visible(False)
                drawCursor(player, mouse_pos) # draw a cross or circle instead of the cursor
                pg.display.update()
            else:
                pg.mouse.set_visible(True)

            if move_counter >= 5: # victory is possible after 5 moves
                win = checkWinner(cell_status)
                winner, across_line = win
                if winner == 0:
                    _is_end = True
                    win_msg = 'Crosses won'
                elif winner == 1:
                    _is_end = True
                    win_msg = 'Circles won'
                elif winner is None and move_counter == 9: # if there is no winner on move 9, it is a draw
                    _is_end = True
                    win_msg = 'Draw'
        else:
            pg.mouse.set_visible(True) # draw cursor after game over
            win_banner = win_msg_inf.render(win_msg, True, BLACK)
            srfc.blit(win_banner, (10, 640))
            if across_line != None: # if not a draw
                ac_line_start, ac_line_end = across_line[0:2], across_line[2:]
                pg.draw.line(srfc, GREEN, ac_line_start, ac_line_end, 10) # draw strikethrough line
            pg.display.update()

        for event in pg.event.get():
            if event.type == pg.QUIT or \
                    (event.type == pg.KEYDOWN and event.key == pg.K_q and event.mod == pg.KMOD_LCTRL):
                exit(0)
            if event.type == pg.MOUSEBUTTONUP and event.button == 1: # if the left mouse button was pressed
                click_pos = event.pos
                if not _is_end:
                    for status in cell_status:
                        if not(status[0] or status[1]): # if current cell is not filled
                            if status[2][0] < click_pos[0] < status[2][2] and status[2][1] < click_pos[1] < status[2][3]:
                                status[player] = 1 # note that the cell is filled
                                move_counter += 1
                                drawFigureList.append((drawFigure, status[3]))
                if 570 < click_pos[0] < 618 and 631 < click_pos[1] < 679: # if the restart button was pressed
                    return

        clock.tick(FPS)

while 1:
    tictactoe()
