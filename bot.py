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

    #dlog('Starting Turn!')
    board_size = get_board_size()

    team = get_team()
    opp_team = Team.WHITE if team == Team.BLACK else team.BLACK
    same_team = Team.WHITE if team == Team.WHITE else team.BLACK
    #dlog('Team: ' + str(team))

    robottype = get_type()
    #dlog('Type: ' + str(robottype))


    if robottype == RobotType.PAWN:
        row, col = get_location()
        #dlog('My location is: ' + str(row) + ' ' + str(col))

        if team == Team.WHITE:
            forward = 1
            backward = -1
            index = 0
        else:
            forward = -1
            backward = 1
            index = board_size - 1

        tryCapture = True
        avoidCapture = True
        triangleFormation = True


        # One-stop status checker
        if (on_board(row + backward, col + 1)):
            if (check_space(row + backward, col + 1) == same_team):
                innerBackRight = True
            else:
                innerBackRight = False
        else:
            innerBackRight = False

        if (on_board(row + backward, col - 1)):
            if (check_space(row + backward, col - 1) == same_team):
                innerBackLeft = True
            else:
                innerBackLeft = False
        else:
            innerBackLeft = False

        if (on_board(row + 2*backward, col + 2)):
            if (check_space(row + (2*backward), col + 2) == same_team):
                outerBackRight = True
            else:
                outerBackRight = False
        else:
            outerBackRight = False

        if (on_board(row + 2*backward, col - 2)):
            if (check_space(row + (2*backward), col - 2) == same_team):
                outerBackLeft = True
            else:
                outerBackLeft = False
        else:
            outerBackLeft = False

        if (on_board(row + 2*backward, col)):
            if (check_space(row + (2*backward), col) == same_team):
                outerBackCenter = True
            else:
                outerBackCenter = False
        else:
            outerBackCenter = False

        if (on_board(row + forward, col + 1)):
            if (check_space(row + forward, col + 1) == same_team):
                innerFrontRight = True
            else:
                innerFrontRight = False
        else:
            innerFrontRight = False

        if (on_board(row + forward, col - 1)):
            if (check_space(row + forward, col - 1) == same_team):
                innerFrontLeft = True
            else:
                innerFrontLeft = False
        else:
            innerFrontLeft = False

        if (on_board(row, col + 2)):
            if (check_space(row, col + 2) == same_team):
                outerRight = True
            else:
                outerRight = False
        else:
            outerRight = False

        if (on_board(row, col - 2)):
            if (check_space(row, col - 2) == same_team):
                outerLeft = True
            else:
                outerLeft = False
        else:
            outerLeft = False

        if (on_board(row + 2*forward, col + 2)):
            if (check_space(row + 2*forward, col + 2) == same_team):
                outerFrontRight = True
            else:
                outerFrontRight = False
        else:
            outerFrontRight = False

        if (on_board(row + 2*forward, col)):
            if (check_space(row + 2*forward, col) == same_team):
                outerFrontCenter = True
            else:
                outerFrontCenter = False
        else:
            outerFrontCenter = False

        if (on_board(row + 2*forward, col - 2)):
            if (check_space(row + 2*forward, col - 2) == same_team):
                outerFrontLeft = True
            else:
                outerFrontLeft = False
        else:
            outerFrontLeft = False



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
            elif (on_board(row + (2*forward), col - 1)):
                if (check_space(row + (2*forward), col - 1) == opp_team):
                    if (check_space(row + forward, col - 1) == same_team):
                        move_forward()
                        dlog('Would\'ve waited, but had to sacrifice to avoid stalemate')
                        return
                    else:
                        dlog('Waited patiently')
                        return
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

        if(triangleFormation):
            # tertiary pawn escape clause
            if(row == index + 2*forward and (outerRight and outerLeft)):
                if(on_board(row + forward, col) and not check_space_wrapper(row + forward, col, board_size)):
                    move_forward()
                    return

            # for leading pawn
            if(row == index and not (innerFrontRight or innerFrontLeft)): # identifies front pawn
                if(on_board(row + forward, col) and not check_space_wrapper(row + forward, col, board_size)):
                    move_forward()
                    return
            elif (row == index + forward and (innerBackLeft or innerBackRight)):
                if (innerBackLeft and innerBackRight):
                    if(on_board(row + forward, col) and not check_space_wrapper(row + forward, col, board_size)):
                        move_forward()
                        return
                else:
                    # wait
                    return
            elif (row == index + 2*forward and (outerBackLeft or outerBackRight or outerBackCenter)):
                if (outerBackLeft and outerBackRight and outerBackCenter):
                    if(on_board(row + forward, col) and not check_space_wrapper(row + forward, col, board_size)):
                        move_forward()
                        return
                else:
                    # wait
                    return

            # for secondary pawns
            if(row == index and (outerLeft or outerRight) and not (outerLeft and outerRight)): #identifies secondary pawn. tertiary pawns will be spawned far right, then far left, then center to make them identifiable
                if(outerRight and innerFrontRight):
                    if(on_board(row + forward, col) and not check_space_wrapper(row + forward, col, board_size)):
                        move_forward()
                        return
                elif(outerLeft and innerFrontLeft):
                    if(on_board(row + forward, col) and not check_space_wrapper(row + forward, col, board_size)):
                        move_forward()
                        return
                else:
                    # wait
                    return
            elif(row == index and not (outerLeft or outerRight)):
                # wait
                return
            elif(row == index + forward and not (innerFrontRight or innerFrontLeft)):
                if(on_board(row + forward, col) and not check_space_wrapper(row + forward, col, board_size)):
                    move_forward()
                    return
            elif(row == index + forward and (innerFrontRight or innerFrontLeft) and not (outerFrontRight or outerFrontCenter)):
                 # wait
                 return

            # for tertiary pawns
            if(row == index and (outerRight or outerLeft)):
                if(on_board(row + forward, col) and not check_space_wrapper(row + forward, col, board_size)):
                    move_forward()
                    return




            



        

        #avoid capture 
        #if it senses an enemy pawn in the top right or left, don't move.

        if (row + forward != -1 and row + forward != board_size and not check_space_wrapper(row + forward, col, board_size)):
                move_forward()
                return



        

        confusion = "you need a line here to avoid segfault. we aren't sure why but are working on it"
        # ^ I think this is related to the potential ambiguity of what the following else is referring to?

    else:
        
        # added this boolean so we don't waste bytecode on spawn loops if something's already been spawned
        hasSpawned = False

        # critRow refers to the critical row that the overlord checks to see if there are any enemies in order to spawn defensive pawns
        if team == Team.WHITE:
            index = 0
            critRow = 2
            forward = 1
            backward = -1
            opp_index = board_size - 1
        else:
            index = board_size - 1
            critRow = board_size - 3
            forward = -1
            backward = 1
            opp_index = 0

        spawnDefense = True
        spawnRandom = True
        spawnFormation = True

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

        # doesn't spawn formations if the pawns are building up on the opposite side
        if(check_space(opp_index, 8) == same_team and check_space(opp_index + backward, 8) == same_team):
            spawnFormation = False


        if(spawnFormation):
            if(not check_space(index, 8) == same_team and not check_space(index + forward, 7) == same_team and not check_space(index+forward, 8)):
                spawn(index, 8)
                return
            elif(check_space(index + forward, 8) == same_team and not check_space(index + 2*forward, 7)): # if only leader pawn
                if(not check_space(index, 7) == same_team):
                    spawn(index, 7)
                    return
                elif(not check_space(index, 9) == same_team):
                    spawn(index, 9)
                    return
                else:
                    dlog("Some error happened when spawning row 2")
            if(check_space(index + 2*forward, 8) == same_team and check_space(index + forward, 7) == same_team and check_space(index + forward, 9)):
                if(not check_space(index, 10)):
                    spawn(index, 10)
                    return
                elif(not check_space(index, 6)):
                    spawn(index, 6)
                    return
                elif(not check_space(index, 8)):
                    spawn(index, 8)
                    return

                 



        if(spawnRandom):
            if not hasSpawned:
                for _ in range(board_size):
                    i = random.randint(0, board_size - 1, 2)
                    if not check_space(index, i):
                        spawn(index, i)
                        dlog('Spawned unit at: (' + str(index) + ', ' + str(i) + ')')
                        break

        bytecode = get_bytecode()
        dlog('Done! Bytecode left: ' + str(bytecode))