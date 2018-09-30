from dialog import Dialog
from abc import abstractclassmethod, ABC
import os
import subprocess


class ScriptInterface(ABC):

    def __init__(self, work_dir):
        self.wd = work_dir

    @abstractclassmethod
    def get_name(self):
        pass

    @abstractclassmethod
    def execute(self):
        pass


class DeployStageScript(ScriptInterface):

    NAME = 'Деплой стейдж'
    SCRIPT_DIR = 'marketplace.app'
    SCRIPT_NAME = './deploy-stage.sh'

    def get_name(self):
        return self.NAME 


    def execute(self):
        script_dir = os.path.join(self.wd, self.SCRIPT_DIR)
        s = ['docker-compose', '-f', 'docker-compose-stage.yml', 'up', '--build', '-d']
        proc = subprocess.Popen(s, stdout=subprocess.PIPE, cwd=script_dir)
        return proc


class FDReadAdapter:
    def __init__(self, fd):
        self.fd = fd

    def __getattribute__(self, attr):
        wrapped = object.__getattribute__(self, 'fd')
        print('-----------------', attr)
        if attr != 'read':
            return getattr(wrapped, attr)
        line = getattr(wrapped, attr)
        if line.startwith('+'):
            return line
        return '---'


class App:

    def __init__(self, dialog, tasks):
        self.dialog = dialog               
        self.tasks = tasks
    
    def run(self):
        menu_tasks_names = [(str(index), task.get_name()) for index, task in enumerate(self.tasks)]
        code, tag = self.dialog.menu('Выберите что нужно сделать', choices=menu_tasks_names)
        if code == Dialog.OK:
            chosen_task = self.tasks[int(tag)]
            proc = chosen_task.execute()
            code = self.dialog.programbox(fd=FDReadAdapter(proc.stdout).fileno(), text=chosen_task.get_name())


def main():
    work_dir = os.path.dirname(os.path.abspath(__file__))
    t = [DeployStageScript(work_dir) ]
    App(Dialog(), t).run()

if __name__ == '__main__':
    main()