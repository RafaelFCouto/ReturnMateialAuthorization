from datetime import datetime
from sqlalchemy.orm import Session
from models.repair import Repair
from typing import List, Dict
from utils.generateUUID import GenerateUUID


class RepairService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def getAllRepairs(self) -> List[Dict]:
        try:
            repairs = self.db_session.query(Repair).all()
            return [repair.as_dict() for repair in repairs]
        except Exception as e:
            raise Exception(f"Error listing Repairs: {e}")

    def getRepairById(self, repairId: str) -> Dict:
        try:
            repair = self.__getRepairByAtt('repairId', repairId)
            if not repair:
                raise ValueError(f"Repair with ID '{repairId}' not found.")
            return repair.as_dict()
        except Exception as e:
            raise Exception(f"Error finding Repair: {e}")

    def createRepair(self, data: Repair) -> Repair:
        try:
            repair_id = GenerateUUID.generate_uuid()
            repair_start_date = datetime.now()

            repair = Repair(
                repairId = repair_id,
                repair_start_date=repair_start_date,
                details=data.details,
                defectId = data.defectId,
                employeeId = data.employeeId
            )
            self.db_session.add(repair)
            self.db_session.commit()
            return repair
        except Exception as e:
            self.db_session.rollback()
            raise Exception(f"Fail on creating Repair: {e}")

    def updateRepair(self, repairId: str, repairUpdate: Repair) -> Repair:
        try:
            repair = self.__getRepairByAtt('repairId', repairId)

            if not repair:
                raise ValueError(f"Repair with ID '{repairId}' not found.")

            repair.repair_finish_date = datetime.now()
            time_spent = repair.repair_finish_date - repair.repair_start_date
            repair.timeSpent = time_spent
            repair.details = repairUpdate.details

            self.db_session.commit()
            return repair
        except Exception as e:
            self.db_session.rollback()
            raise Exception(f"Error updating Repair: {e}")

    def deleteRepair(self, repairId: str):
        try:
            repair = self.__getRepairByAtt('repairId', repairId)

            if not repair:
                raise ValueError(f"Repair with ID '{repairId}' not found.")

            self.db_session.delete(repair)
            self.db_session.commit()

            return "Repair Removed successfully"
        except Exception as e:
            self.db_session.rollback()
            raise Exception(f"Error deleting Repair: {e}")

    def __getRepairByAtt(self, field: str, value: str) -> Repair:
        try:
            repair = self.db_session.query(Repair).filter(getattr(Repair, field) == value).one()
            return repair
        except Exception as e:
            raise Exception(f"Error finding Repair: {e}")