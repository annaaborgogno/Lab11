from database.DB_connect import DBConnect
from model.arco import Arco
from model.product import Product


class DAO():

    @staticmethod
    def getAllColori():
        conn = DBConnect.get_connection()
        cursor = conn.cursor()
        res = []
        query = """select distinct (gp.Product_color)
                   from go_products gp """

        cursor.execute(query)

        for row in cursor:
            res.append(row)
        conn.close()
        cursor.close()
        return res

    @staticmethod
    def getNodes(color):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        res = []
        query = """select *
                    from go_products gp 
                    where gp.Product_color = %s """

        cursor.execute(query, (color,))

        for row in cursor:
            res.append(Product(**row))
        conn.close()
        cursor.close()
        return res

    @staticmethod
    def getArchi(year, color):
        conn = DBConnect.get_connection()
        cursor = conn.cursor()
        res = []
        query = """SELECT 
                        LEAST(gds.Product_number, gds2.Product_number) AS product1,
                        GREATEST(gds.Product_number, gds2.Product_number) AS product2,
                        COUNT(DISTINCT gds.`Date`) AS peso
                    FROM go_daily_sales gds, go_daily_sales gds2, go_products gp, go_products gp2 
                    WHERE gds.Product_number = gp.Product_number 
                    AND gds2.Product_number = gp2.Product_number 
                    AND gds.`Date` = gds2.`Date`
                    AND gds.Retailer_code = gds2.Retailer_code 
                    AND gds.Product_number != gds2.Product_number 
                    AND gp.Product_color = gp2.Product_color
                    AND YEAR(gds.`Date`) = %s 
                    AND gp.Product_color = %s
                    GROUP BY LEAST(gds.Product_number, gds2.Product_number), GREATEST(gds.Product_number, gds2.Product_number)
                    ORDER BY peso DESC"""

        cursor.execute(query, (year, color, ))

        for row in cursor:
            res.append(Arco(row['product1'],row['product2'],row['peso']))
        conn.close()
        cursor.close()
        return res