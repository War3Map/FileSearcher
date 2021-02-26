import queue
import threading

import PySimpleGUI as sg

# Set theme for window
sg.theme('SystemDefault')
# All the stuff inside your window.
layout = [
    [sg.Text('Поиск файлов')],

    [sg.Text('Каталог для поиска'), sg.InputText(),
     sg.FolderBrowse("Выбрать")],

    [sg.Text('Тип поиска'), sg.Combo(
        ["Файлы", "Папки"], readonly=True,
        default_value="Файлы", size=(7, 1)
    )],

    [sg.Text('Включить расширения'),
     sg.InputText(default_text=".*", size=(25, 1))],

    [sg.Text('Исключить расширения'),
     sg.InputText(size=(25, 1))],

    [sg.Listbox(["Нет файлов"], size=(50, 10),
                enable_events=True, key='-LIST-'), ],

    [sg.Button('Начать поиск')]
]


def start_search(path_to_search, type_for_search, window_ref, res_queue):
    """
    Starts files search

    type path: str

    type search_type: str

    :return:
    """
    # TODO: результат вызова функции записывается в объект очередь
    # search_core.SomeClass.SomeFunction()
    res_queue.put([f"result {path_to_search} {type_for_search}"])
    # put a message into queue for GUI
    window_ref.write_event_value('-THREAD-', '** DONE **')


# Create the Window
window = sg.Window('Поиск файлов', layout)
searching_thread = None
out_queue = None

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    # if user closes window or clicks cancel
    if event == sg.WIN_CLOSED or event == 'Выйти':
        break
    # if clicks button 'Начать поиск'
    if event == 'Начать поиск':
        if searching_thread is None:
            source_path = str(values[0]).strip(''' '"''')
            search_type = values[1]
            print(f'Поиск в пути {source_path}...')

            # Queue used for getting results
            out_queue = queue.Queue()
            searching_thread = threading.Thread(target=start_search,
                                                args=(source_path,
                                                      search_type,
                                                      window,
                                                      out_queue),
                                                daemon=True)
            searching_thread.start()

    if event == "-THREAD-":
        result_list = out_queue.get()
        window['-LIST-'].update(result_list)
        print(result_list)
        print('Готово!')
        sg.Popup('Поиск закончен!')
        searching_thread = None

window.close()
