from constants import *
import pymysql
import random


class TMyDB:
    def __init__(self, host, port, user, password, database):
        try:
            self.connection = pymysql.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database,
                cursorclass=pymysql.cursors.DictCursor
            )
            print('Connect!')
            self.cursor = self.connection.cursor()
        except Exception as ex:
            print(f'Error  : {ex}')

    def InsertTableBusDriver(self, full_name, bus_id, experience, class_num):
        insert_query = f'''
            INSERT INTO 
                `{TABLE_BUS_DRIVER}` (full_name, bus_id, experience, class_num) 
            VALUES 
                ('{full_name}', '{bus_id}', '{experience}', '{class_num}')
            '''
        self.cursor.execute(insert_query)
        self.connection.commit()

    def InsertTableSalary(self, experience, class_num, salary_sum):
        insert_query = f'''
            INSERT INTO 
                `{TABLE_SALARY}` (experience, class, salary_sum) 
            VALUES 
                ('{experience}', '{class_num}', '{salary_sum}')
            '''
        self.cursor.execute(insert_query)
        self.connection.commit()

    def InsertTableBus(self, state_number, type_id, route_id):
        insert_query = f'''
            INSERT INTO 
                `{TABLE_BUS}` (state_number, type_id, route_id) 
            VALUES 
                ('{state_number}', '{type_id}', '{route_id}')
            '''
        self.cursor.execute(insert_query)
        self.connection.commit()

    def InsertTableBusType(self, type_info, capacity):
        insert_query = f'''
            INSERT INTO 
                `{TABLE_BUS_TYPE}` (type_info, capacity) 
            VALUES 
                ('{type_info}', '{capacity}')
            '''
        self.cursor.execute(insert_query)
        self.connection.commit()

    def InsertTableRoute(self, route_num, time_start, time_end, time_interval, distance):
        insert_query = f'''
            INSERT INTO 
                `{TABLE_ROUTE}` (route_num, time_start, time_end, time_interval, distance) 
            VALUES 
                ('{route_num}', '{time_start}', '{time_end}', '{time_interval}', '{distance}')
            '''
        self.cursor.execute(insert_query)
        self.connection.commit()

    def PrintTableBusType(self):
        select_all_rows = f'SELECT * FROM {TABLE_BUS_TYPE}'
        self.cursor.execute(select_all_rows)
        rows = self.cursor.fetchall()
        for row in rows:
            print(row['type_info'], ' | ', row['capacity'])
        return rows

    def ex1_GetListDriver_v0(self, idRoute):
        select_all_rows = f'''
            SELECT 
                dr.id as id,
                full_name
            FROM 
                {TABLE_BUS_DRIVER} as dr
            LEFT JOIN `{TABLE_BUS}` AS bus ON dr.bus_id = bus.id
            WHERE route_id = {idRoute}
            '''
        self.cursor.execute(select_all_rows)
        rows = self.cursor.fetchall()
        return [{'id' : 'id', 'full_name' : 'ФИО'}] + rows

    def ex1_GetListDriver(self, id):
        select = f'''
            SELECT 
                dr.id as id,
                full_name,
                experience,
                class_num,
                salary_sum
            FROM 
                {TABLE_BUS_DRIVER} as dr
            LEFT JOIN `{TABLE_BUS}` AS bus ON dr.bus_id = bus.id
            WHERE route_id = {id}
            '''
        self.cursor.execute(select)
        rows = self.cursor.fetchall()
        return [{
            'id':'id', 
            'full_name':'ФИО', 
            'experience':'Опыт', 
            'class_num':'Класс', 
            'salary_sum':'Оклад (руб)'
            }] + rows

    def ex1_GetListRoute(self):
        select_all_rows = f'''
            SELECT 
                id,
                route_num as value
            FROM 
                {TABLE_ROUTE}
            '''
        self.cursor.execute(select_all_rows)
        rows = list(self.cursor.fetchall())
        return rows

    def ex2_GetListRoute(self):
        return self.ex1_GetListRoute()     
       
    def ex2_GetListBus(self, idRoute):
        select_all_rows = f'''
            SELECT 
                id,
                state_number
            FROM 
                {TABLE_BUS}
            WHERE route_id = {idRoute}
            '''
        self.cursor.execute(select_all_rows)
        rows = list(self.cursor.fetchall())
        return [{
            'id' : 'id', 
            'state_number' : 'Гос. Номер'
            }] + rows  

    def ex3_GetListRoute(self):
        return self.ex1_GetListRoute()

    def ex3_GetListTime(self, idRoute, isFinish):
        select= f'''
            SELECT 
                id,
                {'route_num,' if idRoute == -1 else ''}
                {'time_end' if isFinish else 'time_start'}
            FROM 
                {TABLE_ROUTE}
            {f'WHERE id = {idRoute}' if idRoute != -1 else ''}
            '''
        self.cursor.execute(select)

        rows = self.cursor.fetchall()
        keys = {'id' : 'id'}
        if isFinish:
            keys.update({'time_end' : 'Время конца'})
        else:
            keys.update({'time_start' : 'Время начала'})
        if idRoute == -1:
            keys.update({ 'route_num' : 'Номер маршрута'})

        return [keys] + rows

    def ex4_GetListRoute(self):
        return self.ex1_GetListRoute()

    def ex4_GetListDist(self, idRoute):

        select_all_rows = f'''
            SELECT 
                id,
                distance
            FROM 
                {TABLE_ROUTE}
            {f'WHERE id = {idRoute}' if idRoute != -1 else ''}
            '''
        self.cursor.execute(select_all_rows)

        rows = self.cursor.fetchall()
        return [{'id' : 'id', 'distance' : 'Протяженность (км)'}] + rows

    def ex5_GetListDriver(self):
        select_all_rows = f'''
            SELECT 
                id,
                full_name as value
            FROM 
                {TABLE_BUS_DRIVER}
            '''
        self.cursor.execute(select_all_rows)

        rows = self.cursor.fetchall()
        return rows

    def ex5_GetListBus(self, id):
        select_all_rows = f'''
            SELECT
                buss.id as id,
                buss.state_number as state_number,
                type.type_info as type_info,
                type.capacity as capacity
            FROM 
            (
                SELECT 
                    bus.id as id,
                    state_number,
                    bus.type_id as type_id
                FROM 
                    {TABLE_BUS_DRIVER} AS dr
                LEFT JOIN `{TABLE_BUS}` AS bus ON dr.bus_id = bus.id
                WHERE dr.id = {id}
            ) as buss
            LEFT JOIN `{TABLE_BUS_TYPE}` AS type ON type.id = buss.type_id
            
            '''
        self.cursor.execute(select_all_rows)
        rows = self.cursor.fetchall()
        return [{
            'id' : 'id', 
            'state_number' : 'Гос. номер', 
            'type_info':'Тип', 
            'capacity':'Вместимость (чел)'}] + rows

    def ex6_GetListBus(self):
        select_all_rows = f'''
            SELECT
                bus.id as id, 
                bus.state_number as value
            FROM `{TABLE_BUS}` as bus
            LEFT JOIN `{TABLE_BUS_TYPE}` AS type ON type.id = bus.type_id
            
            '''
        self.cursor.execute(select_all_rows)
        rows = self.cursor.fetchall()
        return rows

    def ex6_GetDrivers(self):
        select_all_rows = f'''
            SELECT
                id,
                full_name,
                experience,
                class_num,
                salary_sum	
            FROM `{TABLE_BUS_DRIVER}` as bus    
            '''
        self.cursor.execute(select_all_rows)
        rows = self.cursor.fetchall()
        return [{'id' : 'id', 'full_name':'ФИО', 'experience':'Опыт', 'class_num':'Класс', 'salary_sum':'Оклад'}] +  rows

    def ex6_AddDrivers(self, full_name, bus_id, experience, class_num):
        self.InsertTableBusDriver(full_name, bus_id, experience, class_num)


    def ex7_deleteBus(self, id):
        delete_rows = f'''
            DELETE 
            FROM `{TABLE_BUS}`
            WHERE id = {id}
            '''
        self.cursor.execute(delete_rows)
        self.connection.commit()

    def ex7_GetListBus(self):
        select_all_rows = f'''
            SELECT
                bus.id as id, 
                bus.state_number as value
            FROM `{TABLE_BUS}` as bus
            LEFT JOIN `{TABLE_BUS_TYPE}` AS type ON type.id = bus.type_id
            '''
        self.cursor.execute(select_all_rows)
        rows = self.cursor.fetchall()
        return rows 

    def ex7_GetListBusTable(self):
        select_all_rows = f'''
            SELECT
                buss.id as id,
                buss.state_number as state_number,
                type.type_info as type_info,
                type.capacity as capacity
            FROM `{TABLE_BUS}` as buss
            LEFT JOIN `{TABLE_BUS_TYPE}` AS type ON type.id = buss.type_id
            '''
        self.cursor.execute(select_all_rows)
        rows = self.cursor.fetchall()
        return [{'id' : 'id', 'state_number' : 'Гос. номер', 'type_info':'Тип', 'capacity':'Вместимость (чел)'}] + rows

    def ex8_GetRoute(self):
        return self.ex1_GetListRoute()

    def ex8_GetRouteTable(self):
        select_all_rows = f'''
            SELECT
                id,
                route_num,
                time_start,
                time_end,
                time_interval,
                distance
            FROM `{TABLE_ROUTE}` as buss
            '''
        self.cursor.execute(select_all_rows)
        rows = self.cursor.fetchall()
        return [{
            'id':'id', 
            'route_num':'Номер марш.', 
            'time_start':'Начинает', 
            'time_end':'Заканчивает', 
            'time_interval':'Интервал', 
            'distance':'Протяженность'}] + rows

    def ex8_changeDist(self, id, data):
        update_rows = f'''
            UPDATE `{TABLE_ROUTE}` 
            SET distance={data} WHERE id={id}
            '''
        self.cursor.execute(update_rows)
        self.connection.commit()

    def makeReportGetBus(self):
        select_all_rows = f'''
            SELECT 
                type.type_info as type,
                type.capacity as capacity,
                COUNT(*) as num
            FROM `Bus` as bus
            LEFT JOIN `BusType` as type on bus.type_id = type.id
            GROUP BY type.type_info
            '''
        self.cursor.execute(select_all_rows)
        rows = self.cursor.fetchall()
        return {
            'type':'Тип автобуса', 
            'capacity' : 'Вместимость', 
            'num':'Количество в автопарке'
            }, rows 

    def makeReportGetRoute(self):
        select_all_rows = f'''
            SELECT
                route_num,
                time_start,
                time_end,
                time_interval,
                distance
            FROM `{TABLE_ROUTE}` as buss
            '''
        self.cursor.execute(select_all_rows)
        rows = self.cursor.fetchall()
        return {
            'route_num':'Номер маршрута', 
            'time_start':'Начинает', 
            'time_end':'Заканчивает', 
            'time_interval':'Интервал', 
            'distance':'Протяженность'}, rows

    def makeReportGetDriver(self):
        select_all_rows = f'''
            SELECT
                full_name,
                class_num
            FROM `{TABLE_BUS_DRIVER}` as buss
            '''
        self.cursor.execute(select_all_rows)
        rows = self.cursor.fetchall()
        return {
            'full_name':'ФИО',
            'class_num':'Класс'}, rows
        

if __name__ == "__main__":
    DB = TMyDB(HOST, PORT, USER, PASS, DB_NAME)
    
    # DB.InsertTableBus('A345ОК', '11', '14')

    
    
    
    