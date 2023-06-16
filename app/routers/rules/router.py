from fastapi import APIRouter, Depends

from .schemas import CreateRules_Body
from .dependencies import method_to_upper_if_not_none
from ...database import Rule, ruleStorage


router = APIRouter(prefix="/rules")


@router.get("/", response_model=list[Rule])
def get_rules(url: str = None, method = Depends(method_to_upper_if_not_none)):
    return ruleStorage.get(url, method)

@router.post("/", response_model=list[Rule])
def create_rules(rules_body: CreateRules_Body):
    rules = []
    for url in rules_body.urls:
        for method in rules_body.methods:
            rules.append(Rule(
                url=url,
                method=method,
                refresh_rate=rules_body.refresh_rate,
                requests=rules_body.requests,
            ))
    
    for rule in rules:
        ruleStorage.save(rule)
    
    return rules

@router.delete("/", response_model=bool)
def delete_rule(url: str = None, method = Depends(method_to_upper_if_not_none)):
    return ruleStorage.delete(url, method)
