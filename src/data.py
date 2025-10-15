import datetime
import os
from src.constants import FAILED, SUCCESS, NOUNDO
from src.getname import getname
import shutil

class Data:
    def __init__(self, init_dir, last_exec=None, fr_dir=None, sc_dir=None):
        '''
        Класс для хранения информации об исходной директории и команд для undo.
        :param init_dir: Начальная директория.
        :param last_exec: Последняя выполненная команда из трёх: rm, cp, mv.
        :param fr_dir: Исходная директория, над которой проводилась команда.
        :param sc_dir: Конечная директория, в которую перемещали файлы.
        '''
        self.init_dir = init_dir
        self.last_exec = last_exec
        self.fr_dir = fr_dir
        self.sc_dir = sc_dir

    def log(self, s, userprint=True):
        '''
        Сохраняет логи в файл shell.log, находящийся в исходной директории.
        :param s: Текст для лога.
        :param userprint: Выводит этот же текст в консоль по умолчанию.
        :return: Ничего не возвращает.
        '''
        if userprint:
            print(s)
        with open(f"{self.init_dir}\\shell.log", "a") as f:
            f.write(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {s}\n")

    def hist(self, s):
        '''
        Сохраняет команды пользователя в файл .history
        :param s: Введённая оманда.
        :return: Ничего не возвращает.
        '''
        with open(f"{self.init_dir}\\.history", "a") as f:
            f.write(f"{s}\n")

    def undo(self):
        '''
        Отменяет последнюю команду. Берет информацию о ней из data. Для mv - делает обратное перемещение,
        для cp - удаляет копию, для rm - перемещает из .trash
        :return: True, если команда была успешно отменена, иначе None.
        '''
        match self.last_exec:
            case "mv":
                try:
                    shutil.move(f"{self.sc_dir}\\{getname(self.fr_dir)}", f"{self.fr_dir}\\..")
                    Data.log(self, SUCCESS)
                    return True
                except:
                    Data.log(self, FAILED)

            case "cp":
                try:
                    if os.path.isdir(self.fr_dir):
                        try:
                            shutil.rmtree(f"{self.sc_dir}\\{getname(self.fr_dir)}")
                        except:
                            Data.log(self, FAILED)
                            return
                    else:
                        try:
                            os.remove(f"{self.sc_dir}\\{getname(self.fr_dir)}")
                        except:
                            Data.log(self, FAILED)
                            return
                    Data.log(self, SUCCESS)
                    return True
                except:
                    Data.log(self, FAILED)

            case "rm":
                if os.path.isdir(self.fr_dir):
                    try:
                        shutil.move(f"{self.init_dir}\\.trash\\{getname(self.fr_dir)}", f"{self.fr_dir}\\..")
                    except:
                        Data.log(self, FAILED)
                        return
                else:
                    try:
                        shutil.move(f"{self.init_dir}\\.trash\\{getname(self.fr_dir)}", f"{self.fr_dir}\\..")
                    except:
                        Data.log(self, FAILED)
                        return
                Data.log(self, SUCCESS)
                return True

            case None:
                Data.log(self, NOUNDO)





