#Import libraries
import pygame
from sudoku_generator import *

#Draws the start screen and returns how many tiles should be removed
def DrawStart(screen):
    #Background color
    screen.fill("white")

    #Sets the fonts
    TitleFont = pygame.font.Font(None, 80)
    ButtonFont = pygame.font.Font(None, 50)

    # Draw start menu GUI
    # Title
    TitleSurface = TitleFont.render("Welcome to Sudoku", 0, "black")
    TitleRect = TitleSurface.get_rect(center=(320, 150))
    screen.blit(TitleSurface, TitleRect)
    #Buttons
    EasyText = ButtonFont.render("EASY", 0, "white")
    MediumText = ButtonFont.render("MEDIUM", 0, "white")
    HardText = ButtonFont.render("HARD", 0, "white")
        #Easy
    EasySurface = pygame.Surface((EasyText.get_size()[0] + 20, EasyText.get_size()[1] + 20))
    EasySurface.fill("orange")
    EasySurface.blit(EasyText, (10, 10))
        #Medium
    MediumSurface = pygame.Surface((MediumText.get_size()[0] + 20, MediumText.get_size()[1] + 20))
    MediumSurface.fill("orange")
    MediumSurface.blit(MediumText, (10, 10))
        #Hard
    HardSurface = pygame.Surface((HardText.get_size()[0] + 20, HardText.get_size()[1] + 20))
    HardSurface.fill("orange")
    HardSurface.blit(HardText, (10, 10))
        #Button rectangles
    EasyRect = EasySurface.get_rect(center=(140, 450))
    MediumRect = MediumSurface.get_rect(center=(320, 450))
    HardRect = HardSurface.get_rect(center=(500, 450))
        #Button draws
    screen.blit(EasySurface, EasyRect)
    screen.blit(MediumSurface, MediumRect)
    screen.blit(HardSurface, HardRect)
    #Start menu event loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN: #Player clicks
                if EasyRect.collidepoint(event.pos): #Is mouse on easy button?
                    return 30
                elif MediumRect.collidepoint(event.pos): #Is mouse on medium button?
                    return 40
                elif HardRect.collidepoint(event.pos): #Is mouse on hard button?
                    return 50
        pygame.display.update()


def main():
    #Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((630, 700))
    pygame.display.set_caption("Sudoku")

    #Run the start screen and get the difficulty
    RemovedCells = DrawStart(screen)

    #Initialize game board
    SudokuBoard, BoardSolution = generate_sudoku(9, RemovedCells)
    GameBoard = Board(630, 700, screen, RemovedCells, SudokuBoard)
    Win = False

    #Draw game screen
    #Buttons
    ButtonFont = pygame.font.Font(None, 40)
        #Reset
    ResetText = ButtonFont.render("RESET", 0, "white")
    ResetSurface = pygame.Surface((ResetText.get_size()[0] + 15, ResetText.get_size()[1] + 15))
    ResetSurface.fill("orange")
    ResetSurface.blit(ResetText, (10, 10))
    ResetRect = ResetSurface.get_rect(center=(140, 665))
        #Restart
    RestartText = ButtonFont.render("RESTART", 0, "white")
    RestartSurface = pygame.Surface((RestartText.get_size()[0] + 15, RestartText.get_size()[1] + 15))
    RestartSurface.fill("orange")
    RestartSurface.blit(RestartText, (10, 10))
    RestartRect = RestartSurface.get_rect(center=(320, 665))
        #Exit
    ExitText = ButtonFont.render("EXIT", 0, "white")
    ExitSurface = pygame.Surface((ExitText.get_size()[0] + 15, ExitText.get_size()[1] + 15))
    ExitSurface.fill("orange")
    ExitSurface.blit(ExitText, (10, 10))
    ExitRect = ExitSurface.get_rect(center=(500, 665))
        #Button draws
    screen.blit(ResetSurface, ResetRect)
    screen.blit(RestartSurface, RestartRect)
    screen.blit(ExitSurface, ExitRect)
    #Board
    GameBoard.draw()
    pygame.display.update()

    #Game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN: #Player clicks
                #Gets the row and column that was clicked
                ClickedRow = event.pos[1] // 70 + 1
                ClickedCol = event.pos[0] // 70 + 1
                if ClickedRow < 10: #If the clicked area is inside the game board, select a tile
                    GameBoard.select(ClickedRow, ClickedCol)
                    GameBoard.draw()
                if ResetRect.collidepoint(event.pos): #Is mouse on reset button?
                    GameBoard.reset_to_original(SudokuBoard)
                    GameBoard.draw()
                if RestartRect.collidepoint(event.pos): #Is mouse on restart button?
                    main()
                if ExitRect.collidepoint(event.pos): #Is mouse on exit button?
                    pygame.quit()

            #If a key is pressed
            if event.type == pygame.KEYDOWN:
                #Sketching (player enters a number)
                if event.unicode.isdigit():
                    GameBoard.sketch(int(event.unicode))
                    GameBoard.draw()
                #Entering a value (player presses enter/return)
                if event.key == pygame.K_RETURN:
                    GameBoard.place_number()
                    GameBoard.draw()
                #Removing a value (player presses backspace)
                if event.key == pygame.K_BACKSPACE:
                    GameBoard.clear()
                    GameBoard.draw()
                #Moving selection (player presses arrow keys)
                #Up
                if event.key == pygame.K_UP:
                    if GameBoard.selectedCell is None:
                        GameBoard.select(1, 1)
                    else:
                        GameBoard.select(GameBoard.selectedCell.row, GameBoard.selectedCell.col + 1)
                    GameBoard.draw()
                #Left
                if event.key == pygame.K_LEFT:
                    if GameBoard.selectedCell is None:
                        GameBoard.select(1, 1)
                    else:
                        GameBoard.select(GameBoard.selectedCell.row + 1, GameBoard.selectedCell.col)
                    GameBoard.draw()
                #Down
                if event.key == pygame.K_DOWN:
                    if GameBoard.selectedCell is None:
                        GameBoard.select(1, 1)
                    else:
                        try:
                            GameBoard.select(GameBoard.selectedCell.row + 2, GameBoard.selectedCell.col + 1)
                        except:
                            pass
                    GameBoard.draw()
                #Right
                if event.key == pygame.K_RIGHT:
                    if GameBoard.selectedCell is None:
                        GameBoard.select(1, 1)
                    else:
                        try:
                            GameBoard.select(GameBoard.selectedCell.row + 1, GameBoard.selectedCell.col + 2)
                        except:
                            pass
                    GameBoard.draw()

        pygame.display.update()
        #Check if the board is full, if it is then check if the inputs are correct
        if GameBoard.is_full():
            Win = GameBoard.check_board(BoardSolution)
            break

    #End of the game
    #Background color
    screen.fill("white")
    #Fonts
    OutcomeFont = pygame.font.Font(None, 80)
    ButtonFont = pygame.font.Font(None, 50)
    #Outcomes
    if Win:
        OutcomeSurface = OutcomeFont.render("Game Won!", 0, "black")
        ButtonText = ButtonFont.render("EXIT", 0, "white")
    else:
        OutcomeSurface = OutcomeFont.render("Game Over :(", 0, "black")
        ButtonText = ButtonFont.render("RESTART", 0, "white")
    #Title
    OutcomeRect = OutcomeSurface.get_rect(center=(320, 150))
    screen.blit(OutcomeSurface, OutcomeRect)
    #Button
    ButtonSurface = pygame.Surface((ButtonText.get_size()[0] + 20, ButtonText.get_size()[1] + 20))
    ButtonSurface.fill("orange")
    ButtonSurface.blit(ButtonText, (10, 10))
    ButtonRect = ButtonSurface.get_rect(center=(315, 330))
    screen.blit(ButtonSurface, ButtonRect)
    #End menu event loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN: #Player clicks
                if ButtonRect.collidepoint(event.pos):  # Is mouse on the button?
                    #If the game was won, exit, else restart the program
                    if Win:
                        pygame.quit()
                    else:
                        main()
        pygame.display.update()



if __name__ == "__main__":
    main()