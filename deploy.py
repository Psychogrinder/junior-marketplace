from dialog import Dialog
from abc import abstractclassmethod, ABC
import os
import subprocess


class ScriptInterface(ABC):

    @abstractclassmethod
    def get_name(self):
        pass

    @abstractclassmethod
    def execute(self):
        pass


class DeployScript(ScriptInterface):

    def __init__(self, name, script_dir, script_name, work_dir):
        self.name = name
        self.script_dir = script_dir
        self.script_name = script_name
        self.wd = work_dir

    def get_name(self):
        return self.name

    def execute(self):
        script_dir = os.path.join(self.wd, self.script_dir)
        proc = subprocess.Popen(
            [self.script_name, '-d'],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            cwd=script_dir
        )
        return proc


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
            code = self.dialog.programbox(fd=proc.stdout.fileno(), text=chosen_task.get_name())


def main():
    work_dir = os.path.dirname(os.path.abspath(__file__))
    tasks = [
        DeployStageScript('Деплой приложения на стейдж', 'marketplace.app', './deploy-stage.sh', work_dir),
        DeployStageScript('Деплой бд на стейдж', 'marketplace.db', './deploy-stage.sh', work_dir),
    ]
    App(Dialog(), tasks).run()


if __name__ == '__main__':
    main()
