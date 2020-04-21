import random


# This is an example bot written by the developers!
# Use this to help write your own code, or run it against your bot to see how well you can do!

# cd Python/battlehack20-scaffold-master
# python run.py examplefuncsplayer C:/Users/exzac/Python/bh2020/ezbh2020 --raw-text

DEBUG = 1
def dlog(str):
    if DEBUG > 0:
        log(str)



    



def check_space_wrapper(r, c, board_size):
    # check space, except doesn't hit you with game errors
    if r < 0 or c < 0 or c >= board_size or r >= board_size:
        return False
    try:
        return check_space(r, c)
    except:
        return None

def on_board(targetRow, targetCol):
    if not targetRow < 0 and not targetRow > 15 and not targetCol < 0 and not targetCol > 15:
        return True
    else:
        return False




def turn():
    """
    MUST be defined for robot to run
    This function will be called at the beginning of every turn and should contain the bulk of your robot commands
    """

    dlog('Starting Turn!')
    board_size = get_board_size()

    team = get_team()
    opp_team = Team.WHITE if team == Team.BLACK else team.BLACK
    same_team = Team.WHITE if team == Team.WHITE else team.BLACK
    dlog('Team: ' + str(team))

    robottype = get_type()
    dlog('Type: ' + str(robottype))


    if robottype == RobotType.PAWN:
        row, col = get_location()
        dlog('My location is: ' + str(row) + ' ' + str(col))

        if team == Team.WHITE:
            forward = 1
            backward = -1
        else:
            forward = -1
            backward = 1

        tryCapture = True
        avoidCapture = True


        # One-stop status checker
        if (on_board(row + backward, col + 1)):
            if (check_space(row + backward, col + 1) == same_team):
                innerBackRight = True
        if (on_board(row + backward, col - 1)):
            if (check_space(row + backward, col - 1) == same_team):
                innerBackLeft = True
        if (on_board(row + 2*backward, col + 1)):
            if (check_space(row + (2*backward), col + 1) == same_team):
                outerBackRight = True
        if (on_board(row + 2*backward, col - 1)):
            if (check_space(row + (2*backward), col - 1) == same_team):
                outerBackLeft = True
        if (on_board(row + 2*backward, col)):
            if (check_space(row + (2*backward), col) == same_team):
                outerBackCenter = True



        # try capturing pieces
        
        if(tryCapture):
            if check_space_wrapper(row + forward, col + 1, board_size) == opp_team: # up and right
                capture(row + forward, col + 1)
                dlog('Captured at: (' + str(row + forward) + ', ' + str(col + 1) + ')')
                return

            elif check_space_wrapper(row + forward, col - 1, board_size) == opp_team: # up and left
                capture(row + forward, col - 1)
                dlog('Captured at: (' + str(row + forward) + ', ' + str(col - 1) + ')')
                return

        #avoid capture 
        #if it senses an enemy pawn in the top right or left, don't move.
        if(avoidCapture):

            if (on_board(row + (2*forward), col + 1)):
                if (check_space(row + (2*forward), col + 1) == opp_team):
                    if (check_space(row + forward, col + 1) == same_team):
                        move_forward()
                        dlog('Would\'ve waited, but had to sacrifice to avoid stalemate')
                        return
                    else:
                        dlog('Waited patiently')
                        return
                elif (row + forward != -1 and row + forward != board_size and not check_space_wrapper(row + forward, col, board_size)):
                    move_forward()
            elif (on_board(row + (2*forward), col - 1)):
                if (check_space(row + (2*forward), col - 1) == opp_team):
                    if (check_space(row + forward, col - 1) == same_team):
                        move_forward()
                        dlog('Would\'ve waited, but had to sacrifice to avoid stalemate')
                        return
                    else:
                        dlog('Waited patiently')
                        return
                elif (row + forward != -1 and row + forward != board_size and not check_space_wrapper(row + forward, col, board_size)):
                    move_forward()
            # otherwise try to move forward
            elif (row + forward != -1 and row + forward != board_size and not check_space_wrapper(row + forward, col, board_size)):
                move_forward()

        elif (row + forward != -1 and row + forward != board_size and not check_space_wrapper(row + forward, col, board_size)):
                move_forward()



        

        confusion = "you need a line here to avoid segfault. we aren't sure why but are working on it"
        # ^ I think this is related to the potential ambiguity of what the following else is referring to?

    else:
        
        # added this boolean so we don't waste bytecode on spawn loops if something's already been spawned
        hasSpawned = False

        # critRow refers to the critical row that the overlord checks to see if there are any enemies in order to spawn defensive pawns
        if team == Team.WHITE:
            index = 0
            critRow = 2
        else:
            index = board_size - 1
            critRow = board_size - 3

        spawnDefense = True
        spawnRandom = True

        # TODO: SPAWN UNDER ENEMY PAWN IN SECOND TO LAST ROW AS LAST RESORT, MAYBE AVOID SPAWN ON EITHER SIDE?
        #       PREEMPTIVELY ATTACK ROWS OF TWO
        # checks the third row from the bottom to see if there are enemy pawns and spawns defensive pawn on adjacent column
        if(spawnDefense):
            for col in range(0, 16):
                if check_space(critRow, col) == opp_team:
                    if(on_board(critRow, col + 1)):
                        if not check_space(index, col + 1):
                            spawn(index, col + 1)
                            hasSpawned = True
                            dlog('Spawned defensive pawn at ' + str(index) + ', ' + str(col))
                            break
                    elif(on_board(critRow, col - 1)):
                        if not check_space(index, col - 1):
                            spawn(index, col - 1)
                            hasSpawned = True
                            dlog('Spawned defensive pawn at ' + str(index) + ', ' + str(col))
                            break

        if(spawnRandom):
            if not hasSpawned:
                for _ in range(board_size):
    #                if not check_space(index, 7):
    #                    if not check_space(index, 8):
    #                        spawn(index, 8)
    #                        dlog('Spawned unit at: (' + str(index) + ', ' + str(8) + ')')
    #                    spawn(index, 7)
    #                    dlog('Spawned unit at: (' + str(index) + ', ' + str(7) + ')')
    #                else:
                    i = random.randint(0, board_size - 1)
                    if not check_space(index, i):
                        spawn(index, i)
                        dlog('Spawned unit at: (' + str(index) + ', ' + str(i) + ')')
                        break

    bytecode = get_bytecode()
    dlog('Done! Bytecode left: ' + str(bytecode))