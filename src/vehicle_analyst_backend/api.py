from fastapi  import HTTPException
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os

from src.vehicle_analyst_backend.crew import VehicleAnalystBackend

class VehicleInput(BaseModel):
    vehicle1: str
    vehicle2: str

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",") ,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    """
    Health check endpoint
    """
    return {"message": "vehicle_analyst_backend API is running", "status": "healthy"}


@app.post("/compare-vehicle")
async def compare_vehicle(input_data: VehicleInput):
    """
    Endpoint to run the VehicleAnalystBackend crew with provided vehicle inputs.
    """ 
    try:
        crew_class = VehicleAnalystBackend()
        crew_instance = crew_class.vehicle_comparison_crew()
        inputs = {
            "vehicle1": input_data.vehicle1,
            "vehicle2": input_data.vehicle2
        }
        result = crew_instance.kickoff(inputs=inputs)
        return {
            "status": "success", 
            "result": result.tasks_output
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail={
                "error": str(e),
                "message": "Ensure the crew is properly configured and inputs are valid"
            }
        )

@app.post("/find-ads")
async def find_ads(input_data: VehicleInput):
    """
    Endpoint to run the VehicleAnalystBackend crew with provided vehicle inputs.
    """
    try:
        crew_class = VehicleAnalystBackend()
        ad_finder_crew_instance = crew_class.ad_finder_crew()
        inputs = {
            "vehicle1": input_data.vehicle1,
            "vehicle2": input_data.vehicle2
        }
        result = ad_finder_crew_instance.kickoff(inputs=inputs)
        return {
            "status": "success",
            "result": result.tasks_output
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": str(e),
                "message": "Ensure the crew is properly configured and inputs are valid"
            }
        )
    