from database.DB_connect import DBConnect
from model.team import Team


class DAO():

    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct(YEAR) 
                    from teams t 
                    where `year` >= 1985 
                    order by `year` desc"""

        cursor.execute(query)

        for row in cursor:
            result.append(row["YEAR"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getTeamsOfYear(year):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select * 
                    from teams t 
                    where t.`year` = %s"""

        cursor.execute(query, (year,))

        for row in cursor:
            result.append(Team(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getSalaryOfTeams(year, idMap):
        conn = DBConnect.get_connection()
        result = {}
        cursor = conn.cursor(dictionary=True)
        query = """SELECT t.teamCode, t.ID, sum(s.salary) as totSalary
                    from lahmansbaseballdb.salaries s, lahmansbaseballdb.teams t, lahmansbaseballdb.appearances a
                    where s.`year` = t.`year` and t.`year` = a.`year`
                    and a.`year`= %s
                    and t.ID = a.teamID
                    and s.playerID = a.playerID
                    group by t.teamCode 
                    """
        cursor.execute(query, (year,))
        for row in cursor:
            result[idMap[row["ID"]]] = row["totSalary"]
        cursor.close()
        conn.close()
        return result
