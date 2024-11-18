from datetime import datetime
from sqlalchemy.orm import Session, lazyload
from models.defect import Defect
from utils.generateUUID import GenerateUUID
from typing import List, Dict
from constants.defect import DefectStatus


class defectService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def getAllDefects(self, status:str=None) -> List[Dict]:
        try:
            query = self.db_session.query(Defect)
            if status:
                query = query.filter(Defect.defectStatus == status)
            print(query)
            defects = query.options(lazyload(Defect.product)).all()
            return [defect.as_dict() for defect in defects]
        except Exception as e:
            raise Exception(f"Error list Product Types: {e}")

    def getDefectById(self, defectId:str) -> Dict:
        try:
            defect = self.__getDefectByAtt('defectId', defectId)
            if not defect:
                raise ValueError(f"defect with ID '{defectId}' not found.")
            return defect.as_dict()
        except Exception as e:
            raise Exception(f"Error find Product Types: {e}")

    def createDefect(self, data:Defect)-> Defect:
        defect_id = GenerateUUID.generate_uuid()
        defect_status = DefectStatus.WIP.value
        registration_date = datetime.now()
        defect = Defect(
                        defectId=defect_id,
                        defectLevel=data.defectLevel,
                        defectStatus=defect_status,
                        registration_date= registration_date,
                        description = data.description,
                        productId=data.productId,
                        employeeId=data.employeeId)
        try:
            self.db_session.add(defect)
            self.db_session.commit()
            return defect
        except Exception as e:
            self.db_session.rollback()
            raise Exception(f"Fail on create defect: {e}")

    def updateDefect(self,defect_id:str, defectUpdate: Defect) -> Defect:
            try:
                defect = self.__getDefectByAtt('defectId', defect_id)

                if not defect:
                    raise ValueError(f"defect with ID '{defect_id}' not found.")

                defect.defectName = defectUpdate.defectLevel
                defect.description = defectUpdate.description
                if defectUpdate.defectStatus:
                    print('update defect status')
                    defect.defectStatus= DefectStatus.DONE.value

                self.db_session.commit()
                return defect
            except Exception as e:
                self.db_session.rollback()
                raise Exception(f"Error updating defect: {e}")

    def deleteDefect(self, defect_id:str):
        try:
            defect = self.__getDefectByAtt('defectId', defect_id)

            if not defect:
                raise ValueError(f"defect with ID '{defect_id}' not found.")

            self.db_session.delete(defect)
            self.db_session.commit()

            return "defect Removed successfully"
        except Exception as e:
            self.db_session.rollback()
            raise Exception(f"Error deleting defect: {e}")

    def __getDefectByAtt(self, field:str, value:str) -> Defect:
        try:
            defect = self.db_session.query(Defect).filter(getattr(Defect, field) == value).one()
            return defect
        except Exception as e:
            raise Exception(f"Error find Product Types: {e}")

