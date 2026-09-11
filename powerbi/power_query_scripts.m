// =============================================================================
// InsightBI AI — Power Query M Scripts
// File: powerbi/power_query_scripts.m
// =============================================================================

/* 
--------------------------------------------------------------------------------
1. Dynamic Calendar Table Generator (M Language)
--------------------------------------------------------------------------------
*/
let
    StartDate = #date(2023, 1, 1),
    EndDate = #date(2026, 12, 31),
    DayCount = Duration.Days(EndDate - StartDate) + 1,
    SourceList = List.Dates(StartDate, DayCount, #duration(1, 0, 0, 0)),
    TableFromList = Table.FromList(SourceList, Splitter.SplitByNothing(), {"Date"}, null, ExtraValues.Error),
    SetType = Table.TransformColumnTypes(TableFromList, {{"Date", type date}}),
    AddYear = Table.AddColumn(SetType, "Year", each Date.Year([Date]), Int64.Type),
    AddQuarter = Table.AddColumn(AddYear, "Quarter", each Date.QuarterOfYear([Date]), Int64.Type),
    AddMonth = Table.AddColumn(AddQuarter, "Month", each Date.Month([Date]), Int64.Type),
    AddMonthName = Table.AddColumn(AddMonth, "Month Name", each Date.MonthName([Date]), type text),
    AddDay = Table.AddColumn(AddMonthName, "Day", each Date.Day([Date]), Int64.Type),
    AddDayName = Table.AddColumn(AddDay, "Day Name", each Date.DayOfWeekName([Date]), type text),
    AddDateID = Table.AddColumn(AddDayName, "DateID", each Number.FromText(Date.ToText([Date], "yyyyMMdd")), Int64.Type)
in
    AddDateID

/*
--------------------------------------------------------------------------------
2. PostgreSQL Fact Sales Connection Query
--------------------------------------------------------------------------------
*/
/*
let
    ServerHost = "localhost",
    DatabaseName = "insightbi",
    Source = PostgreSQL.Database(ServerHost, DatabaseName),
    public_fact_sales = Source{[Schema="public", Item="fact_sales"]}[Data],
    FilterActiveDate = Table.SelectRows(public_fact_sales, each [revenue] >= 0)
in
    FilterActiveDate
*/

/*
--------------------------------------------------------------------------------
3. REST API Data Connector M Script (FastAPI Backend Ingestion)
--------------------------------------------------------------------------------
*/
/*
let
    ApiUrl = "http://localhost:8000/api/analytics/summary",
    Response = Web.Contents(ApiUrl, [Headers=[#"Accept"="application/json"]]),
    JsonResponse = Json.Document(Response),
    KpisRecord = JsonResponse[kpis],
    KpisTable = Record.ToTable(KpisRecord)
in
    KpisTable
*/
