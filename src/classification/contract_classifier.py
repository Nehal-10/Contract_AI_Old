# from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from src.models.embedding_model import model

CONTRACT_TYPES = {

    "NDA":
    """
    non disclosure agreement
    confidentiality agreement
    confidential information
    proprietary information
    confidentiality obligations
    """,

    "Employment":
    """
    employment agreement
    employee
    employer
    salary
    compensation
    termination of employment
    """,

    "Vendor":
    """
    vendor agreement
    supplier
    procurement
    purchase order
    delivery obligations
    """,

    "Service":
    """
    service agreement
    consulting services
    statement of work
    service provider
    customer
    """,

    "Lease":
    """
    lease agreement
    landlord
    tenant
    rent
    premises
    leased property
    """
}


def classify_contract(text):

    # model = SentenceTransformer(
    #     "all-MiniLM-L6-v2"
    # )

    contract_embedding = model.encode(
        [text[:5000]]
    )

    best_type = None
    best_score = 0

    for contract_type, description in CONTRACT_TYPES.items():

        type_embedding = model.encode(
            [description]
        )

        score = cosine_similarity(
            contract_embedding,
            type_embedding
        )[0][0]

        if score > best_score:

            best_score = score
            best_type = contract_type

    return best_type