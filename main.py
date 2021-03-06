import socket
import threading


class TicTacToe:

    def __init__(self):
        self.board = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]];
        self.turn = "X";
        self.you = "X";
        self.opponent = "O";
        self.winner = None;
        self.game_over = False;

        self.counter = 0;


    def host_game(self, host, port):
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
            server.bind((host, port));
            server.listen(1);
            print("Successfully hosted a new game, waiting for connection..");
            client, addr = server.accept();

            self.you = "X";
            self.opponent = "O";

            print("Game begins, you start!")
            self.print_board();

            threading.Thread(target=self.handle_connection, args=(client,)).start();
            server.close();
        except Exception as e:
            print(e);


    def connect_to_game(self, host, port):
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
            client.connect((host, port));

            self.you = "O";
            self.opponent = "X";

            print("Successfully connected to the game.");
            print("Games begins, opponent starts!");
            self.print_board();

            threading.Thread(target=self.handle_connection, args=(client,)).start();

        except Exception as e:
            print(e);


    def handle_connection(self, client):
        while not self.game_over:
            if self.turn == self.you:
                move = input("Enter a move (row, column): ");
                if self.check_valid_move(move.split(",")):
                    client.send(move.encode('utf-8'));
                    self.apply_move(move.split(","), self.you);
                    self.turn = self.opponent;
                else:
                    print("Invalid move!");
            else:
                data = client.recv(1024);
                if data:
                    self.apply_move(data.decode('utf-8').split(','), self.opponent);
                    self.turn = self.you;
                else:
                    break;

        print("Client closed.");
        client.close();


    def apply_move(self, move, player):
        if self.game_over:
            return;
        
        self.counter += 1;
        self.board[int(move[0])][int(move[1])] = player;
        self.print_board();
        self.check_if_won();
        if self.winner == self.you:
            print("You won!");
            exit();
        elif self.winner == self.opponent:
            print("You lost!");
            exit();
        else:
            if self.counter == 9:
                print("Its a tie!");
                exit();



    def check_valid_move(self, move):
        try:
            return self.board[int(move[0])][int(move[1])] == " ";
        except Exception as e:
            pass;



    def check_if_won(self):
        for row in range(3):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] != " ":
                self.winner = self.board[row][0];
                self.game_over = True;
                return True;
        
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != " ":
                self.winner = self.board[0][col];
                self.game_over = True;
                return True;

        if self.board[0][0] == self.board[1][1] == self.board[2][2] != " ":
            self.winner = self.board[0][0];
            self.game_over = True;
            return True;


        if self.board[0][2] == self.board[1][1] == self.board[2][0] != " ":
            self.winner = self.board[0][2];
            self.game_over = True;
            return True;

        return False;


    def print_board(self):
        print("\n");
        for row in range(3):
            print(" | ".join(self.board[row]));
            if row != 2:
                print("----------");


game = TicTacToe();
# game.host_game("localhost", 9999);
game.host_game("", 9999);
