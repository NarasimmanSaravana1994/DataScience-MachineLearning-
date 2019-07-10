from unittest import TestCase
from Naive import NaiveBayes

class TestConnector(TestCase):

    # MsSql Connection Passed
    def test_ConnectorMsSQl(self):
        ServerName = "MsSql"
        ServerIP = "bellsqlnew"
        UserID = "qa"
        Password = "bellqa"
        Database = "NORTHWIND"
        Port = "1433"
        SId = None
        s = NaiveBayes()
        Output = s.Connector(ServerName,ServerIP,UserID,Password,Database,Port,SId)
        self.assertTrue(Output)

    # Oracle Password expired
    def test_ConnectorOracle(self):
        ServerName= "Oracle"
        ServerIP= "10.0.0.9/orcl.ducenitchn.com"
        UserID= "PRODUCT_TEST"
        Password= "tiger"
        Database = "PRODUCT_TEST"
        Port = "1521"
        SId = "orcl"
        s = NaiveBayes()
        Output = s.Connector(ServerName,ServerIP,UserID,Password,Database,Port,SId)
        self.assertTrue(Output)

    # MySql Connection Passed
    def test_ConnectorMySql(self):
        ServerName = "MySql"
        ServerIP = "10.0.0.9"
        UserID = "root"
        Password = "root"
        Database = "northwind"
        Port = "3306"
        SId = None
        s = NaiveBayes()
        Output = s.Connector(ServerName, ServerIP, UserID, Password, Database, Port, SId)
        self.assertTrue(Output)

    # Postgre Connection Passed
    def test_ConnectorPostgre(self):
        ServerName = "Postgre"
        ServerIP = "10.0.0.9"
        UserID = "postgres"
        Password = "Temp1234"
        Database = "SSPLSRV3"
        Port = "5432"
        SId = None
        s = NaiveBayes()
        Output = s.Connector(ServerName,ServerIP,UserID,Password,Database,Port,SId)
        self.assertTrue(Output)

class TestFetchInput(TestCase):

    # MsSql fetching Input
    def test_FetchInput(self):
        ServerName = "MsSql"
        ServerIP = "bellsqlnew"
        UserID = "qa"
        Password = "bellqa"
        Database = "NORTHWIND"
        Port = "1433"
        SId = None
        s = NaiveBayes()
        Connection = s.Connector(ServerName, ServerIP, UserID, Password, Database, Port, SId)
        Query = "select * from SampleComments"
        Data = s.FetchInputData(Connection,Query)
        self.assertIsNotNone(Data)

# class TestDataProcessing(TestCase):




