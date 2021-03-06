# -*- coding: utf-8 -*-
# ////////////////////////////////////////////////////////////////////////// #
#
#  モジュールインポート
#
# ////////////////////////////////////////////////////////////////////////// #
import os
import sys
sys.path.append(os.path.join('..', 'rakudasu_project'))
from rakudasu_project import settings
import argparse
import time
import datetime
import traceback
import shutil
from sshtunnel import SSHTunnelForwarder
import pymysql
import pandas as pd
# import mysql.connector
# ------------------------------
#  オリジナルモジュール
# ------------------------------

# ////////////////////////////////////////////////////////////////////////// #
#
#  グローバル変数
#
# ////////////////////////////////////////////////////////////////////////// #
SSH_BASTION_ADDRESS = settings.SSH_BASTION_ADDRESS
SSH_PORT = int(settings.SSH_PORT)
SSH_USER = settings.SSH_USER
SSH_PKEY_PATH = settings.SSH_PKEY_PATH
MYSQL_HOST = settings.MYSQL_HOST
MYSQL_PORT = int(settings.MYSQL_PORT)
MYSQL_USER = settings.MYSQL_USER
MYSQL_PASS = settings.MYSQL_PASS
MYSQL_DB = settings.MYSQL_DB

work_type_Map = {
    1: 9, # SES
    2: 10, # 派遣
    3: 9, # 社内業務
    4: 12, # 出勤予定
    5: 13, # 受託
    6: 20, # 内勤
    None: '',
}

# ////////////////////////////////////////////////////////////////////////// #
#
#  Rakudasu クラス
#
# ////////////////////////////////////////////////////////////////////////// #
# -------------------------------------------------------------------------- #
#  クラス名    Rakudasu
#  説明        Rakudasu 操作用クラス
#  引数1       dict(コマンドライン引数)
# -------------------------------------------------------------------------- #
class Rakudasu:
    def __init__(self, request, pk=None):
        self.def_name = "init"
        request_data = dict(request.data)
        self.employee_id = request.user.get_employee_id()
        if request.method == "POST" or request.method == "PUT" or request.method == "PATCH":
            self.work_type = work_type_Map[request_data['work_type']]
            self.opening_time = request_data['opening_time']
            self.closing_time = request_data['closing_time']
            self.break_time = request_data['break_time']
            self.date = request_data['date'] + ' 00:00:00'
        if request.method == "PUT" or request.method == "PATCH" :
            self.attendance_details_id = request_data['attendance_details_id']
        if request.method == "DELETE":
            self.attendance_details_id = pk

    # ====================================================================== #
    #  関数名: select
    # ---------------------------------------------------------------------- #
    #  説明: DBに接続し、SQL文を実行
    #  返り値: dataframe or error_code
    # ====================================================================== #
    def select(self, q):
        self.def_name = "select"
        description = f'Processing of "{self.def_name}" function is started.'
        self.printLog("INFO", f'[ OK ] {description}')

        # メインコード
        try:
            with SSHTunnelForwarder(
                (SSH_BASTION_ADDRESS, SSH_PORT),
                ssh_pkey=SSH_PKEY_PATH,
                ssh_username=SSH_USER,
                remote_bind_address=(MYSQL_HOST, MYSQL_PORT),
                # local_bind_address=(MYSQL_HOST, MYSQL_PORT),
            ) as server:
                conn = pymysql.connect(
                    host = MYSQL_HOST,
                    port = server.local_bind_port,
                    user = MYSQL_USER,
                    passwd = MYSQL_PASS,
                    db = MYSQL_DB,
                    charset = 'utf8',
                    cursorclass = pymysql.cursors.DictCursor
                )
                df = pd.read_sql_query(q, conn)
                conn.close()

                # ログ作業後処理
                message = f'"select" completed.'
                self.printLog("INFO", f"[ OK ] {message}")

                return df
        # ---------------------
        # エラーが発生した場合
        # ---------------------
        except Exception as e:
            message = f'{traceback.print_exc}'
            if e:
                message = e
            self.printLog("FATAL", f'!!!!!===== Exception =====!!!!!')
            self.printLog("FATAL", f'{message}')
            return 1

    # ====================================================================== #
    #  関数名: insert
    # ---------------------------------------------------------------------- #
    #  説明: DBに接続し、SQL文を実行
    #  返り値: int
    # ====================================================================== #
    def insert(self, q):
        self.def_name = "insert"
        description = f'Processing of "{self.def_name}" function is started.'
        self.printLog("INFO", f'[ OK ] {description}')

        # メインコード
        try:
            with SSHTunnelForwarder(
                (SSH_BASTION_ADDRESS, SSH_PORT),
                ssh_pkey=SSH_PKEY_PATH,
                ssh_username=SSH_USER,
                remote_bind_address=(MYSQL_HOST, MYSQL_PORT),
                # local_bind_address=(MYSQL_HOST, MYSQL_PORT),
            ) as server:
                conn = pymysql.connect(
                    host = MYSQL_HOST,
                    port = server.local_bind_port,
                    user = MYSQL_USER,
                    passwd = MYSQL_PASS,
                    db = MYSQL_DB,
                    charset = 'utf8',
                    cursorclass = pymysql.cursors.DictCursor
                )
                with conn.cursor() as cursor:
                    cursor.execute(q)
                    # オートコミットじゃないので、明示的にコミットを書く必要がある
                    conn.commit()
                    conn.close()

                # ログ作業後処理
                message = f'"insert" completed.'
                self.printLog("INFO", f"[ OK ] {message}")

                return 0
        # ---------------------
        # エラーが発生した場合
        # ---------------------
        except Exception as e:
            message = f'{traceback.print_exc}'
            if e:
                message = e
            self.printLog("FATAL", f'!!!!!===== Exception =====!!!!!')
            self.printLog("FATAL", f'{message}')
            return 1

    # ====================================================================== #
    #  関数名: excute
    # ---------------------------------------------------------------------- #
    #  説明: DBに接続し、SQL文を実行
    #  返り値: int
    # ====================================================================== #
    def excute(self, q):
        self.def_name = "excute"
        description = f'Processing of "{self.def_name}" function is started.'
        self.printLog("INFO", f'[ OK ] {description}')

        # メインコード
        try:
            with SSHTunnelForwarder(
                (SSH_BASTION_ADDRESS, SSH_PORT),
                ssh_pkey=SSH_PKEY_PATH,
                ssh_username=SSH_USER,
                remote_bind_address=(MYSQL_HOST, MYSQL_PORT),
                # local_bind_address=(MYSQL_HOST, MYSQL_PORT),
            ) as server:
                conn = pymysql.connect(
                    host = MYSQL_HOST,
                    port = server.local_bind_port,
                    user = MYSQL_USER,
                    passwd = MYSQL_PASS,
                    db = MYSQL_DB,
                    charset = 'utf8',
                    cursorclass = pymysql.cursors.DictCursor
                )
                with conn.cursor() as cursor:
                    cursor.execute(q)
                    # オートコミットじゃないので、明示的にコミットを書く必要がある
                    conn.commit()
                    conn.close()

                # ログ作業後処理
                message = f'"excute" completed.'
                self.printLog("INFO", f"[ OK ] {message}")

                return 0
        # ---------------------
        # エラーが発生した場合
        # ---------------------
        except Exception as e:
            message = f'{traceback.print_exc}'
            if e:
                message = e
            self.printLog("FATAL", f'!!!!!===== Exception =====!!!!!')
            self.printLog("FATAL", f'{message}')
            return 1

    # ====================================================================== #
    #  関数名: get_userInfo
    # ---------------------------------------------------------------------- #
    #  説明: employee ID をもとにユーザー情報を取得
    #  返り値: int
    # ====================================================================== #
    def get_userInfo(self):
        self.def_name = "get_userInfo"
        description = f'Processing of "{self.def_name}" function is started.'
        self.printLog("INFO", f'[ OK ] {description}')

        # メインコード
        try:
            sql = f'select name from users where id="{self.employee_id}";'
            df = self.select(sql)
            if len(df) == 1:
                self.user_name = df.at[0, 'name']
            if len(df) == 0:
                raise Exception(f'User of ID {self.employee_id} not found.')

            # ログ作業後処理
            message = f'"get_userInfo" completed.'
            self.printLog("INFO", f"[ OK ] {message}")

            return 0
        # ---------------------
        # エラーが発生した場合
        # ---------------------
        except Exception as e:
            message = f'{traceback.print_exc}'
            if e:
                message = e
            self.printLog("FATAL", f'!!!!!===== Exception =====!!!!!')
            self.printLog("FATAL", f'{message}')
            return 1

    # ====================================================================== #
    #  関数名: check_info
    # ---------------------------------------------------------------------- #
    #  説明: 取得した名前と登録情報が一致しているかチェック（社員かどうか）
    #  返り値: int
    # ====================================================================== #
    def check_info(self, fullname):
        self.def_name = "check_info"
        description = f'Processing of "{self.def_name}" function is started.'
        self.printLog("INFO", f'[ OK ] {description}')

        # メインコード
        try:
            if self.user_name == fullname:
                # ログ作業後処理
                message = f"The registration information matched with fullname ({fullname})."
                self.printLog("INFO", f"[ OK ] {message}")

            else:
                raise Exception(f'The registration information did not match with fullname ({fullname}).')
                return 1

            # ログ作業後処理
            message = f'"check_info" completed.'
            self.printLog("INFO", f"[ OK ] {message}")

            return 0
        # ---------------------
        # エラーが発生した場合
        # ---------------------
        except Exception as e:
            message = f'{traceback.print_exc}'
            if e:
                message = e
            self.printLog("FATAL", f'!!!!!===== Exception =====!!!!!')
            self.printLog("FATAL", f'{message}')
            return 1

    # ====================================================================== #
    #  関数名: get_latestAttendanceId
    # ---------------------------------------------------------------------- #
    #  説明: 最新の attendance IDを取得
    #  返り値: int
    # ====================================================================== #
    def get_latestAttendanceId(self):
        self.def_name = "get_attendanceId"
        description = f'Processing of "{self.def_name}" function is started.'
        self.printLog("INFO", f'[ OK ] {description}')

        # メインコード
        try:
            sql = f'select id from attendances where user_id={self.employee_id} order by id desc limit 1;'
            df = self.select(sql)
            if len(df) == 1:
                self.latestAttendanceId = df.at[0, 'id']

            # ログ作業後処理
            message = f'"get_latestAttendanceId" completed.'
            self.printLog("INFO", f"[ OK ] {message}")

            return 0
        # ---------------------
        # エラーが発生した場合
        # ---------------------
        except Exception as e:
            message = f'{traceback.print_exc}'
            if e:
                message = e
            self.printLog("FATAL", f'!!!!!===== Exception =====!!!!!')
            self.printLog("FATAL", f'{message}')
            return 1

    # ====================================================================== #
    #  関数名: check_attendance_details
    # ---------------------------------------------------------------------- #
    #  説明: 登録済みのデータを確認
    #  返り値: int
    # ====================================================================== #
    def check_attendance_details(self):
        self.def_name = "check_attendance_details"
        description = f'Processing of "{self.def_name}" function is started.'
        self.printLog("INFO", f'[ OK ] {description}')

        # メインコード
        try:
            sql = f'select * from attendance_details where user_id={self.employee_id} and attendance_id={self.latestAttendanceId} and work_type={self.work_type} and date="{self.date}" and deleted is NULL;'
            df = self.select(sql)
            if len(df) == 0:
                pass
            else:
                raise Exception('This work type data already exists.')

            # ログ作業後処理
            message = f'"get_latestAttendanceId" completed.'
            self.printLog("INFO", f"[ OK ] {message}")

            return 0
        # ---------------------
        # エラーが発生した場合
        # ---------------------
        except Exception as e:
            message = f'{traceback.print_exc}'
            if e:
                message = e
            self.printLog("FATAL", f'!!!!!===== Exception =====!!!!!')
            self.printLog("FATAL", f'{message}')
            return 1

    # ====================================================================== #
    #  関数名: calculate_working_hours
    # ---------------------------------------------------------------------- #
    #  説明: 仕事時間計算
    #  返り値: int
    # ====================================================================== #
    def calculate_working_hours(self):
        self.def_name = "calculate_working_hours"
        description = f'Processing of "{self.def_name}" function is started.'
        self.printLog("INFO", f'[ OK ] {description}')

        # メインコード
        try:
            s_time = datetime.datetime.strptime(self.opening_time, '%H:%M:%S')
            e_time = datetime.datetime.strptime(self.closing_time, '%H:%M:%S')
            b_time = datetime.datetime.strptime(self.break_time, '%H:%M:%S')
            # 仕事時間計算処理
            working_hours = e_time - s_time
            # 休憩時間も引く
            working_hours = datetime.datetime.strptime(str(working_hours), '%H:%M:%S')
            self.working_hours = working_hours - b_time

            # ログ作業後処理
            message = f'"calculate_working_hours" completed.'
            self.printLog("INFO", f"[ OK ] {message}")

            return 0
        # ---------------------
        # エラーが発生した場合
        # ---------------------
        except Exception as e:
            message = f'{traceback.print_exc}'
            if e:
                message = e
            self.printLog("FATAL", f'!!!!!===== Exception =====!!!!!')
            self.printLog("FATAL", f'{message}')
            return 1

    # ====================================================================== #
    #  関数名: commit_data
    # ---------------------------------------------------------------------- #
    #  説明: DBにデータを入れる
    #  返り値: int
    # ====================================================================== #
    def commit_data(self):
        self.def_name = "commit_data"
        description = f'Processing of "{self.def_name}" function is started.'
        self.printLog("INFO", f'[ OK ] {description}')

        # メインコード
        try:
            sql = f'''
            insert into attendance_details (
                user_id,
                attendance_id,
                work_type,
                opening_time,
                closing_time,
                break_time,
                working_hours,
                date,
                remarks,
                reason,
                modified_id,
                created,
                modified
            ) values (
                {self.employee_id},
                {self.latestAttendanceId},
                {self.work_type},
                '{self.opening_time}',
                '{self.closing_time}',
                '{self.break_time}',
                '{self.working_hours}',
                '{self.date}',
                NULL,
                NULL,
                {self.employee_id},
                now(),
                now()
            );'''
            df = self.insert(sql)

            # ログ作業後処理
            message = f'"commit_data" completed.'
            self.printLog("INFO", f"[ OK ] {message}")

            return 0
        # ---------------------
        # エラーが発生した場合
        # ---------------------
        except Exception as e:
            message = f'{traceback.print_exc}'
            if e:
                message = e
            self.printLog("FATAL", f'!!!!!===== Exception =====!!!!!')
            self.printLog("FATAL", f'{message}')
            return 1

    # ====================================================================== #
    #  関数名: get_attendance_detailsId
    # ---------------------------------------------------------------------- #
    #  説明: 登録した勤怠データのIDを取得
    #  返り値: int
    # ====================================================================== #
    def get_attendance_detailsId(self):
        self.def_name = "get_attendance_detailsId"
        description = f'Processing of "{self.def_name}" function is started.'
        self.printLog("INFO", f'[ OK ] {description}')

        # メインコード
        try:
            # created_at を使うのはめんどくさそう => and複数で無理やり
            sql = f'select * from attendance_details where user_id={self.employee_id} and attendance_id={self.latestAttendanceId} and work_type={self.work_type} and date="{self.date}" and deleted is NULL;'
            df = self.select(sql)
            if len(df) == 1:
                self.attendance_detailsId = df.at[0, 'id']
            else:
                raise Exception('Failed to get attendance_details_id.')

            # ログ作業後処理
            message = f'"get_attendance_detailsId" completed.'
            self.printLog("INFO", f"[ OK ] {message}")

            return int(self.attendance_detailsId)
        # ---------------------
        # エラーが発生した場合
        # ---------------------
        except Exception as e:
            message = f'{traceback.print_exc}'
            if e:
                message = e
            self.printLog("FATAL", f'!!!!!===== Exception =====!!!!!')
            self.printLog("FATAL", f'{message}')
            return None

    # ====================================================================== #
    #  関数名: update_commit_data
    # ---------------------------------------------------------------------- #
    #  説明: データ更新
    #  返り値: int
    # ====================================================================== #
    def update_commit_data(self):
        self.def_name = "update_commit_data"
        description = f'Processing of "{self.def_name}" function is started.'
        self.printLog("INFO", f'[ OK ] {description}')

        # メインコード
        try:
            sql = f'''
            update attendance_details set
                work_type={self.work_type},
                opening_time="{self.opening_time}",
                closing_time="{self.closing_time}",
                break_time="{self.break_time}",
                working_hours="{self.working_hours}",
                date="{self.date}"
                where id={self.attendance_details_id}
            ;'''

            df = self.excute(sql)

            # ログ作業後処理
            message = f'"update_attendance_data" completed.'
            self.printLog("INFO", f"[ OK ] {message}")

            return 0
        # ---------------------
        # エラーが発生した場合
        # ---------------------
        except Exception as e:
            message = f'{traceback.print_exc}'
            if e:
                message = e
            self.printLog("FATAL", f'!!!!!===== Exception =====!!!!!')
            self.printLog("FATAL", f'{message}')
            return 1

    # ====================================================================== #
    #  関数名: delete_commit_data
    # ---------------------------------------------------------------------- #
    #  説明: データ更新
    #  返り値: int
    # ====================================================================== #
    def delete_commit_data(self):
        self.def_name = "delete_commit_data"
        description = f'Processing of "{self.def_name}" function is started.'
        self.printLog("INFO", f'[ OK ] {description}')

        # メインコード
        try:
            sql = f'''
            delete from attendance_details where id={self.attendance_details_id};
            '''

            df = self.excute(sql)

            # ログ作業後処理
            message = f'"delete_commit_data" completed.'
            self.printLog("INFO", f"[ OK ] {message}")

            return 0
        # ---------------------
        # エラーが発生した場合
        # ---------------------
        except Exception as e:
            message = f'{traceback.print_exc}'
            if e:
                message = e
            self.printLog("FATAL", f'!!!!!===== Exception =====!!!!!')
            self.printLog("FATAL", f'{message}')
            return 1

    # ====================================================================== #
    #  関数名: printLog
    # ---------------------------------------------------------------------- #
    #  説明: ログ
    # ====================================================================== #
    def printLog(self, level, message):
        print(f'[{level}] {message}')

# ========================================================================== #
#  メインパート
# ========================================================================== #
def main():
    pass

if __name__ == "__main__":
    main()
