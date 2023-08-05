"""LinkedDataProof."""

from typing import Optional

from marshmallow import INCLUDE, fields, post_dump

from ....messaging.models.base import BaseModel, BaseModelSchema
from ....messaging.valid import (
    INDY_ISO8601_DATETIME_EXAMPLE,
    INDY_ISO8601_DATETIME_VALIDATE,
    Uri_EXAMPLE,
    Uri_VALIDATE,
    UUIDFour,
)


class LDProof(BaseModel):
    """Linked Data Proof model."""

    class Meta:
        """LinkedDataProof metadata."""

        schema_class = "LinkedDataProofSchema"

    def __init__(
        self,
        type: Optional[str] = None,
        proof_purpose: Optional[str] = None,
        verification_method: Optional[str] = None,
        created: Optional[str] = None,
        domain: Optional[str] = None,
        challenge: Optional[str] = None,
        jws: Optional[str] = None,
        proof_value: Optional[str] = None,
        nonce: Optional[str] = None,
        **kwargs,
    ) -> None:
        """Initialize the LDProof instance."""

        self.type = type
        self.proof_purpose = proof_purpose
        self.verification_method = verification_method
        self.created = created
        self.domain = domain
        self.challenge = challenge
        self.jws = jws
        self.proof_value = proof_value
        self.nonce = nonce
        self.extra = kwargs


class LinkedDataProofSchema(BaseModelSchema):
    """Linked data proof schema.

    Based on https://w3c-ccg.github.io/ld-proofs

    """

    class Meta:
        """Accept parameter overload."""

        unknown = INCLUDE
        model_class = LDProof

    type = fields.Str(
        required=True,
        description=(
            "Identifies the digital signature suite"
            " that was used to create the signature"
        ),
        example="Ed25519Signature2018",
    )

    proof_purpose = fields.Str(
        data_key="proofPurpose",
        required=True,
        description="Proof purpose",
        example="assertionMethod",
    )

    verification_method = fields.Str(
        data_key="verificationMethod",
        required=True,
        description="Information used for proof verification",
        example=(
            "did:key:z6Mkgg342Ycpuk263R9d8Aq6MUaxPn1DDeHyGo38EefXmgDL"
            "#z6Mkgg342Ycpuk263R9d8Aq6MUaxPn1DDeHyGo38EefXmgDL"
        ),
        validate=Uri(),
    )

    created = fields.Str(
        required=True,
        description=(
            "The string value of an ISO8601 combined date"
            " and time string generated by the Signature Algorithm"
        ),
        **INDY_ISO8601_DATETIME,
    )

    domain = fields.Str(
        required=False,
        description="A string value specifying the restricted domain of the signature.",
        example="example.com",
        validate=Uri(),
    )

    challenge = fields.Str(
        required=False,
        description=(
            "Associates a challenge with a proof, for use"
            " with a proofPurpose such as authentication"
        ),
        example=UUIDFour.EXAMPLE,
    )

    jws = fields.Str(
        required=False,
        description="Associates a Detached Json Web Signature with a proof",
        example=(
            "eyJhbGciOiAiRWREUc2UsICJjcml0IjogWyJiNjQiXX0..lKJU0Df_ke"
            "blRKhZAS9Qq6zybm-HqUXNVZ8vgEPNTAjQ1Ch6YBKY7UBAjg6iBX5qBQ"
        ),
    )

    proof_value = fields.Str(
        required=False,
        data_key="proofValue",
        description="The proof value of a proof",
        example=(
            "sy1AahqbzJQ63n9RtekmwzqZeVj494VppdAVJBnMYrTwft6cLJJGeTSSxCCJ6HKnRtwE7"
            "jjDh6sB2z2AAiZY9BBnCD8wUVgwqH3qchGRCuC2RugA4eQ9fUrR4Yuycac3caiaaay"
        ),
    )

    nonce = fields.Str(
        required=False,
        description="The nonce",
        example=(
            "CF69iO3nfvqRsRBNElE8b4wO39SyJHPM7Gg1nExltW5vSfQA1lvDCR/zXX1To0/4NLo=="
        ),
    )

    @post_dump(pass_original=True)
    def add_unknown_properties(self, data: dict, original, **kwargs):
        """Add back unknown properties before outputting."""

        data.update(original.extra)

        return data
