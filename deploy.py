#!/usr/bin/env python3

from dialog import Dialog
from abc import abstractclassmethod, ABC
import os, sys
import subprocess


class MyDialog:

    def __init__(self, Dialog_instance):
        self.dlg = Dialog_instance

    def check_exit_request(self, code, ignore_Cancel=False):
        if code == self.CANCEL and ignore_Cancel:
            return True
        if code in (self.CANCEL, self.ESC):
            msg = "Закрыть?"
            if self.dlg.yesno(msg) == self.OK:
                self.clear_screen()
                sys.exit(0)
            else:
                return False
        else:
            return True

    def widget_loop(self, method):
        def wrapper(*args, **kwargs):
            while True:
                res = method(*args, **kwargs)
                if hasattr(method, "retval_is_code") \
                        and getattr(method, "retval_is_code"):
                    code = res
                else:
                    code = res[0]
                if self.check_exit_request(code):
                    break
            return res
        return wrapper

    def __getattr__(self, name):
        obj = getattr(self.dlg, name)
        if hasattr(obj, "is_widget") and getattr(obj, "is_widget"):
            return self.widget_loop(obj)
        else:
            return obj

    def clear_screen(self):
        program = "clear"
        try:
            p = subprocess.Popen(
                [program],
                shell=False,
                stdout=None,
                stderr=None,
                close_fds=True
            )
            p.wait()
        except os.error as e:
            return

    def _Yesno(self, *args, **kwargs):
        while True:
            code = self.dlg.yesno(*args, **kwargs)
            if self.check_exit_request(code, ignore_Cancel=True):
                break

        return code

    def Yesno(self, *args, **kwargs):
        return self._Yesno(*args, **kwargs) == self.dlg.OK


class ScriptInterface(ABC):

    def __init__(self, dialog, work_dir):
        self.wd = work_dir
        self.dialog = dialog

    @abstractclassmethod
    def get_name(self):
        pass

    @abstractclassmethod
    def execute(self):
        pass


class GrafanaRunScript(ScriptInterface):

    NAME = 'Запуск grafana'
    SCRIPT_DIR = 'marketplace.monitoring'
    SCRIPT_NAME = './grafana-run.sh'

    def get_name(self):
        return self.NAME

    def _make_proc(self, cmd):
        script_dir = os.path.join(self.wd, self.SCRIPT_DIR)
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=script_dir
        )
        return proc

    def _running(self, proc):
         return self.dialog.infobox(text=self.get_name())

    def execute(self):
        proc = self._make_proc([self.SCRIPT_NAME])
        self._running(proc)
        r_code = proc.wait()
        if r_code != 0:
            proc = self._make_proc(['docker', 'container', 'start', 'grafana'])
            r_code = proc.wait()
        return self.dialog.msgbox('grafana запущена\nhttp://localhost:3000')


class DeployScript(ScriptInterface):

    def __init__(self, dialog, name, script_dir, script_name, work_dir):
        self.dialog = dialog
        self.name = name
        self.script_dir = script_dir
        self.script_name = script_name
        self.wd = work_dir

    def get_name(self):
        return self.name

    def _running(self, proc):
         return self.dialog.programbox(fd=proc.stdout.fileno(), text=self.get_name())

    def execute(self):
        script_dir = os.path.join(self.wd, self.script_dir)
        proc = subprocess.Popen(
            [self.script_name, '-d'],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            close_fds=True,
            cwd=script_dir
        )
        return self._running(proc)


class App:

    def __init__(self, dialog, tasks):
        self.dialog = dialog
        self.tasks = tasks

    def run(self):
        loop_code = self.dialog.OK
        while loop_code == self.dialog.OK:
            menu_tasks = [(str(index), task.get_name()) for index, task in enumerate(self.tasks)]
            code, tag = self.dialog.menu('Выберите что нужно сделать', choices=menu_tasks)
            if code == Dialog.OK:
                chosen_task = self.tasks[int(tag)]
                loop_code = chosen_task.execute()

                if len(self.tasks) > 1:
                    del self.tasks[int(tag)]
                else:
                    break

        self.dialog.clear_screen()

def main():
    dialog = MyDialog(Dialog())
    work_dir = os.path.dirname(os.path.abspath(__file__))
    tasks = [
        DeployScript(dialog, 'Деплой приложения на стейдж', 'marketplace.app', './deploy-stage.sh', work_dir),
        DeployScript(dialog, 'Деплой бд на стейдж', 'marketplace.db', './deploy-stage.sh', work_dir),
        GrafanaRunScript(dialog, work_dir)
    ]
    App(dialog, tasks).run()


if __name__ == '__main__':
    main()
