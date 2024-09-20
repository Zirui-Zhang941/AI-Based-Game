import random
import copy
class TeekoPlayer:
    """ An object representation for an AI game player for the game Teeko.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']

    def __init__(self):
        """ Initializes a TeekoPlayer object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]
    
    

    def succ(self, state):
        output=[]
        count_r=0 # count the num that item in state is not ' ' 
        count_b=0
        for row in range(0,5):
            for col in range(0,5):
                if state[row][col]=='r':
                    count_r+=1
                if state[row][col]=='b':
                    count_b+=1
        
        if count_r==4 and count_b==4:
            drop_phase = False   # TODO: detect drop phase
        else:
            drop_phase = True
        
        if drop_phase:
            for row in range(0,5):
                for col in range(0,5):
                    if state[row][col] == ' ':
                        temp_state = copy.deepcopy(state)
                        temp_state[row][col] = self.my_piece
                        output.append(temp_state)
        else:
            for row in range(0,5):
                for col in range(0,5):
                    if state[row][col]==self.my_piece:
                        possible_rows=[row-1,row,row+1]
                        possible_cols=[col-1,col,col+1]
                        
                        for rows in possible_rows:
                            for cols in possible_cols:
                                
                                if rows>=0 and rows<5:
                                    if cols>=0 and cols<5:
                                        temp_state=copy.deepcopy(state)
                                        if temp_state[rows][cols]==' ':
                                            temp_state[row][col]=' '
                                            temp_state[rows][cols]=self.my_piece
                                            output.append(temp_state)
        return output
    
    def max_value(self, state, depth):
        a=self.game_value(state)
        if a==1 or a==-1:
            return a,state
        if depth>=2:
            return self.heuristic_game_value(state),state
        temp_succ=self.succ(state)
        inf=-1000
        output_state=state
        for item in temp_succ:
            value,_=self.min_value(item,depth+1)
            if value>inf:
                inf=value
                output_state=item
        return value,output_state
    
    def min_value(self, state, depth):
        a=self.game_value(state)
        if a==1 or a==-1:
            return a,state
        if depth>=2:
            return self.heuristic_game_value(state),state
        temp_succ=self.succ(state)
        inf=1000
        output_state=state
        for item in temp_succ:
            value,_=self.max_value(item,depth+1)
            if value<inf:
                inf=value
                output_state=item
        return value,output_state


    
    def make_move(self, state):
        """ Selects a (row, col) space for the next move. You may assume that whenever
        this function is called, it is this player's turn to move.

        Args:
            state (list of lists): should be the current state of the game as saved in
                this TeekoPlayer object. Note that this is NOT assumed to be a copy of
                the game state and should NOT be modified within this method (use
                place_piece() instead). Any modifications (e.g. to generate successors)
                should be done on a deep copy of the state.

                In the "drop phase", the state will contain less than 8 elements which
                are not ' ' (a single space character).

        Return:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

        Note that without drop phase behavior, the AI will just keep placing new markers
            and will eventually take over the board. This is not a valid strategy and
            will earn you no points.
        """

        

        # select an unoccupied space randomly
        # TODO: implement a minimax algorithm to play better
        move = []
        drop_phase = True
        count_r=0 # count the num that item in state is not ' ' 
        count_b=0
        for row in range(0,5):
            for col in range(0,5):
                if (state[row][col])=='r':
                    count_r+=1
                if (state[row][col])=='b':
                    count_b+=1
        
        if count_r==4 and count_b==4:
            drop_phase = False   # TODO: detect drop phase
        
        _,max_state=self.max_value(state,0)
        if not drop_phase:
            # TODO: choose a piece to move and remove it from the board
            # (You may move this condition anywhere, just be sure to handle it)
            #
            # Until this part is implemented and the move list is updated
            # accordingly, the AI will not follow the rules after the drop phase!
            new_row,new_col=0,0
            old_row,old_col=0,0
            for row in range(5):
                for col in range(5):
                    if state[row][col] != ' ' and max_state[row][col] == ' ':
                        old_row=row
                        old_col=col
                    elif max_state[row][col] != ' ' and state[row][col] == ' ':
                        new_row=row
                        new_col=col
            move = [(new_row, new_col), (old_row, old_col)]
        
        if drop_phase:
            for row in range(0,5):
                for col in range(0,5):
                    if max_state[row][col]!=' 'and state[row][col]==' ':
                        move.insert(0, (row, col))
        #(row,col)=self.compare_lists(state,expect_state)
        #(row,col)=(1,1)
        #(row, col) = (random.randint(0,4), random.randint(0,4))
        #while not state[row][col] == ' ':
        #   (row, col) = (random.randint(0,4), random.randint(0,4))

        # ensure the destination (row,col) tuple is at the beginning of the move list
        
        return move

    def compare_lists(list1, list2):
        # Check if the dimensions of the lists are the same
        if len(list1) != len(list2) or len(list1[0]) != len(list2[0]):
            return False  # Lists are of different dimensions

        # Iterate through the lists and compare elements
        for i in range(len(list1)):
            for j in range(len(list1[0])):
                if list1[i][j] != list2[i][j] and list2[i][j]!=' ':
                    return (i,j)  # Elements at the same position are different
    
        return None

    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                self.print_board()
                print(move)
                raise Exception("You don't have a piece there!")
            if abs(source_row - move[0][0]) > 1 or abs(source_col - move[0][1]) > 1:
                self.print_board()
                print(move)
                raise Exception('Illegal move: Can only move to an adjacent space')
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)

    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece

    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row)+": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")

    def game_value(self, state):
        """ Checks the current board status for a win condition

        Args:
        state (list of lists): either the current state of the game as saved in
            this TeekoPlayer object, or a generated successor state.

        Returns:
            int: 1 if this TeekoPlayer wins, -1 if the opponent wins, 0 if no winner

        TODO: complete checks for diagonal and box wins
        """
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i+1] == row[i+2] == row[i+3]:
                    return 1 if row[i]==self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i+1][col] == state[i+2][col] == state[i+3][col]:
                    return 1 if state[i][col]==self.my_piece else -1

        # TODO: check \ diagonal wins
        for row in range(0,2):
            for col in range(0,2):
                if state[row][col]!=' ' and state[row][col]==state[row+1][col+1]==state[row+2][col+2]==state[row+3][col+3]:
                    return 1 if state[row][col]==self.my_piece else -1

        # TODO: check / diagonal wins
        for row in range(3,5):
            for col in range(3,5):
                if state[row][col]!=' ' and state[row][col]==state[row-1][col-1]==state[row-2][col-2]==state[row-3][col-3]:
                    return 1 if state[row][col]==self.my_piece else -1
        # TODO: check box wins
        for row in range(0,4):
            for col in range(0,4):
                if state[row][col]!=' ' and state[row][col]==state[row+1][col]==state[row][col+1]==state[row+1][col+1]:
                    return 1 if state[row][col]==self.my_piece else -1
        return 0 # no winner yet

    
    def heuristic_game_value(self, state):

        term_value=self.game_value(state)
        if term_value==1 or term_value==-1:
            return term_value
        
        heur_value=0
        opp_value=0
        #check row
        for row in range(0,5):
            count=0
            opp_count=0
            for col in range(0,5):
                item=state[row][col]
                
                if item==self.my_piece:
                    count+=1
                elif item==self.opp:
                    opp_count+=1
            if count>opp_count:
                heur_value+=0.1
            elif count<opp_count:
                opp_value-=0.1
        #check col
        for col in range(0,5):
            count=0
            opp_count=0
            for row in range(0,5):
                item=state[row][col]
                
                if item==self.my_piece:
                    count+=1
                elif item==self.opp:
                    opp_count+=1
            if count>opp_count:
                heur_value+=0.1
            elif count<opp_count:
                opp_value-=0.1
        #check \
        for row in range(2):
            for col in range(2):
                item=state[row][col]
                count=0
                opp_count=0
                if item==self.my_piece:
                    for i in range(1,5):
                        next_row=row+i
                        next_col=col+i
                        if next_col<=4 and next_row<=4:
                            next_item=state[next_row][next_col]
                            if next_item==self.my_piece:
                                count+=1
                elif item==self.opp:
                    for i in range(1,5):
                        next_row=row+i
                        next_col=col+i
                        if next_col<=4 and next_row<=4:
                            next_item=state[next_row][next_col]
                            if next_item==self.opp:
                                opp_count+=1
                if count>opp_count:
                    heur_value+=0.1
                elif count<opp_count:
                    opp_value-=0.1
        
        #check /
        for row in range(3,5):
            for col in range(3,5):
                item=state[row][col]
                count=0
                opp_count=0
                if item==self.my_piece:
                    for i in range(1,5):
                        next_row=row-i
                        next_col=col-i
                        if next_col>=0 and next_row>=0:
                            next_item=state[next_row][next_col]
                            if next_item==self.my_piece:
                                count+=1
                elif item==self.opp:
                    for i in range(1,5):
                        next_row=row-i
                        next_col=col-i
                        if next_col>=0 and next_row>=0:
                            next_item=state[next_row][next_col]
                            if next_item==self.opp:
                                opp_count+=1
                if count>opp_count:
                    heur_value+=0.1
                elif count<opp_count:
                    opp_value-=0.1

        final_value=heur_value+opp_value
        return final_value


############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################
def main():
    print('Hello, this is Samaritan')
    ai = TeekoPlayer()
    piece_count = 0
    turn = 0

    # drop phase
    while piece_count < 8 and ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved at "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                player_move = input("Move (e.g. B3): ")
                while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                    player_move = input("Move (e.g. B3): ")
                try:
                    ai.opponent_move([(int(player_move[1]), ord(player_move[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        piece_count += 1
        turn += 1
        turn %= 2

    # move phase - can't have a winner until all 8 pieces are on the board
    while ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved from "+chr(move[1][1]+ord("A"))+str(move[1][0]))
            print("  to "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                move_from = input("Move from (e.g. B3): ")
                while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                    move_from = input("Move from (e.g. B3): ")
                move_to = input("Move to (e.g. B3): ")
                while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                    move_to = input("Move to (e.g. B3): ")
                try:
                    ai.opponent_move([(int(move_to[1]), ord(move_to[0])-ord("A")),
                                    (int(move_from[1]), ord(move_from[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        turn += 1
        turn %= 2

    ai.print_board()
    if ai.game_value(ai.board) == 1:
        print("AI wins! Game over.")
    else:
        print("You win! Game over.")


if __name__ == "__main__":
    
    main()
