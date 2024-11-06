# Integration Steps
# https://documentation.digio.in/digistudio/integration/create_request/


from fastapi import APIRouter, Depends
from sqlmodel import Session

from digio.models.db_engine import get_db_session
from pydantic import BaseModel, EmailStr, Field, constr, conint
from typing import Optional, List, Dict, Any
from enum import Enum
from datetime import datetime

router = APIRouter()


class NotificationMode(str, Enum):
    SMS = "SMS"
    WHATSAPP = "WHATSAPP"
    ALL = "ALL"


class SignType(str, Enum):
    aadhaar = "aadhaar"
    dsc = "dsc"
    electronic = "electronic"
    external = "external"
    external_sign = "external_sign"
    aadhaar_with_dependents = "aadhaar_with_dependents"
    electronic_with_dependents = "electronic_with_dependents"
    document_review = "document_review"


class SignatureMode(str, Enum):
    otp = "otp"
    slate = "slate"
    kyc = "kyc"
    otp_certified = "otp_certified"
    slate_certified = "slate_certified"
    esign_3 = "esign_3"


class SignAddonType(str, Enum):
    geo_location = "geo_location"


class NoteOnPage(str, Enum):
    first = "first"
    last = "last"
    all = "all"
    custom = "custom"


class CreateKYCRequest(BaseModel):
    customer_identifier: str = Field(
        ...,
        description="Email/mobile phone number of the customer to which the KYC request is sent.",
    )
    notify_customer: bool = Field(
        ...,
        description="If true, a notification is sent to the customer on their email/mobile phone.",
    )
    customer_notification_mode: Optional[NotificationMode] = Field(
        NotificationMode.SMS,
        description="Sends an SMS/Whatsapp notification if the identifier is mobile number.",
    )
    customer_name: str  # Optional[constr(max_length=100, regex=r"^[0-9A-Za-z\s.]{0,}$")] = ( Field(None, description="Name of the customer."))
    reference_id: str  # Optional[constr(regex=r"^[0-9A-Za-z_\-\/]{0,}$")] = Field( None, description="Customer reference number.")
    transaction_id: str  # Optional[constr(regex=r"^[0-9A-Za-z_\-\/]{0,}$")] = Field(None, description="Unique identifier referring to transaction.")
    template_name: str  # constr(min_length=1, max_length=100, regex=r'^[^<>";=%!\*+?]*$') = (  Field(...,description="Name of KYC template created over dashboard to be used while creating the request.",))
    preset_values: Optional[Dict[str, str]] = Field(
        None, description="Preset values for the KYC request."
    )
    digilocker_document_attributes: Optional[Dict[str, Dict[str, str]]] = Field(
        None,
        description="Attributes for fetching additional documents from digilocker.",
    )
    expire_in_days: Optional[conint(ge=1, le=90)] = Field(  # type: ignore
        10, description="Request Expiry in number of days."
    )
    message: str  # Optional[constr(regex=r'^[^<>";=%!\*+?]*$')] = Field(  None, description="Custom message for the customer.")
    reminder: Optional[List[int]] = Field(
        None, description="Reminders in days before expiration."
    )

    class Signer(BaseModel):
        identifier: EmailStr = Field(
            ..., description="Email address or mobile of the signer."
        )
        reason: Optional[constr(max_length=250)] = Field(  # type: ignore
            None, description="Signing reason for the signer."
        )
        sign_type: SignType = Field(
            SignType.aadhaar, description="Type of signature method."
        )
        signature_mode: Optional[SignatureMode] = Field(
            None, description="Mode of signature, if sign_type is electronic."
        )
        name: str  # Optional[constr(max_length=100, regex=r'^[^<>";=%!\*+?]*$')] = Field(None, description="Name of signer.")
        signer_tag: Optional[str] = Field(
            None, description="Signer tag as mentioned in the template."
        )

    other_signers: Optional[List[Signer]] = Field(
        None, description="List of other signers."
    )

    class SignAddon(BaseModel):
        type: SignAddonType = Field(..., description="Type of additional sign feature.")
        performEnrichment: Optional[bool] = Field(
            False, description="Perform enrichment with geo location."
        )
        optional: Optional[bool] = Field(
            False, description="Pass true if geo location is optional."
        )

    signing_addons: Optional[List[SignAddon]] = Field(
        None, description="Additional sign features added upon document signing."
    )

    class EStampRequest(BaseModel):
        tags: Optional[Dict[str, conint(ge=1)]] = Field(  # type: ignore
            None, description="Map of tag names and quantities to be attached."
        )
        note_content: str  # Optional[constr(max_length=250, regex=r'^[^<>";=%!\*+?]*$')] = (Field(None, description="Note on estamp page."))
        note_on_page: Optional[NoteOnPage] = Field(
            NoteOnPage.last, description="Where the note appears on the estamp page."
        )
        sign_on_page: Optional[NoteOnPage] = Field(
            NoteOnPage.all, description="Where to place the signature on the page."
        )

    estamp_request: Optional[EStampRequest] = Field(
        None,
        description="Details of Estamps, Quantities to be consumed, and other merge details.",
    )
    generate_access_token: Optional[bool] = Field(
        False, description="Generate an access token for the request."
    )
    rpd_config_id: Optional[str] = Field(None, description="RPD Configuration ID.")
    collection_amount: Optional[str] = Field(
        None, description="Collection amount related to the request."
    )
    estamp_tags: Optional[Dict[str, conint(ge=1)]] = Field(  # type: ignore
        None, description="Map of estamp tag names and quantities."
    )


###Response


class StatusEnum(str, Enum):
    requested = "requested"
    approval_pending = "approval_pending"
    approved = "approved"
    rejected = "rejected"
    failed = "failed"
    expired = "expired"
    skipped = "skipped"


class ActionTypeEnum(str, Enum):
    video = "video"
    image = "image"
    selfie = "selfie"
    aadhaar_offline = "aadhaar_offline"
    two_way_video = "two_way_video"
    digilocker = "digilocker"
    penny_drop = "penny_drop"
    generic = "generic"
    document_flow = "document_flow"
    fund_collection = "fund_collection"


class ActionStatusEnum(str, Enum):
    requested = "requested"
    success = "success"
    approval_pending = "approval_pending"
    approved = "approved"
    rejected = "rejected"
    failed = "failed"
    expired = "expired"
    skipped = "skipped"


class FaceMatchStatusEnum(str, Enum):
    na = "na"
    new = "new"
    halted = "halted"
    failed = "failed"
    done = "done"


class FaceMatchObjTypeEnum(str, Enum):
    source = "source"
    match_required = "match_required"
    strict_match_required = "strict_match_required"
    none = "none"


class MethodEnum(str, Enum):
    otp_text = "otp_text"
    otp_audio = "otp_audio"
    otp_none = "otp_none"


class MatchResultEnum(str, Enum):
    matched = "matched"
    not_matched = "not_matched"
    failed = "failed"
    none = "none"


class AdditionalValidations(BaseModel):
    type: Optional[str] = None  # Example: "fuzzy_match"
    validation_attributes: Optional[Dict[str, str]] = None
    match_result: Optional[MatchResultEnum] = None
    confidence: Optional[float] = None


class ActionDetails(BaseModel):
    id: str
    step_request_id: Optional[str] = None
    action_ref: Optional[str] = None
    type: Optional[ActionTypeEnum] = None
    status: Optional[ActionStatusEnum] = None
    file_id: Optional[str] = None
    sub_file_id: Optional[str] = None
    execution_request_id: Optional[str] = None
    validation_result: Optional[Dict[str, AdditionalValidations]] = None
    completed_at: Optional[datetime] = None
    face_match_obj_type: Optional[FaceMatchObjTypeEnum] = None
    face_match_status: Optional[FaceMatchStatusEnum] = None
    method: Optional[MethodEnum] = None
    otp: Optional[str] = None
    processing_done: Optional[bool] = None
    retry_count: Optional[int] = None


class AccessTokenDetails(BaseModel):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    entity_id: Optional[str] = None
    id: Optional[str] = None
    valid_till: Optional[datetime] = None
    workflow_name: Optional[str] = None


class KYCResponse(BaseModel):
    id: str
    created_at: datetime
    status: StatusEnum
    customer_identifier: str
    actions: Optional[List[ActionDetails]] = None
    reference_id: Optional[str] = None
    transaction_id: Optional[str] = None
    customer_name: Optional[str] = None
    expire_in_days: Optional[int] = None
    reminder_registered: Optional[bool] = None
    access_token: Optional[AccessTokenDetails] = None
    request_details: Optional[Dict[str, str]] = None
    error_messages: Optional[List[str]] = None
    auto_approved: Optional[bool] = None
    auditor_name: Optional[str] = None
    auditor_identifier: Optional[str] = None
    additional_validations: Optional[List[AdditionalValidations]] = None
    additional_plugin_invocations: Optional[Dict[str, List[Dict[str, Any]]]] = None


# # Create a request object
# request_data = CreateKYCRequest(
#     customer_identifier="customer@example.com",
#     notify_customer=True,
#     customer_name="John Doe",
#     template_name="StandardKYC",
#     reference_id="REF123456",
#     transaction_id="TXN123456",
#     preset_values={"key1": "value1"},
#     expire_in_days=10,
#     message="Please complete your KYC",
#     other_signers=[
#         CreateKYCRequest.Signer(
#             identifier="signer@example.com", reason="To sign the document"
#         )  # type: ignore
#     ],
#     signing_addons=[
#         CreateKYCRequest.SignAddon(
#             type=SignAddonType.geo_location, performEnrichment=True
#         )  # type: ignore
#     ],
#     estamp_request=CreateKYCRequest.EStampRequest(tags={"Tag1": 1}),  # type: ignore
#     generate_access_token=True,
# )  # type: ignore

# # Convert the request object to a dictionary
# request_payload = request_data.dict()

# # Make the API call
# response = httpx.post(
#     url="http://localhost:8080/client/kyc/v2/request/with_template",
#     json=request_payload,
#     auth=("username", "password"),  # Replace with your authentication method
# )

# # Check the response
# if response.status_code == 200:
#     print("Request successful!")
#     response_data = response.json()
#     print(response.json())
#     validated_response = KYCResponse(**response_data)
# else:
#     print(f"Request failed with status code: {response.status_code}")
#     print(response.text)


@router.post("/integration/create_request/", response_model=KYCResponse)
def create_request(
    *, session: Session = Depends(get_db_session), item: CreateKYCRequest
) -> KYCResponse:  # type: ignore
    pass
    # return create_entity(session, item)


"""
curl 'https://api.digio.in/v3/client/kyc/fetch_id_data/PAN' \
  -H 'accept: application/json, text/plain, */*' \
  -H 'accept-language: en-GB,en-US;q=0.9,en;q=0.8,ja;q=0.7' \
  -H 'content-type: application/json' \
  -H 'origin: https://playground.digio.in' \
  -H 'priority: u=1, i' \
  -H 'referer: https://playground.digio.in/' \
  -H 'sec-ch-ua: "Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "macOS"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-site' \
  -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36' \
  -H 'x-session: SIDGOJBRFDCTKDHTWGYEZOAMNSAPMASB' \
  -H 'x-source: PLAYGROUND' \
  --data-raw '{"id_no":"ABVPE8364K"}'

"""


"""
curl 'https://api.digio.in/v3/client/kyc/analyze/file/idcard_cord' \
  -H 'accept: application/json, text/plain, */*' \
  -H 'accept-language: en-GB,en-US;q=0.9,en;q=0.8,ja;q=0.7' \
  -H 'content-type: multipart/form-data; boundary=----WebKitFormBoundaryS4lOoRsCaBvyMatG' \
  -H 'origin: https://playground.digio.in' \
  -H 'priority: u=1, i' \
  -H 'referer: https://playground.digio.in/' \
  -H 'sec-ch-ua: "Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "macOS"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-site' \
  -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36' \
  -H 'x-session: SIDVNCDPURQQWWWZIVEIEVNPNQLXPBSB' \
  -H 'x-source: PLAYGROUND' \
  --data-raw $'------WebKitFormBoundaryS4lOoRsCaBvyMatG\r\nContent-Disposition: form-data; name="front_part"; filename="Ezhil-PAN.jpg"\r\nContent-Type: image/jpeg\r\n\r\n\r\n------WebKitFormBoundaryS4lOoRsCaBvyMatG\r\nContent-Disposition: form-data; name="should_verify"\r\n\r\ntrue\r\n------WebKitFormBoundaryS4lOoRsCaBvyMatG--\r\n'
"""


"""
    curl 'https://api.digio.in/v3/client/kyc/fetch_id_data/PASSPORT' \
  -H 'accept: application/json, text/plain, */*' \
  -H 'accept-language: en-GB,en-US;q=0.9,en;q=0.8,ja;q=0.7' \
  -H 'content-type: application/json' \
  -H 'origin: https://playground.digio.in' \
  -H 'priority: u=1, i' \
  -H 'referer: https://playground.digio.in/' \
  -H 'sec-ch-ua: "Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "macOS"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-site' \
  -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36' \
  -H 'x-session: SIDVNCDPURQQWWWZIVEIEVNPNQLXPBSB' \
  -H 'x-source: PLAYGROUND' \
  --data-raw '{"id_no":"S1861111","file_no":"S 1861111","dob":"20/07/1997"}'

"""
