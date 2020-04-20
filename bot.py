import random


# This is an example bot written by the developers!
# Use this to help write your own code, or run it against your bot to see how well you can do!

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
        else:
            forward = -1


        # try capturing pieces
        if check_space_wrapper(row + forward, col + 1, board_size) == opp_team: # up and right
            capture(row + forward, col + 1)
            dlog('Captured at: (' + str(row + forward) + ', ' + str(col + 1) + ')')

        elif check_space_wrapper(row + forward, col - 1, board_size) == opp_team: # up and left
            capture(row + forward, col - 1)
            dlog('Captured at: (' + str(row + forward) + ', ' + str(col - 1) + ')')

        #avoid capture 
        #if it senses an enemy pawn in the top right or left, don't move. 
        if (check_space(row - 2, col + 1) == opp_team or check_space(row - 2, col - 1) == opp_team):
            #do nothing
            return
            dlog('Waited patiently')
        # otherwise try to move forward
        elif row + forward != -1 and row + forward != board_size and not check_space_wrapper(row + forward, col, board_size):
            #               ^  not off the board    ^            and    ^ directly forward is empty
            move_forward()
            dlog('Moved forward!')


        

        confusion = "you need a line here to avoid segfault. we aren't sure why but are working on it"
        # ^ I think this is related to the potential ambiguity of what the following else is referring to?

    else:
        
        # added this boolean so we don't waste bytecode on spawn loops if something's already been spawned
        hasSpawned = False

        if team == Team.WHITE:
            index = 0
        else:
            index = board_size - 1

        # checks the third row from the bottom to see if there are enemy pawns and spawns defensive pawn on adjacent column
        for col in range(0, 16):
            if check_space(13, col) == opp_team:
                if not check_space(index, col + 1):
                    spawn(index, col + 1)
                    hasSpawned = True
                    dlog('Spawned defensive pawn at ' + str(index) + ', ' + str(col))
                    break
                elif not check_space(index, col - 1):
                    spawn(index, col - 1)
                    hasSpawned = True
                    dlog('Spawned defensive pawn at ' + str(index) + ', ' + str(col))
                    break

        if not hasSpawned:
            for _ in range(board_size):
                if not check_space(index, 7):
                    if not check_space(index, 8):
                        spawn(index, 8)
                        dlog('Spawned unit at: (' + str(index) + ', ' + str(8) + ')')
                    spawn(index, 7)
                    dlog('Spawned unit at: (' + str(index) + ', ' + str(7) + ')')
                else:
                    i = random.randint(0, board_size - 1)
                    if not check_space(index, i):
                        spawn(index, i)
                        dlog('Spawned unit at: (' + str(index) + ', ' + str(i) + ')')
                        break


    # defensive moves
    # if there is someone in the third to bottom row, spawn a defensive pawn on either the left or the right
    bytecode = get_bytecode()
    dlog('Done! Bytecode left: ' + str(bytecode))
    dlog('Round ' + turn + ' end')