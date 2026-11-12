from fastapi import FastAPI,HTTPException
from pydantic import BaseModel

app = FastAPI()

class Report(BaseModel):
    id: int
    title: str
    status: str

reports=[]

@app.get("/reports")
def get_reports():
    return reports

@app.post("/reports")
def add_report(report: Report):
    reports.append(report)
    return report



@app.get("/reports/{report_id}")
def get_report(report_id: int):
    for report in reports:
        if report.id == report_id:
            return report
    raise HTTPException(status_code=404, detail="Report not found")

@app.put("/reports/{report_id}")
def update_report(report_id: int, updated_report: Report):
    for index,report in enumerate(reports):
        if report.id == report_id:
            reports[index] = updated_report
            return updated_report



@app.delete("/reports/{report_id}")
def delete_report(report_id: int):
    for index,report in enumerate(reports):
        if report.id == report_id:
            deleted=reports.pop(index)

            return {
                "message": "Report deleted",
                "product": deleted
            }
