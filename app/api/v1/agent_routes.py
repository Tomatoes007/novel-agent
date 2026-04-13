from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.agent import ProposalRequest, GenericAgentRequest
from app.services.project_service import ProjectService
from app.agents.orchestrator import AgentOrchestrator

router = APIRouter(prefix="/agent", tags=["agent"])


@router.post("/proposal")
def generate_proposal(req: ProposalRequest, db: Session = Depends(get_db)):
    return ProjectService.generate_proposal(db, req.user_idea)


@router.post("/run")
def run_agent(req: GenericAgentRequest, db: Session = Depends(get_db)):
    try:
        return AgentOrchestrator.run(db, req.action, req.payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
