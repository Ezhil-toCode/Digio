# https://documentation.digio.in/digikyc/id_proof/api_integration/
# Fetch ID Card

from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

from fastapi import APIRouter, Depends
from sqlmodel import Session

from digio.models.db_engine import get_db_session

router = APIRouter()


class FetchIDCardRequest(BaseModel):
    id_no: str = Field(..., description="Identifier of the ID Card")
    name: Optional[str] = Field(None, description="Name as per ID Card")
    dob: Optional[str] = Field(None, description="Date of birth as per ID Card")
    file_no: Optional[str] = Field(None, description="Mandatory in case of PASSPORT")
    unique_request_id: Optional[str] = Field(
        ...,
        description="Unique request id for traceability of request and recon purpose. Businesses are required to pass unique id for every request.",
    )


class IDCardType(str, Enum):
    PAN = "PAN"
    PASSPORT = "PASSPORT"
    VEHICLE_RC = "VEHICLE_RC"
    VOTER_ID = "VOTER_ID"
    DRIVING_LICENSE = "DRIVING_LICENSE"


class FetchIDCardResponse(BaseModel):
    pan: Optional[str] = Field(None, description="Applicable in case of PAN")
    category: Optional[str] = Field(None, description="Applicable in case of PAN")
    status: Optional[str] = Field(None, description="Describes the status of ID Card")
    remarks: Optional[str] = Field(None, description="Applicable in case of PAN")
    name_as_per_pan_match: Optional[str] = Field(
        None, description="Applicable in case of PAN"
    )
    date_of_birth_match: Optional[str] = Field(
        None, description="Date of birth as per ID Card details"
    )
    aadhaar_seeding_status: Optional[str] = Field(
        None, description="Applicable in case PAN"
    )

    # Voter ID fields
    pc_name: Optional[str] = Field(
        None, description="Polling center name, Applicable in case VOTER_ID"
    )
    st_code: Optional[str] = Field(
        None, description="State code, Applicable in case VOTER_ID"
    )
    gender: Optional[str] = Field(
        None, description="Gender M/F/T, Applicable in case VOTER_ID"
    )
    rln_name_v2: Optional[str] = Field(
        None,
        description="Relative name in secondary language, Applicable in case VOTER_ID",
    )
    rln_name_v1: Optional[str] = Field(
        None, description="Relative name in hindi, Applicable in case VOTER_ID"
    )
    rln_name_v3: Optional[str] = Field(
        None,
        description="Relative name in tertiary language, Applicable in case VOTER_ID",
    )
    name_v1: Optional[str] = Field(
        None, description="Holder name in hindi, Applicable in case VOTER_ID"
    )
    epic_no: Optional[str] = Field(
        None, description="EPIC number of the voter ID, Applicable in case VOTER_ID"
    )
    ac_name: Optional[str] = Field(
        None, description="Assembly Name, Applicable in case VOTER_ID"
    )
    name_v2: Optional[str] = Field(
        None,
        description="Holder Name in secondary language, Applicable in case VOTER_ID",
    )
    name_v3: Optional[str] = Field(
        None,
        description="Holder name in tertiary language, Applicable in case VOTER_ID",
    )
    pc_no: Optional[str] = Field(
        None, description="Polling center Number, Applicable in case VOTER_ID"
    )
    last_update: Optional[str] = Field(
        None, description="Last Updated time, Applicable in case VOTER_ID"
    )
    dist_no: Optional[str] = Field(
        None, description="District Number, Applicable in case VOTER_ID"
    )
    ps_no: Optional[str] = Field(
        None, description="Polling station number, Applicable in case VOTER_ID"
    )
    ps_name: Optional[str] = Field(
        None, description="Polling station name, Applicable in case VOTER_ID"
    )
    ps_name_v1: Optional[str] = Field(
        None, description="Polling station name in hindi, Applicable in case VOTER_ID"
    )
    st_name: Optional[str] = Field(
        None, description="State name, Applicable in case VOTER_ID"
    )
    dist_name: Optional[str] = Field(
        None, description="District Name, Applicable in case VOTER_ID"
    )
    rln_type: Optional[str] = Field(
        None, description="Relation type, Applicable in case VOTER_ID"
    )
    pc_name_v1: Optional[str] = Field(
        None, description="Polling center name in hindi, Applicable in case VOTER_ID"
    )
    part_name_v1: Optional[str] = Field(
        None, description="Polling center, Applicable in case VOTER_ID"
    )
    ac_name_v1: Optional[str] = Field(
        None, description="Assembly name in hindi, Applicable in case VOTER_ID"
    )
    part_no: Optional[str] = Field(
        None, description="Part number, Applicable in case VOTER_ID"
    )
    dist_name_v1: Optional[str] = Field(
        None, description="District Name in hindi, Applicable in case VOTER_ID"
    )
    section_no: Optional[str] = Field(
        None, description="Section number, Applicable in case VOTER_ID"
    )
    ac_no: Optional[str] = Field(
        None, description="Assembly number, Applicable in case VOTER_ID"
    )
    rln_name: Optional[str] = Field(
        None, description="Relative Name, Applicable in case VOTER_ID"
    )
    age: Optional[str] = Field(
        None, description="Age of holder, Applicable in case VOTER_ID"
    )
    part_name: Optional[str] = Field(
        None, description="Part name, Applicable in case VOTER_ID"
    )
    details: Optional[dict] = Field(
        None,
        description="Contains all other irrelevant details, Applicable in case VOTER_ID",
    )

    # Driving License fields
    date_of_issue: Optional[str] = Field(
        None, description="Applicable in case DRIVING_LICENSE"
    )
    old_new_dl_no: Optional[str] = Field(
        None, description="Applicable in case DRIVING_LICENSE"
    )
    holders_name: Optional[str] = Field(
        None, description="Holder's Name, Applicable in case DRIVING_LICENSE"
    )
    hazardous_valid_till: Optional[str] = Field(
        None, description="Hazardous Valid Till, Applicable in case DRIVING_LICENSE"
    )
    non_transport: Optional[str] = Field(
        None, description="Non-Transport, Applicable in case DRIVING_LICENSE"
    )
    transport: Optional[str] = Field(
        None, description="Transport, Applicable in case DRIVING_LICENSE"
    )
    current_status: Optional[str] = Field(
        None, description="Current Status, Applicable in case DRIVING_LICENSE"
    )
    last_transaction_at: Optional[str] = Field(
        None, description="Last Transaction At, Applicable in case DRIVING_LICENSE"
    )

    # Vehicle RC fields
    fuel_norms: Optional[str] = Field(
        None, description="Fuel Norms, Applicable in case VEHICLE_RC"
    )
    registration_no: Optional[str] = Field(
        None, description="Registration No, Applicable in case VEHICLE_RC"
    )
    maker_model: Optional[str] = Field(
        None, description="Maker / Model, Applicable in case VEHICLE_RC"
    )
    chassis_no: Optional[str] = Field(
        None, description="Chassis No, Applicable in case VEHICLE_RC"
    )
    fitness_upto: Optional[str] = Field(
        None, description="Fitness Upto, Applicable in case VEHICLE_RC"
    )
    owner_name: Optional[str] = Field(
        None, description="Owner Name, Applicable in case VEHICLE_RC"
    )
    vehicle_class: Optional[str] = Field(
        None, description="Vehicle Class, Applicable in case VEHICLE_RC"
    )

    # Passport fields
    file_number: Optional[str] = Field(
        None, description="File Number, Applicable in case PASSPORT"
    )
    given_name: Optional[str] = Field(
        None, description="Given Name, Applicable in case PASSPORT"
    )
    surname: Optional[str] = Field(
        None, description="Surname, Applicable in case PASSPORT"
    )
    type_of_application: Optional[str] = Field(
        None, description="Type of Application, Applicable in case PASSPORT"
    )
    application_received_on_date: Optional[str] = Field(
        None, description="Application Received on Date, Applicable in case PASSPORT"
    )
    passport_number: Optional[str] = Field(
        None, description="Passport Number, Applicable in case PASSPORT"
    )
    nt: Optional[str] = Field(None, description="Applicable in case PASSPORT")


@router.post("/fetch_id_data/", response_model=FetchIDCardResponse)
def create_request(
    *,
    session: Session = Depends(get_db_session),
    types: IDCardType,
    item: FetchIDCardRequest,
) -> FetchIDCardResponse:  # type: ignore
    print(types)
    print(item)
    pass
    # return create_entity(session, item)
