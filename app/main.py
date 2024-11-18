
from fastapi import FastAPI
from database.db import test_db_connection
from routes.productTypeRoute import productTypeRouter
from routes.productRoute import productRouter
from routes.employeeRoute import employeeRouter
from routes.customerRoute import customerRouter
from routes.defectRoute import defectRouter
from routes.returnRequestRoute import returnRequestRouter
from routes.requestApprovalRoute import requestApprovalRouter
from routes.sortingRoute import sortingRouter
from routes.repairRoute import repairRouter

app = FastAPI()

##Routes
app.include_router(productTypeRouter, prefix="/productType", tags=["Product Type"])
app.include_router(productRouter, prefix="/product", tags=["Product"])
app.include_router(employeeRouter, prefix="/employee", tags=["Employee"])
app.include_router(customerRouter, prefix="/customer", tags=["Customer"])
app.include_router(defectRouter, prefix="/defect", tags=["Defect"])
app.include_router(returnRequestRouter, prefix="/returnRequest", tags=["Return Request"])
app.include_router(requestApprovalRouter, prefix="/requestApproval", tags=["Request Approval"])
app.include_router(sortingRouter, prefix="/sorting", tags=["Sorting"])
app.include_router(repairRouter, prefix="/repair", tags=["Repair"])

@app.get("/test-db-connection")
async def test_connection():
    return test_db_connection()