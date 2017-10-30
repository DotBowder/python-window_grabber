import os
import sys
import subprocess
from termcolor import colored

user_input_color = 'cyan'
highlight_1 = 'yellow'
highlight_2 = 'green'


class window():
    name = ''
    xdotool_id = ''
    pid = ''
    pos = ''
    size = ''
    def __init__(self, input_id='', search_term=''):

        print('Creating new python window class object.\nInputParams: input_id:({}) search_term:({})\n'.format(input_id, colored(search_term,highlight_2)))

        if input_id != '':          # If the input_id is not blank, assume the user has already defined the window they want.
            self.name, self.xdotool_id, self.pid, self.pos, self.size = self.xdotool_window_stat(input_id)
            print('Sucessfully associated user selected window with a window class object.')
        elif search_term != '':     # If the search_term is not blank, assume the user wants to search for the search term.
            self.search_windows(search_term=search_term, user_search=False)
        else:                       # If no inputs are given, prompt the user to search for a window.
            self.search_windows(user_search=True)


    def select_window_id(self, ids):
        # From a list of window ids, we will pull the stats of a window with xdotool, store the windows in a window_list,\
        # and request the user to select the desired window.
        x = 0
        window_list = {}
        for xdotool_id in ids:
            if xdotool_id != '': # due to the bytes to
                window_list[x] = self.xdotool_window_stat(xdotool_id, num=x)
                x += 1
            else:
                pass

        user_input = input(colored("\nPlease type the desired window number: ",user_input_color))
        user_window = window_list[int(user_input)]
        selected_window = '\nWindow:({}) Name:({})\nXdotool_ID:({}) PID:({}) Position:({}) Size:({})'.format(colored(int(user_input),highlight_1),colored(user_window[0],highlight_2),user_window[1],user_window[2],user_window[3],user_window[4])
        user_confirmation = input('You selected the following window:\n{}\n\n'.format(selected_window) + colored('Would you like to proceeed with this window? ',user_input_color) + colored('(y/n) ',highlight_1))
        if user_confirmation == 'y' or user_confirmation == 'Y':
            self.name, self.xdotool_id, self.pid, self.pos, self.size = window_list[int(user_input)]
            print('Sucessfully associated user selected window with a window class object.')
        else:
            print('Failed to associate user selected window with a window class object.')

    def xdotool_window_stat(self, xdotool_id, num=0, print_mode=True, update=False):
        # Pull the stats of a window with xdotool given it's xdotool_id.
        pid = subprocess.run(['xdotool', 'getwindowpid', '{}'.format(xdotool_id)], stdout=subprocess.PIPE).stdout.decode('utf-8').split('\n')[0]
        name = subprocess.run(['xdotool', 'getwindowname', '{}'.format(xdotool_id)], stdout=subprocess.PIPE).stdout.decode('utf-8').split('\n')[0]
        geometry = subprocess.run(['xdotool', 'getwindowgeometry', '{}'.format(xdotool_id)], stdout=subprocess.PIPE).stdout.decode('utf-8').split('\n')
        position_x = int(str(geometry[1].split(':')[1].split(' ')[1]).split(',')[0])
        position_y = int(str(geometry[1].split(':')[1].split(' ')[1]).split(',')[1])
        position = position_x, position_y
        size_x = int(geometry[2].split(':')[1].split(' ')[1].split('x')[0])
        size_y = int(geometry[2].split(':')[1].split(' ')[1].split('x')[1])
        size = size_x, size_y
        if print_mode == True:
            print('\nWindow:({}) Name:({})\nXdotool_ID:({}) PID:({}) Position:({}) Size:({})'.format(colored(num,highlight_1),colored(name,highlight_2),xdotool_id,pid,position,size))
        #self.name, self.xdotool_id, self.pid, self.pos, self.size = name,xdotool_id,pid,position,size
        return (name,xdotool_id,pid,position,size)

    def search_windows(self, search_term='', user_search=True):
        # Initiate a name-based search for a window.
        if user_search == True:
            search_term = input(colored("Look at the Title/Name of your desired capture window, and type a few letters of it here.\nAlternatively, enter 0 to list all windows:",user_input_color))
        if search_term == '0':
            self.searched_ids = (subprocess.run(['xdotool', 'search', '--any', '{}'.format('')], stdout=subprocess.PIPE).stdout).decode('utf-8').split('\n')
            if self.searched_ids[0] == '':
                print('Search found no windows... At all... 0.0 uhhhh.....')
                sys.exit(0)
            else:
                self.select_window_id(self.searched_ids)
        else:
            try:
                self.searched_ids = (subprocess.run(['xdotool', 'search', '--name', '{}'.format(search_term)], stdout=subprocess.PIPE).stdout).decode('utf-8').split('\n')
                if self.searched_ids[0] == '':
                    print('Search found no matching windows with the term: ({})'.format(colored(search_term,'red')))
                    sys.exit(0)
                else:
                    self.select_window_id(self.searched_ids)
            except:
                print(colored('\nInput Error - No Matching Windows - Program will now exit.', 'red'))
                sys.exit(0)

application_name = 'Window Grabber'
version = 0.01
print('\n------------------------------------------------')
print('Welcome to the {} application!\nVersion: {}\nTo start, follow the on-screen prompts.'.format(application_name, version))
print('------------------------------------------------\n')


def main():
    print('Would you like to use your mouse to select a window? y/n')
    userin = input()
    if userin == 'y':
        subprocess.run(['clear'])
        print('Please click on the desired window.')
        xdotool_id = subprocess.run(['xdotool', 'selectwindow'], stdout=subprocess.PIPE).stdout.decode('utf-8').split('\n')[0]
        new_window = window(input_id=xdotool_id)
        pass
    else:
        new_window = window() #(search_term='MyProgramName')

    print()
    print('Window Name:\t"{}'.format(new_window.name))
    print('Window ID:\t{}'.format(new_window.xdotool_id))
    print('Window PID:\t{}'.format(new_window.pid))
    print('Window POS:\t{}'.format(new_window.pos))
    print('Window SIze:\t{}'.format(new_window.size))

main()
