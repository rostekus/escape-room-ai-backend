from fastapi import APIRouter

router = APIRouter()


@router.get("/api/v1/hint/{hint_id}/{riddle_id}")
async def read_user_item(hint_id: int, riddle_id: int):
    return {"hint_id": hint_id, "riddle_id": riddle_id}

    # chain = load_qa_chain(OpenAI(),
    #                   chain_type="stuff")
    # chain.run(input_documents=docs, question="who are the authors of the book?")
    # return docs[0]
