from pynput import keyboard
import copy
import json
import os


class Main:

    matrix = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
              [2, 0, 0, 3, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
              [1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
              [1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
              [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
              [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
              [1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
              [1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
              [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
              [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1],
              [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
              [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1],
              [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
              [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 3, 1],
              [1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1]]
    # дорога = 0, стена = 1, старт = 2, финиш = 3
    start_pos = {'x': 1, 'y': 0}    #стартовая позиция
    real_pos = {'x': 1, 'y': 0}     #реальная позиция
    end_pos = {}                    #предыдушая позиция

    def __init__(self):
        self.load_flag = False
        #проверка на наличие сохранения
        if self.load_game() != self.load_flag:
            #если имеется сохраненная и предлогаем загрузить
            self.do_you_load_game()
        self.flag_game = True
        print('Ваш ход =>')
        with keyboard.Listener(on_press=self.press) as listener:
            listener.join()

    def do_you_load_game(self):
        print('Загрузить сохраненную игру?')
        yes = input('Нажмите "y" для загрузки или "n" чтобы начать заново:')
        if yes == 'y':
            self.load_game()
        elif yes == 'n':
            os.remove('end_pos.json')
            self.real_pos = self.start_pos

    # значение позиции в матрице
    def position(self, a):
        if a == 0:
            print('\nШарик нашел правильный путь!\nСделайте следующий ход.')
        elif a == 1:
            print('\nШарик ударился о стену\nИгра закончена!\n')
            self.real_pos = self.end_pos
            self.save_game()
        elif a == 2:
            print('\nШарик шарик струсил и убежал\nИгра закончена!\n')
            self.real_pos = self.end_pos
            self.save_game()
        elif a == 3:
            print('\nШарик прошел через все оптимальные ходы\nПоздравляем с победой!')
            self.real_pos = self.start_pos
            self.new_game()

    # сохранение игры
    def save_game(self):
        print('Сохранить прогресс?')
        s = input('Нажмите "y" для сохранения или "n" для отмены: ')
        if s == 'y':
            with open('end_pos.json', 'w') as save:
                json.dump(self.real_pos, save)
                print('Игра сохранена\n')
                self.new_game()
        elif s == 'n':
            self.flag_game = False
            self.new_game()

    #загрузка игры
    def load_game(self):
        try:
            with open('end_pos.json') as load_save:
                self.real_pos = json.load(load_save)
                return self.real_pos
        except:
            return False

    def new_game(self):
        print('Начать игру заново?')
        restart = input('Нажмите "y" чтобы вернуться к предыдушему ходу,"r" чтобы начать заново или "n" для выхода:')
        if restart == 'y':
            self.real_pos = self.end_pos
            self.flag_game = True
        elif restart == 'r':
            self.real_pos = self.start_pos
            self.flag_game = True
            print('Ваш ход =>')
        elif restart == 'n':
            self.flag_game = False
        pass

    #распознование нажатия клавиш
    def press(self, event):
        self.end_pos = copy.copy(self.real_pos)
        if self.flag_game is False:
            return False
        elif event == keyboard.Key.up:
            self.real_pos['x'] -= 1
            self.position(self.matrix[self.real_pos['x']][self.real_pos['y']])
        elif event == keyboard.Key.down:
            self.real_pos['x'] += 1
            self.position(self.matrix[self.real_pos['x']][self.real_pos['y']])
        elif event == keyboard.Key.left:
            self.real_pos['y'] -= 1
            self.position(self.matrix[self.real_pos['x']][self.real_pos['y']])
        elif event == keyboard.Key.right:
            self.real_pos['y'] += 1
            self.position(self.matrix[self.real_pos['x']][self.real_pos['y']])
        elif event == keyboard.Key.esc:
            self.save_game()
            print('Игра закончена')
            self.flag_game = False
        else:
            pass
     #jhiugiujhkujghjhkjgjhgkgfyugbbhjgv

Main()
