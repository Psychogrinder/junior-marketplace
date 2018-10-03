#!/usr/bin/env python3

from dialog import Dialog
from abc import abstractclassmethod, ABC
import os, sys, time
import subprocess


class MyDialog:

    NOT_EXIT = 1000

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
                try:
                    not_check = kwargs.pop('not_check_cancel')
                except KeyError:
                    not_check = False
                res = method(*args, **kwargs)
                if method == 'Yesno' and not_check:
                    return res
                if hasattr(method, "retval_is_code") \
                        and getattr(method, "retval_is_code"):
                    code = res
                else:
                    code = res[0]
                if self.check_exit_request(code, not_check):
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
    def __init__(self, dialog, work_dir, name):
        self.wd = work_dir
        self.dialog = dialog
        self.name = name

    def get_name(self):
        return self.name

    @abstractclassmethod
    def execute(self):
        pass

    def set_status(self, status):
        self.name = '{} -({})'.format(self.name, status)


class BaseScript(ScriptInterface):

    STDOUT = subprocess.PIPE
    STDERR = subprocess.DEVNULL

    def __init__(self, dialog, work_dir, name, script_dir, script_name):
        super().__init__(dialog, work_dir, name)
        self.script_dir = script_dir
        self.script_name = script_name
        self.proc_cmd = [script_name, '-d']

    def _running(self, proc):
        return self.dialog.programbox(fd=proc.stdout.fileno(), text=self.get_name())

    def _get_script_dir(self):
        return os.path.join(self.wd, self.script_dir) + '/'

    def _make_proc(self, cmd):
        proc = subprocess.Popen(
            cmd,
            stdout=self.STDOUT,
            stderr=self.STDERR,
            close_fds=True,
            cwd=self._get_script_dir()
        )
        return proc

    def _before_proc(self):
        return self.dialog.OK

    def _proc_done(self, code):
        return code

    def execute(self):
        if self.dialog.OK != self._before_proc():
            return self.dialog.NOT_EXIT
        proc = self._make_proc(self.proc_cmd)
        code = self._running(proc)
        return self._proc_done(code)


class GrafanaRunScript(BaseScript):
    URL = 'http://localhost:3000'

    def _running(self, proc):
        code = self.dialog.infobox(text=self.get_name())
        r_code = proc.wait()
        if r_code != 0:
            proc = self._make_proc(['docker', 'container', 'start', 'grafana'])
            r_code = proc.wait()
        code = self.dialog.msgbox('grafana запущена\n{}'.format(self.URL), extra_button=True, extra_label='Open')
        if code == self.dialog.EXTRA:
            self.STDOUT = subprocess.DEVNULL
            self._make_proc(['sensible-browser', self.URL])
            return self.dialog.OK
        return code


class PollingProcessScript(BaseScript):

    STDERR = subprocess.PIPE

    def _before_proc(self):
        return self.dialog.yesno('Выполнить {}?'.format(self.get_name()), not_check_cancel=True)

    def _process_polling(self, proc):
        process_indication = '|'
        while proc.poll() is None:
            self.dialog.infobox(text='Выполняется\n{}'.format(process_indication))
            time.sleep(0.2)
            process_indication += '|'
            if len(process_indication) > 7:
                process_indication = '|'
        return proc.poll()

    def _running(self, proc):
        r_code = self._process_polling(proc)
        if r_code != 0:
            err = proc.stderr.read().decode()
            self.dialog.scrollbox(err, width=80, height=20)
            return self.dialog.NOT_EXIT
        return self.dialog.OK

    def _proc_done(self, code):
        if code == self.dialog.OK:
            return self.dialog.msgbox('{} - выполнено'.format(self.get_name()))
        return code


class DBRestoreScript(PollingProcessScript):

    def _before_proc(self):
        super()._before_proc()
        code, dump_file_path = self.dialog.fselect(
            title='Выберите файл для восстановления БД',
            filepath=self._get_script_dir(),
            width=50,
            height=20
        )
        if os.path.splitext(dump_file_path)[1] != '.gz':
            self.dialog.msgbox('файл должен быть gzip формата')
            return self.dialog.CANCEL
        if code == self.dialog.OK:
            self.proc_cmd = [self.script_name, dump_file_path, 'create']
        return code


class App:
    def __init__(self, dialog, tasks):
        self.dialog = dialog
        self._check_task_instance_class(tasks)
        self.tasks = tasks

    def _check_task_instance_class(self, tasks):
        for section, tasks in tasks.items():
            for task in tasks:
                if not issubclass(task.__class__, ScriptInterface):
                    raise TypeError('{} не является наследником ScriptInterface'.format(task))

    def show_menu_sections(self):
        menu_sections = [(str(index), section) for index, section in enumerate(self.tasks.keys())]
        code, tag = self.dialog.menu('Выберите раздел', choices=menu_sections)
        section_id = menu_sections[int(tag)][1]
        return code, section_id

    def show_menu_tasks(self, section_key):
        menu_tasks = [(str(index), task.get_name()) for index, task in enumerate(self.tasks[section_key])]
        return self.dialog.menu(
            'Выберите что нужно сделать',
            choices=menu_tasks,
            extra_button=True,
            extra_label='Back'
        )

    def run(self):
        loop_code = self.dialog.OK
        while loop_code == self.dialog.OK:
            code, section_key = self.show_menu_sections()
            code, tag = self.show_menu_tasks(section_key)
            if code == self.dialog.EXTRA:
                continue
            chosen_task = self.tasks[section_key][int(tag)]
            loop_code = chosen_task.execute()
            if loop_code == self.dialog.OK:
                chosen_task.set_status('выполнен')
            elif loop_code == self.dialog.NOT_EXIT:
                loop_code = self.dialog.OK

        self.dialog.clear_screen()


def main():
    dialog = MyDialog(Dialog())
    work_dir = os.path.dirname(os.path.abspath(__file__))
    tasks = {
        'App': [
            BaseScript(dialog, work_dir, 'Деплой приложения на продакшен', 'marketplace.app', './deploy-prod.sh'),
            BaseScript(dialog, work_dir, 'Деплой приложения на стейдж', 'marketplace.app', './deploy-stage.sh'),
        ],
        'Monitoring': [
            GrafanaRunScript(dialog, work_dir, 'Запуск grafana', 'marketplace.monitoring', './grafana-run.sh'),
            PollingProcessScript(dialog, work_dir, 'Деплой сервисов мониторинга', 'marketplace.monitoring', './deploy-prod.sh'),
        ],
        'Nginx': [
            BaseScript(dialog, work_dir, 'Деплой nginx на продакшен', 'marketplace.nginx', './deploy-prod.sh'),
        ],
        'DB': [
            BaseScript(dialog, work_dir, 'Деплой БД на стейдж', 'marketplace.db', './deploy-stage.sh'),
            PollingProcessScript(dialog, work_dir, 'Дамп БД', 'marketplace.db', './db_dump.sh'),
            PollingProcessScript(dialog, work_dir, 'Дамп пользовательских картинок', 'marketplace.db', './dump_user_images.sh'),
            PollingProcessScript(dialog, work_dir, 'Применить миграции', 'marketplace.db', './make_migrations.sh'),
            DBRestoreScript(dialog, work_dir, 'Восстановление БД', 'marketplace.db', './db_restore.sh'),
        ],
    }

    App(dialog, tasks).run()


if __name__ == '__main__':
    main()
